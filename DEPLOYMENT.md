# CO₂ Emission Detection - Render Deployment Guide

## 🚀 Auto-Deploy on Render (Free Tier)

### Prerequisites
- GitHub repository: `https://github.com/jayaraman2212066/CO2_EMISSION_DETECTION_AUTO_GENERATOR_LEVEL.git`
- Render account (free)

### Deployment Steps

1. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configuration**
   - **Repository**: `jayaraman2212066/CO2_EMISSION_DETECTION_AUTO_GENERATOR_LEVEL`
   - **Branch**: `main`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300 --workers 1 --threads 1 --max-requests 100`
   - **Plan**: Free

3. **Environment Variables** (Auto-configured via render.yaml)
   - `PYTHON_VERSION`: 3.9.18
   - `TF_CPP_MIN_LOG_LEVEL`: 3
   - `DATABASE_URL`: sqlite:///co2_predictions.db

### Optimizations for Free Tier

✅ **TensorFlow-CPU**: Reduced memory usage  
✅ **SQLite Database**: No external DB required  
✅ **Single Worker**: Memory efficient  
✅ **Build Script**: Automated verification  
✅ **Auto-Deploy**: Enabled on git push  

### Features Working
- 🤖 ML Model Predictions
- 📊 CO₂ Level Categorization  
- 🎤 Speech Synthesis
- 📱 Responsive UI
- 💾 Prediction History
- 🔄 Auto-generation

### Expected Deployment Time
- Build: ~5-8 minutes
- Deploy: ~2-3 minutes
- Total: ~10 minutes

### Troubleshooting
- Check build logs for TensorFlow installation
- Verify model file exists in logs
- Monitor memory usage (512MB limit)

### Live URL
After deployment: `https://co2-emission-detection-[random].onrender.com`