# CI/CD Architecture & Flow Diagram

## What is CI/CD? 🔄

```
Your Code
   ↓
GitHub (Push)
   ↓
GitHub Actions (Test & Build)
   ↓
Docker Hub (Store Images)
   ↓
Render (Deploy)
   ↓
Live Website 🌐
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     YOU - Local Development                      │
│                                                                   │
│  1. Write code                                                   │
│  2. Test locally: docker build . && docker run -p 8501:8501 .   │
│  3. Commit: git commit -m "message"                             │
│  4. Push: git push origin main                                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ↓
        ┌──────────────────────────────────────┐
        │   GITHUB REPOSITORY                  │
        │   (Your code is now here)            │
        │   Triggers webhook...                │
        └──────────────┬───────────────────────┘
                       │
        ┌──────────────↓───────────────────────┐
        │  GITHUB ACTIONS (CI/CD Pipeline)    │
        │  ================================    │
        │                                      │
        │  JOB 1: TEST                        │
        │  ├─ Checkout code ✓                │
        │  ├─ Install Python 3.13 ✓          │
        │  ├─ Install dependencies ✓         │
        │  └─ Run tests ✓                    │
        │                                     │
        │  JOB 2: BUILD (if test passes)     │
        │  ├─ Build Docker image             │
        │  ├─ Push to Docker Hub             │
        │  └─ Create registry entry          │
        │                                     │
        │  JOB 3: DEPLOY (if build succeeds) │
        │  ├─ Trigger Render webhook         │
        │  └─ Signal deployment              │
        └──────────┬─────────┬─────────┬─────┘
                   │         │         │
        ┌──────────↓─┐   ┌──↓────┐   ┌↓──────────┐
        │ DOCKER HUB │   │ LOGS  │   │ Artifacts │
        └─────┬──────┘   └───────┘   └───────────┘
              │
        ┌─────↓──────────────────────┐
        │  RENDER (Hosting)           │
        │  ======================    │
        │                              │
        │  1. Gets alert from GitHub  │
        │  2. Pulls Docker image      │
        │  3. Loads secrets from .env │
        │  4. Starts container        │
        │  5. Health check passes ✓   │
        │                              │
        │  YOUR APP IS LIVE! 🎉      │
        └─────┬──────────────────────┘
              │
        ┌─────↓──────────────────────┐
        │  PRODUCTION                 │
        │                              │
        │  URL: https://job-recomm... │
        │  Users can now access:      │
        │  - Upload PDFs              │
        │  - Get job recommendations  │
        │  - Apply for jobs           │
        └─────────────────────────────┘
```

---

## Components Explained 🧩

### 1. **You (Local Machine)**
- Write code in VS Code
- Test locally with Docker
- Push to GitHub

### 2. **GitHub**
- Stores your code
- Runs automated workflows
- Tracks all changes

### 3. **GitHub Actions**
- Runs on GitHub's servers
- Executes workflow automatically
- Tests, builds, deploys

### 4. **Docker Hub**
- Public registry for Docker images
- Stores your app image
- Free storage for public images

### 5. **Render**
- Cloud hosting platform
- Runs your Docker container
- Provides live URL
- 24/7 uptime (paid tier)

---

## Files Created 📁

```
Job_Recommender/
├── app.py                          # Your Streamlit app (unchanged)
├── requirements.txt                # Dependencies (unchanged)
├── Dockerfile                      # NEW: Container instructions
├── .dockerignore                   # NEW: Files to skip building
├── .env.example                    # NEW: Secrets template
├── .github/
│   └── workflows/
│       └── deploy.yml             # NEW: GitHub Actions workflow
├── CI_CD_GUIDE.md                 # NEW: Complete detailed guide
├── QUICKSTART.md                  # NEW: Quick start (read first!)
└── TROUBLESHOOTING.md             # NEW: Common issues & fixes
```

---

## What Each File Does 🔧

