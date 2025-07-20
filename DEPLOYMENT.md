# 🚀 Deployment Guide - Number Guessing Game

## Quick Deployment Steps

### 🎯 Recommended: Render.com (100% FREE with real domain)

**Why Render?** 
- ✅ Completely FREE forever
- ✅ Custom domain support (FREE)
- ✅ Auto-deploys from GitHub
- ✅ SSL certificates included
- ✅ No credit card required

**Steps:**
1. **Push to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/number-guessing-game.git
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Click "Get Started for Free"
   - Connect GitHub account
   - Click "New" → "Web Service"
   - Select your repository
   - Configure:
     - **Name**: `number-guessing-game`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
   - Click "Create Web Service"

3. **Your game will be live at**: `https://number-guessing-game-xxxx.onrender.com`

4. **Add Custom Domain** (Optional):
   - Buy domain from Namecheap, GoDaddy, etc. (~$10/year)
   - In Render dashboard → Settings → Custom Domains
   - Add your domain and follow DNS instructions

---

### 🌟 Alternative: Railway.app (Also FREE)

1. **Sign up**: [railway.app](https://railway.app)
2. **New Project** → Deploy from GitHub
3. **Select repo** → Auto-deploys!
4. **Live at**: `https://yourapp.up.railway.app`

---

### 🚄 Alternative: Vercel (Great for static + serverless)

1. **Sign up**: [vercel.com](https://vercel.com)
2. **Import Project** from GitHub
3. **Deploy** → Live instantly!
4. **Live at**: `https://yourapp.vercel.app`

---

### 💰 FREE Domain Options

1. **Freenom** (Free domains):
   - Go to [freenom.com](https://freenom.com)
   - Search for available `.tk`, `.ml`, `.ga`, `.cf` domains
   - Register for FREE (12 months)

2. **GitHub Student Pack** (if you're a student):
   - Free `.me` domain for 1 year
   - Many other free services

3. **Use subdomain**:
   - Most platforms give you free subdomains
   - Example: `number-guessing-game.onrender.com`

---

## 🔧 Files Added for Deployment

- `vercel.json` - Vercel configuration
- `Procfile` - Process file for some platforms
- `runtime.txt` - Python version specification
- Modified `app.py` - Production-ready settings

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Platform account created (Render/Railway/Vercel)
- [ ] Repository connected
- [ ] Build configuration set
- [ ] Deployment successful
- [ ] Custom domain added (optional)
- [ ] SSL certificate active (automatic)

## 🎮 Test Your Live Game

After deployment:
1. Visit your live URL
2. Test number guessing functionality
3. Try the "New Game" button
4. Check responsive design on mobile
5. Share with friends! 🎉

---

**Estimated deployment time**: 5-10 minutes  
**Cost**: $0 (completely free!)  
**Maintenance**: Auto-updates from GitHub pushes
