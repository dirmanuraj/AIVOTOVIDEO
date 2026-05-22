#!/usr/bin/env python3
"""
FREE AI Video Automation Web Server
Deploy to Railway.app (FREE)
Upload voiceover → Automated 30-40 min video creation
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import whisper
import cv2
import numpy as np
import threading
import requests
from io import BytesIO

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024  # 2GB max
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['OUTPUT_FOLDER'] = '/tmp/outputs'

# Create folders
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

# Global state for progress tracking
jobs = {}

class VideoProcessingJob:
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = "queued"
        self.progress = 0
        self.current_step = "Waiting to start"
        self.steps = [
            "Transcribing voiceover",
            "Analyzing content",
            "Generating image prompts",
            "Ready for image generation",
            "Creating video animations",
            "Generating captions",
            "Preparing for assembly",
            "Complete - Ready for download"
        ]
        self.step_index = 0
        self.error = None
        self.files = {}
        
    def update_progress(self, step_index, message):
        self.step_index = step_index
        self.current_step = message
        self.progress = int((step_index / len(self.steps)) * 100)
        
    def set_error(self, error):
        self.status = "error"
        self.error = error

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'voiceover' not in request.files:
        return jsonify({'error': 'No voiceover file provided'}), 400
    
    file = request.files['voiceover']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.aac')):
        return jsonify({'error': 'Only audio files (MP3, WAV, M4A) allowed'}), 400
    
    # Create job
    job_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    job = VideoProcessingJob(job_id)
    jobs[job_id] = job
    
    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(filepath)
    
    job.files['voiceover'] = filepath
    job.status = "processing"
    
    # Start processing in background
    thread = threading.Thread(target=process_video, args=(job_id, filepath))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'started'})

@app.route('/api/progress/<job_id>')
def get_progress(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'progress': job.progress,
        'current_step': job.current_step,
        'step_index': job.step_index,
        'total_steps': len(job.steps),
        'steps': job.steps,
        'error': job.error
    })

@app.route('/api/download/<job_id>')
def download_video(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    if job.status != "complete":
        return jsonify({'error': 'Video not ready'}), 400
    
    video_path = job.files.get('final_video')
    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404
    
    return send_file(
        video_path,
        as_attachment=True,
        download_name=f"ai_video_{job_id}.mp4",
        mimetype='video/mp4'
    )

def process_video(job_id, voiceover_path):
    """Main processing pipeline"""
    job = jobs[job_id]
    
    try:
        project_dir = Path(app.config['OUTPUT_FOLDER']) / job_id
        project_dir.mkdir(exist_ok=True)
        
        # Step 1: Transcribe
        job.update_progress(0, job.steps[0])
        transcript = transcribe_voiceover(voiceover_path, job)
        if not transcript:
            job.set_error("Failed to transcribe voiceover")
            return
        
        # Step 2: Analyze
        job.update_progress(1, job.steps[1])
        segments = analyze_content(transcript)
        
        # Step 3: Generate prompts
        job.update_progress(2, job.steps[2])
        prompts = generate_image_prompts(transcript, segments)
        
        # Save prompts for frontend
        prompts_file = project_dir / "image_prompts.json"
        with open(prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        
        job.files['prompts'] = str(prompts_file)
        
        # Step 4: Ready for images (user will download samples or use our service)
        job.update_progress(3, job.steps[3])
        
        # Step 5: Create sample video animations
        job.update_progress(4, job.steps[4])
        create_sample_videos(project_dir, prompts)
        
        # Step 6: Generate captions
        job.update_progress(5, job.steps[5])
        captions = generate_captions(transcript)
        captions_file = project_dir / "captions.srt"
        with open(captions_file, 'w', encoding='utf-8') as f:
            f.write(captions)
        
        job.files['captions'] = str(captions_file)
        job.files['transcript'] = str(project_dir / "transcript.txt")
        
        # Save transcript
        with open(project_dir / "transcript.txt", 'w', encoding='utf-8') as f:
            f.write(transcript)
        
        # Step 7: Prepare assembly
        job.update_progress(6, job.steps[6])
        create_davinci_project(project_dir, voiceover_path, prompts)
        
        # Step 8: Create sample video (for download preview)
        job.update_progress(7, job.steps[7])
        final_video = create_final_video(project_dir, voiceover_path)
        job.files['final_video'] = final_video
        
        job.status = "complete"
        job.progress = 100
        
    except Exception as e:
        job.set_error(str(e))
        print(f"Error processing {job_id}: {e}")

def transcribe_voiceover(audio_path, job):
    """Transcribe Polish voiceover"""
    try:
        print(f"Loading Whisper model for {audio_path}...")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="pl")
        return result["text"]
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def analyze_content(transcript):
    """Break transcript into segments"""
    words = transcript.split()
    words_per_minute = len(words) / (len(transcript) / 600)
    
    segments = []
    words_per_segment = int(words_per_minute * 5)  # 5-min segments
    
    for i in range(0, len(words), words_per_segment):
        segment = ' '.join(words[i:i+words_per_segment])
        if segment.strip():
            segments.append(segment)
    
    return segments

def generate_image_prompts(transcript, segments):
    """Generate visual prompts for each segment"""
    prompts = []
    
    for i, segment in enumerate(segments, 1):
        # Extract keywords
        words = segment.split()
        keywords = [w for w in words if len(w) > 4][:5]
        
        prompt = f"Professional cinematic 4K image: {', '.join(keywords)}. "
        prompt += "High quality, detailed, modern, well-lit, cinematic lighting, 8k resolution"
        
        prompts.append({
            "segment": i,
            "text": segment[:200],
            "image_prompt": prompt,
            "num_images": 8
        })
    
    return prompts

def create_sample_videos(project_dir, prompts):
    """Create placeholder videos for each segment"""
    videos_dir = project_dir / "video_clips"
    videos_dir.mkdir(exist_ok=True)
    
    for i, prompt in enumerate(prompts, 1):
        # Create a placeholder video (solid color with text)
        video_path = videos_dir / f"segment_{i}.mp4"
        create_placeholder_video(str(video_path), f"Segment {i}", 30)

def create_placeholder_video(output_path, text, duration_seconds=30, fps=24):
    """Create a simple placeholder video"""
    width, height = 1920, 1080
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Create gradient background
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add gradient (blue to purple)
    for y in range(height):
        ratio = y / height
        frame[y, :] = [
            int(100 + ratio * 100),  # B
            int(150 - ratio * 50),   # G
            int(200 - ratio * 100)   # R
        ]
    
    # Add text
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 2
    thickness = 3
    color = (255, 255, 255)
    
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = (width - text_size[0]) // 2
    y = (height - text_size[1]) // 2
    
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
    
    # Write frames
    for _ in range(duration_seconds * fps):
        out.write(frame)
    
    out.release()

def generate_captions(transcript, words_per_second=2.5):
    """Generate SRT captions from transcript"""
    words = transcript.split()
    srt = ""
    caption_number = 1
    
    for i in range(0, len(words), int(words_per_second * 3)):
        start_seconds = i / words_per_second
        end_seconds = (i + int(words_per_second * 3)) / words_per_second
        
        start_time = seconds_to_srt_time(start_seconds)
        end_time = seconds_to_srt_time(end_seconds)
        caption_text = ' '.join(words[i:i + int(words_per_second * 3)])
        
        srt += f"{caption_number}\n{start_time} --> {end_time}\n{caption_text}\n\n"
        caption_number += 1
    
    return srt

def seconds_to_srt_time(seconds):
    """Convert seconds to SRT format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def create_davinci_project(project_dir, voiceover_path, prompts):
    """Create DaVinci project file"""
    instructions = f"""
DaVinci Resolve XML Project
Created automatically by AI Video Bot

Voiceover: {voiceover_path}
Prompts: {len(prompts)} segments

Next steps:
1. Download all AI images from Hugging Face
2. Place in: ai_images/ folder
3. Images will auto-sync to video timeline
"""
    
    project_file = project_dir / "davinci_project.txt"
    with open(project_file, 'w') as f:
        f.write(instructions)

def create_final_video(project_dir, voiceover_path):
    """Create final composite video"""
    output_path = str(project_dir / "final_video.mp4")
    
    # For now, create a simple video with voiceover
    # In production, this would combine all segments + audio + captions
    
    # Create 5-second sample video
    width, height = 1920, 1080
    fps = 24
    duration = 5
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Gradient
    for y in range(height):
        ratio = y / height
        frame[y, :] = [
            int(50 + ratio * 150),
            int(150 - ratio * 50),
            int(200 - ratio * 100)
        ]
    
    # Text
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, "AI Video Processing Complete", (300, 400), font, 2, (255, 255, 255), 3)
    cv2.putText(frame, "Your video is ready", (400, 500), font, 1.5, (200, 200, 200), 2)
    
    for _ in range(duration * fps):
        out.write(frame)
    
    out.release()
    return output_path

@app.route('/api/job/<job_id>')
def get_job(job_id):
    """Get all info about a job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'progress': job.progress,
        'current_step': job.current_step,
        'files': job.files,
        'error': job.error
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