| File | Purpose | When Modified |
|------|---------|--------------|
| `Dockerfile` | Tells Docker how to build your app | When dependencies change |
| `.dockerignore` | Like .gitignore for Docker | Rarely |
| `.env.example` | Shows what secrets are needed | When adding new API keys |
| `.github/workflows/deploy.yml` | Automation instructions | To change deployment process |
| `requirements.txt` | Python packages needed | When adding libraries |

---

## Step-by-Step Timeline 📅

### Day 1: Setup (30 minutes)
1. Create GitHub account
2. Create DockerHub account
3. Push code to GitHub
4. Add GitHub secrets
5. Deploy to Render

### Day 2+: Automatic Magic
```
You make changes → Push to GitHub → Auto test → Auto build → Auto deploy
```

---

## Security Flow 🔐

```
┌────────────────────────────────────┐
│ Secrets (Never stored in code)     │
│                                    │
│ GROQ_API_KEY                       │
│ APIFY_TOKEN                        │
│ DOCKERHUB_PASSWORD                │
└────────┬───────────────────────────┘
         │
     ┌───↓────────────────────────┐
     │  GitHub Secrets (Encrypted)│
     │  ├─ Accessible in Actions  │
     │  └─ Masked in logs         │
     └───┬────────────────────────┘
         │
     ┌───↓────────────────────────┐
     │ Render Env Variables       │
     │ ├─ Loaded at runtime       │
     │ └─ Never leave container   │
     └────────────────────────────┘
```

---

## Failure Recovery 🛡️

```
If Test Fails:
├─ Workflow stops (no deploy) ✓
├─ You get notified on GitHub
└─ Fix and push again

If Build Fails:
├─ Workflow stops (no deploy) ✓
├─ Check logs
└─ Fix Dockerfile and push

If Deploy Fails:
├─ Old version stays live ✓
├─ Check Render logs
└─ Fix and trigger redeploy
```

---

## Performance Metrics ⚡

| Operation | Time | Notes |
|-----------|------|-------|
| Test | 1-2 min | Python setup + imports |
| Build | 10-15 min | First time (cached after) |
| Push to Docker Hub | 2-3 min | Depends on image size |
| Deploy to Render | 2-5 min | Container start + health check |
| **Total First Time** | **~15-20 min** | Subsequent: ~5-8 min |

---

## Costs 💰

| Service | Cost | Notes |
|---------|------|-------|
| GitHub | FREE | Unlimited public/private repos |
| DockerHub | FREE | Public images |
| Render | FREE/PAID | Free: suspends after 15 min inactivity |
| Total/Month | ~$0-7 | Just Render paid tier if you want 24/7 |

---

## Next Improvements 🚀

Once you have basic CI/CD working:

1. **Add unit tests**
   ```python
   # tests/test_helper.py
   def test_extract_text():
       assert result == expected
   ```

2. **Add code coverage**
   ```yaml
   - pytest --cov
   ```

3. **Deploy to multiple environments**
   - Staging (test)
   - Production (live)

4. **Custom domain**
   - `https://job-recommender.com`

5. **Monitoring & alerts**
   - Uptime tracking
   - Error notifications

6. **Database backups**
   - If you add a database

---

## Quick Reference 🎯

### To Make Changes Live:
```powershell
git add .
git commit -m "Your message"
git push origin main
# Wait 15-20 minutes, app updates automatically
```

### To Check Status:
1. GitHub → Actions tab
2. Render → Your service → Deployment
3. Live app → https://your-render-url.onrender.com

### To Debug:
1. GitHub Actions logs → See what failed
2. Render logs → See runtime errors
3. TROUBLESHOOTING.md → Find solution

---

## Congratulations! 🎉

You now have:
- ✅ Professional CI/CD pipeline
- ✅ Automated testing
- ✅ Automated deployment
- ✅ Zero manual intervention
- ✅ Production-ready app

This is what enterprise teams use! 🚀

