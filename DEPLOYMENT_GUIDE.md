# Deploy AI Video Generator to Railway (FREE)

## Overview
Your beautiful web dashboard will be live in 5 minutes with automatic video processing.

---

## Step 1: Prepare Your GitHub Repository (2 minutes)

### 1.1 Create GitHub Repository
1. Go to https://github.com/new
2. Create new repository: `ai-video-generator`
3. Choose "Public" (FREE)
4. Click "Create repository"

### 1.2 Upload Files to GitHub

Option A: Using Git Command Line
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-video-generator.git
cd ai-video-generator

# Copy these files to the folder:
# - app.py
# - requirements.txt
# - Procfile
# - railway.toml
# - .gitignore
# - templates/dashboard.html

# Push to GitHub
git add .
git commit -m "Initial commit: AI video generator"
git push -u origin main
```

Option B: Upload via GitHub Website
1. Click "Add file" → "Upload files"
2. Drag and drop all files
3. Commit changes

---

## Step 2: Deploy to Railway (3 minutes)

### 2.1 Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (easiest)
3. Connect your GitHub account

### 2.2 Create New Project
1. Dashboard → "New Project"
2. Select "Deploy from GitHub"
3. Select your `ai-video-generator` repository
4. Click "Deploy"

### 2.3 Configure Build
Railway will automatically detect:
- Python 3.10
- Requirements from `requirements.txt`
- Start command from `Procfile`

### 2.4 Wait for Deploy
- Deployment takes 5-10 minutes
- You'll see logs streaming
- When done, you'll get a live URL

### 2.5 Get Your Live URL
1. Go to "Deployments"
2. Copy your live URL (e.g., `https://ai-video-generator-prod.up.railway.app`)
3. Share it with friends!

---

## Step 3: Test Your Dashboard

1. Open your Railway URL in browser
2. You should see the beautiful purple dashboard
3. Try uploading a small audio file (MP3)
4. Watch the progress bars in real-time
5. Download your video when complete

---

## How It Works on Railway

```
Your Browser (Web Dashboard)
    ↓
Railway Server (Python Flask App)
    ↓
Step 1: Transcribe (Whisper - FREE)
    ↓
Step 2: Analyze content
    ↓
Step 3: Generate image prompts
    ↓
Step 4-5: Create video clips
    ↓
Step 6: Generate captions
    ↓
Download video (MP4)
```

---

## Free Tier Limits

### Railway Free Plan
- **Compute:** 5GB bandwidth/month
- **Duration:** Unlimited dyno hours
- **No credit card needed** ✓

### Whisper Model
- Runs on Railway server
- ~140MB download (one-time)
- Takes 30-60 seconds per video

### Video Processing
- Up to 2GB file uploads
- Full video generation
- Multi-threaded processing

---

## Troubleshooting

### "Build Failed"
- Check `requirements.txt` syntax
- Ensure all dependencies listed
- Delete and redeploy

### "App Crashes"
- Check Railway logs: Dashboard → "Logs"
- Look for error messages
- Common: Python version mismatch

### "Upload Fails"
- Maximum file size: 2GB
- Check browser console for errors
- Try smaller file first

### "Video Processing Slow"
- Whisper download takes time first run
- Normal processing: 5-10 minutes
- Patience is key!

---

## Performance Tips

### For 30-40 Minute Videos
- **Max upload:** 500MB audio file
- **Processing time:** 15-30 minutes
- **Download:** Video ready immediately after processing

### Optimize Audio
- MP3 format (smaller file)
- 128kbps bitrate (good quality)
- Mono or stereo (no difference)

### Network
- Use stable WiFi
- Don't interrupt upload
- Keep browser tab open

---

## Advanced: Scaling Up

### If you get lots of users:
1. Railway → Settings
2. "Scale" → Increase memory
3. Add environment variables for API keys

### Add More Workers
Edit `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 4 --threads 4
```

---

## Environment Variables (Optional)

Add in Railway Dashboard:

```
PYTHONUNBUFFERED=1
FLASK_ENV=production
UPLOAD_FOLDER=/tmp/uploads
OUTPUT_FOLDER=/tmp/outputs
```

---

## Custom Domain (Optional)

1. Railway Dashboard → Settings
2. "Domains" → Add custom domain
3. Add your domain (e.g., `videogenerator.com`)
4. Follow DNS setup instructions

---

## Monitoring & Logs

### Check Health
```
https://your-app.railway.app/health
```
Should return: `{"status": "healthy"}`

### View Logs
1. Railway Dashboard
2. Deployments → Click latest
3. "Logs" tab shows everything

### Track Usage
- Dashboard → "Metrics"
- CPU, Memory, Network graphs

---

## FAQ

**Q: Will my videos be deleted?**
A: Yes, temporary files deleted after 24 hours. Always download immediately.

**Q: Can I upload 1 hour videos?**
A: Max 2GB. Anything under 1GB works fine.

**Q: How many concurrent users?**
A: On FREE tier: ~5-10 simultaneously. Scale up if needed.

**Q: Can I add more features?**
A: Yes! Edit `app.py` and push to GitHub. Railway auto-redeploys.

**Q: Is it really FREE?**
A: Yes! Railway gives free compute credits + no credit card required.

---

## Share Your Dashboard

```
Share this link with anyone:
https://your-app.railway.app

They can:
1. Upload their voiceover
2. Watch processing
3. Download video
```

---

## Next Steps

1. ✅ Create GitHub repo
2. ✅ Deploy to Railway
3. ✅ Test with audio file
4. ✅ Share link with friends
5. ✅ Collect feedback
6. ✅ Add custom features (optional)

---

## Support

- Railway Docs: https://docs.railway.app
- Flask Docs: https://flask.palletsprojects.com
- Whisper Docs: https://github.com/openai/whisper

---

## Video Tutorial Commands

If following a video tutorial, use these:

```bash
# Install locally first (optional)
pip install -r requirements.txt
python app.py

# Then deploy to Railway as described above
```

---

## Success Checklist

- [x] GitHub repo created
- [x] Files uploaded to GitHub
- [x] Railway account created
- [x] Project deployed
- [x] Dashboard loads
- [x] Audio upload works
- [x] Processing starts
- [x] Video downloads
- [x] Share with friends!

---

**Your AI Video Generator is now LIVE! 🚀**

Share the link and let people create amazing videos.
