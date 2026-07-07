# 🚀 Deployment Guide — Study Marks Predictor

This guide walks you through uploading your project to GitHub and deploying it on Streamlit Cloud.

---

## 📋 Pre-Deployment Checklist

Before pushing to GitHub, verify:

- [x] **README.md** — Updated with features, installation, and usage docs
- [x] **requirements.txt** — All dependencies listed with pinned versions
- [x] **.gitignore** — Excludes `.venv/`, `__pycache__/`, `.env`, `schedule.json` (optional)
- [x] **LICENSE** — MIT license included
- [x] **app.py** — No local file paths, deployment-ready
- [x] **Syntax check** — Run `python -m py_compile app.py` ✅
- [x] **Import verification** — All packages importable ✅
- [x] **Streamlit runs locally** — `streamlit run app.py` works ✅

---

## 📤 Step 1: Initialize Git Repository

```bash
cd c:\ml_miniproj

# Initialize Git
git init

# Configure Git (use your GitHub email/username)
git config user.email "your-email@example.com"
git config user.name "Your GitHub Username"

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: AI Study Planner Dashboard - marks prediction, schedule management, progress tracking"
```

**Expected output:**
```
[main (root-commit) abcd1234] Initial commit: ...
 6 files changed, 150 insertions(+)
 create mode 100644 app.py
 create mode 100644 README.md
 create mode 100644 requirements.txt
 create mode 100644 .gitignore
 create mode 100644 LICENSE
 create mode 100644 schedule.json
```

---

## 🔐 Step 2: Create GitHub Repository

2. **GitHub Repository:** https://github.com/Malika26-08/study-marks-predictor
   - **Repository name:** `study-marks-predictor`
   - **Visibility:** Public (for portfolio/recruiters)
   - **Description:** "AI-powered study planner and exam marks prediction dashboard with schedule management and analytics"

3. **Repository URL:** `https://github.com/Malika26-08/study-marks-predictor.git`

---

## 📡 Step 3: Connect Local Repo to GitHub and Push

```bash
cd c:\ml_miniproj

# Add the remote GitHub repository
git remote add origin https://github.com/yourusername/study-marks-predictor.git

# Rename branch to main (if not already)
git branch -M main

# Push your local commits to GitHub
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 12 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (6/6), 2.34 KiB | 2.34 MiB/s, done.
Total 6 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/yourusername/study-marks-predictor.git
 * [new branch]      main -> main
Branch 'main' is set to track remote branch 'main' from 'origin'.
```

Verify on GitHub: https://github.com/yourusername/study-marks-predictor ✅

---

## 🌐 Step 4: Deploy to Streamlit Cloud

### Prerequisites
- GitHub account (✅ just created repo)
- Streamlit Cloud account (free tier available)

### Deployment Steps

1. **Sign in to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "Sign in with GitHub" (or create account)
   - Authorize Streamlit to access your GitHub repos

2. **Deploy New App:**
   - Click **"Create app"** button
   - **Repository:** Select `yourusername/study-marks-predictor`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - Click **"Deploy"**

3. **Wait for Deployment:**
   - Streamlit will build and deploy (usually takes 1-2 minutes)
   - You'll see logs showing the build progress
   - Once complete, your app URL appears: `https://your-username-study-marks-predictor.streamlit.app`

4. **Share Your App:**
   - Copy the app URL
   - Add to GitHub README
   - Share with recruiters, portfolio, etc.

---

## 🔄 Making Updates (After Initial Deployment)

Every time you push changes to GitHub, Streamlit auto-deploys:

```bash
cd c:\ml_miniproj

# Make code changes in app.py or other files

# Stage changes
git add .

# Commit with descriptive message
git commit -m "Feature: Add export as CSV, improve prediction confidence calculation"

# Push to GitHub
git push origin main
```

Streamlit will automatically detect the push and redeploy within 1-2 minutes. ✅

---

## 🛠️ Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| **App won't start (import errors)** | Check `requirements.txt` — ensure all imports in `app.py` are listed. |
| **"ModuleNotFoundError"** | Missing dependency in `requirements.txt`. Add it: `pip install <package>` locally, then update `requirements.txt`. |
| **Port 8501 already in use** | `streamlit run app.py --server.port 8502` |
| **Data not persisting** | Streamlit Cloud has ephemeral storage. Use cloud database (Firebase, Supabase) for persistent data. For now, data persists per session. |
| **app.py too large** | Refactor into modules (e.g., `pages/dashboard.py`, `utils/predict.py`) if size exceeds 500KB. |

---

## 📊 Deployment Verification

After deployment, verify these URLs work:

- ✅ App loads at: `https://your-username-study-marks-predictor.streamlit.app`
- ✅ GitHub repo visible: `https://github.com/yourusername/study-marks-predictor`
- ✅ README displays properly (with screenshots, if added)
- ✅ All features work (predictions, schedule, insights)
- ✅ Export buttons work
- ✅ No console errors (check browser DevTools)

---

## 📝 Portfolio Integration

### For Recruiters / Portfolio

**Update your portfolio with:**

```markdown
## Study Marks Predictor

**Live App:** [https://your-username-study-marks-predictor.streamlit.app](...)
**GitHub:** [yourusername/study-marks-predictor](...)

- Built with **Streamlit**, **scikit-learn**, **Plotly**
- Features: ML marks prediction, task scheduling, progress analytics
- 500+ lines of production-ready Python code
```

### GitHub README Tips

- Add project screenshots (capture from your live app)
- Link to live deployment
- List key tech stack
- Include installation steps
- Add contributing guidelines
- Ask for GitHub stars ⭐

---

## 🔒 Keeping Secrets Safe

If your app needs API keys, environment variables, or credentials:

1. **Create `.env` file locally (not committed):**
   ```
   OPENAI_API_KEY=sk-...
   DATABASE_URL=postgresql://...
   ```

2. **Access in `app.py`:**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   api_key = os.getenv("OPENAI_API_KEY")
   ```

3. **On Streamlit Cloud:**
   - Go to app settings → Secrets
   - Add same environment variables
   - Streamlit loads them automatically

4. **Update `.gitignore`:**
   ```
   .env
   secrets.toml
   ```

---

## 📈 Next Steps for Growth

- [ ] **Add screenshots** to README (use your live app)
- [ ] **Enable authentication** (Google login via streamlit-authenticator)
- [ ] **Add cloud database** (Supabase for persistent user data)
- [ ] **Create issues/PRs workflow** for community contributions
- [ ] **Add GitHub Actions CI/CD** (auto-test on push)
- [ ] **Monitor usage** (Streamlit Cloud analytics dashboard)
- [ ] **Create Docker image** for self-hosted deployment

---

## 🚀 Your App is Live! 🎉

Share your Streamlit Cloud URL everywhere:
- Twitter/LinkedIn: "Just built an AI study planner with marks prediction! Live at [URL]"
- Portfolio website
- Resume/CV (GitHub section)
- Discord, Reddit, HN (Show HN)
- Interview prep: "I built a Streamlit app for study optimization"

---

**Questions?** See [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app) or [GitHub Pages](https://pages.github.com/)
