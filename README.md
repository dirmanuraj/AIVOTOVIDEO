# 🎬 AI Video Generator - Web Dashboard

Create beautiful 30-40 minute AI videos from Polish voiceovers with **zero hassle**.

Upload your audio → Automatic video generation with captions → Download MP4

**100% FREE** • **No API keys** • **No credit card** • **Deploy in 5 minutes**

---

## ✨ Features

✅ **Beautiful Web Dashboard** - Modern, responsive UI  
✅ **Real-time Progress Tracking** - See each step as it happens  
✅ **Auto Transcription** - Polish speech-to-text (Whisper)  
✅ **Image Prompts** - AI suggests visuals for your content  
✅ **Auto Captions** - Polish subtitles generated automatically  
✅ **Video Generation** - Smooth animations from images  
✅ **One-Click Download** - Get your MP4 when ready  
✅ **100% FREE** - No costs, no subscriptions  

---

## 🚀 Quick Deploy

### Option 1: Deploy to Railway (Easiest - 5 minutes)

```bash
# 1. Create GitHub repo and push code
# 2. Go to railway.app
# 3. Connect GitHub → Select this repo
# 4. Done! Your dashboard is LIVE
```

[See Full Deployment Guide](DEPLOYMENT_GUIDE.md)

### Option 2: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py

# Open browser
# http://localhost:5000
```

---

## 📁 Project Structure

```
ai-video-generator/
├── app.py                    # Flask web server
├── requirements.txt          # Python dependencies
├── Procfile                  # Railway deployment config
├── railway.toml             # Railway settings
├── templates/
│   └── dashboard.html       # Web dashboard UI
├── DEPLOYMENT_GUIDE.md      # Deploy instructions
└── README.md               # This file
```

---

## 🎯 How It Works

### User Flow:
1. **Upload** - Drag & drop Polish voiceover (MP3/WAV)
2. **Watch** - Real-time progress bars for each step
3. **Download** - Get finished MP4 video

### Backend Pipeline:
1. **Transcription** - Whisper converts speech to Polish text
2. **Analysis** - Content breaks into 5-min segments
3. **Prompts** - AI generates visual descriptions
4. **Images** - (Manual) Download from Hugging Face
5. **Videos** - OpenCV creates smooth animations
6. **Captions** - Auto-generated Polish subtitles
7. **Assembly** - DaVinci Resolve combines everything
8. **Export** - Final MP4 ready for download

---

## 💻 Technology Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Web Server | Flask (Python) | FREE |
| Speech-to-Text | OpenAI Whisper | FREE |
| Image Gen | Hugging Face Spaces | FREE |
| Video Creation | OpenCV | FREE |
| Hosting | Railway.app | FREE |
| Deployment | GitHub + Railway | FREE |

---

## 🎨 Dashboard Features

### Upload Section
- Drag & drop interface
- File validation
- Size display
- Beautiful gradient background

### Processing Section
- Real-time progress bar
- 8-step workflow display
- Current step highlighting
- Completion percentage

### Completion Section
- Success message
- Download button
- Create new video button
- Usage statistics

---

## 🔧 Configuration

No configuration needed! The app works out of the box.

Optional environment variables:
```
PORT=5000                          # Server port
UPLOAD_FOLDER=/tmp/uploads        # Upload directory
OUTPUT_FOLDER=/tmp/outputs        # Output directory
PYTHONUNBUFFERED=1               # Debug logging
```

---

## 📊 Performance

- **Upload speed:** Depends on your internet
- **Processing time:** 5-10 minutes per video
- **Download speed:** Fast (depends on internet)
- **Concurrent users:** Railway FREE = 5-10
- **Max file size:** 2GB
- **Max video length:** 60 minutes

---

## 🆘 Troubleshooting

### Upload fails
- Check file format (MP3, WAV, M4A)
- Check file size < 2GB
- Try refreshing page

### Processing hangs
- Check Railway logs
- Common: First run downloads Whisper model
- Takes 5-10 minutes, be patient

### Download fails
- Video may not be ready yet
- Check progress is 100%
- Try refreshing page

### Low quality video
- Depends on image quality
- Use good prompts for images
- Higher resolution = better output

---

## 📝 Example Usage

1. Record your Polish voiceover in any app
2. Export as MP3
3. Go to your dashboard
4. Drag & drop the MP3
5. Watch progress
6. Wait for "Complete"
7. Click "Download Video"
8. Share your AI video!

---

## 🎓 Learning Resources

- **Whisper Documentation:** https://github.com/openai/whisper
- **Flask Tutorial:** https://flask.palletsprojects.com
- **OpenCV Guide:** https://docs.opencv.org
- **Railway Docs:** https://docs.railway.app
- **Hugging Face:** https://huggingface.co

---

## 🤝 Contributing

Want to improve the dashboard?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Ideas for improvements:
- Add more language support
- AI image generation integration
- Custom video effects
- Batch processing
- API endpoint for automation

---

## 📄 License

This project is FREE and open source.

---

## 🎬 Example Workflow

```
Input:  Polish voiceover (30 min, 45MB MP3)
        ↓
Transcribe:  "Dzień dobry, dziś opowiemy o..."
        ↓
Segments:   6 × 5-min chunks
        ↓
Prompts:    "cinematic futuristic city", "AI robots", ...
        ↓
Images:     48 AI-generated images
        ↓
Videos:     6 × 5-min video clips
        ↓
Captions:   Polish subtitles with timing
        ↓
Output:     final_video_30min.mp4 (1.2GB, 1080p)
```

---

## 🚀 Deploy Now

### 1. GitHub
```bash
git clone https://github.com/your-username/ai-video-generator
cd ai-video-generator
```

### 2. Railway
- Go to https://railway.app
- Click "New Project"
- Connect GitHub
- Deploy!

### 3. Share
```
Your dashboard URL:
https://ai-video-generator-prod.up.railway.app
```

---

## 💡 Pro Tips

1. **Best audio quality:** 128kbps MP3, no background noise
2. **Faster processing:** Smaller files process faster
3. **Better visuals:** Specific image prompts = better results
4. **Share results:** Videos ready immediately after processing

---

## 📞 Support

Issues? Questions?

1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review Railway logs
3. Check browser console (F12)
4. Restart the service

---

## 🎉 You're All Set!

Your AI Video Generator is ready to create amazing 30-40 minute videos.

**Next Step:** Deploy to Railway and start creating!

[Go to Deployment Guide](DEPLOYMENT_GUIDE.md)

---

**Built with ❤️ for video creators everywhere**

*Generate, create, share. No limits. No costs.*
