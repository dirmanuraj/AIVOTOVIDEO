#!/usr/bin/env python3
"""
AI Video Generator - Minimal Flask App for Railway
Zero external dependencies (except Flask)
"""

import os
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import threading
import time

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024

# Folders
Path('/tmp/uploads').mkdir(parents=True, exist_ok=True)
Path('/tmp/outputs').mkdir(parents=True, exist_ok=True)

jobs = {}

class Job:
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = "queued"
        self.progress = 0
        self.step_index = 0
        self.steps = [
            "📝 Analyzing voiceover",
            "🔍 Detecting language",
            "📊 Breaking into segments",
            "🎨 Generating prompts",
            "🤖 AI analyzing",
            "✂️ Creating clips",
            "📝 Generating captions",
            "🎬 Assembling video",
            "✅ Complete!"
        ]
        self.error = None
        self.filename = ""
        
    def update(self, step):
        self.step_index = step
        self.progress = int((step / len(self.steps)) * 100)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'voiceover' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['voiceover']
    if not file.filename:
        return jsonify({'error': 'Empty filename'}), 400
    
    # Validate extension
    allowed = {'mp3', 'wav', 'm4a', 'aac', 'ogg', 'flac'}
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in allowed:
        return jsonify({'error': f'Invalid format. Allowed: {", ".join(allowed)}'}), 400
    
    # Create job
    job_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    job = Job(job_id)
    job.filename = file.filename
    jobs[job_id] = job
    
    # Save file
    filename = secure_filename(file.filename)
    filepath = f'/tmp/uploads/{job_id}_{filename}'
    file.save(filepath)
    
    job.status = "processing"
    
    # Process in background
    thread = threading.Thread(target=process, args=(job_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'filename': filename})

@app.route('/api/progress/<job_id>')
def progress(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'step_index': job.step_index,
        'step': job.steps[job.step_index] if job.step_index < len(job.steps) else 'Done',
        'steps': job.steps,
        'error': job.error
    })

@app.route('/api/download/<job_id>')
def download(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Not found'}), 404
    
    job = jobs[job_id]
    video_path = f'/tmp/outputs/{job_id}/video.mp4'
    
    if job.status != "complete" or not Path(video_path).exists():
        return jsonify({'error': 'Not ready'}), 400
    
    try:
        return open(video_path, 'rb')
    except:
        return jsonify({'error': 'Download error'}), 500

def process(job_id):
    """Simulate video processing"""
    job = jobs[job_id]
    
    try:
        output_dir = Path(f'/tmp/outputs/{job_id}')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Simulate 9 steps
        for step in range(len(job.steps)):
            job.update(step)
            time.sleep(1)
        
        # Create dummy video file
        video_path = output_dir / 'video.mp4'
        with open(video_path, 'wb') as f:
            # Write minimal MP4 header
            f.write(b'\x00\x00\x00\x20ftypisom')
            f.write(b'\x00' * 1000)  # Padding
        
        job.status = "complete"
        job.progress = 100
        
    except Exception as e:
        job.error = str(e)
        job.status = "error"

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
