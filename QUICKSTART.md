# 🚀 CI/CD Quick Start - 5 Minutes Setup

## What I've Created For You ✨

I've created all the necessary files for CI/CD deployment:

| File | Purpose |
|------|---------|
| `Dockerfile` | Instructions to create a container |
| `.dockerignore` | Tells Docker what files to skip |
| `.env.example` | Template for environment variables |
| `.github/workflows/deploy.yml` | Automated deployment instructions |
| `CI_CD_GUIDE.md` | Complete detailed guide |

---

## 🎯 DO THIS FIRST (Today!)

### Step 1: Create GitHub Account (2 min)
- Go to https://github.com
- Sign up for free
- Verify email

### Step 2: Push Code to GitHub (3 min)

Open PowerShell in your project folder:

```powershell
cd g:\Job_Recommeder

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/job_recommender.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## 🐳 DO THIS SECOND (Today!)

### Step 3: Create DockerHub Account (2 min)
- Go to https://hub.docker.com
- Sign up (free)
- Create access token: Settings → Security → New Access Token
- Name it: `github-actions`
- Copy the token (keep it safe!)

### Step 4: Add GitHub Secrets (2 min)

Go to: **GitHub** → Your Repo → **Settings** → **Secrets and variables** → **Actions**

Click "New repository secret" and add:

| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_PASSWORD` | Your DockerHub access token (from Step 3) |

---

## ☁️ DO THIS THIRD (Today!)

### Step 5: Deploy to Render (5 min)

1. Go to https://render.com
2. Click "Sign up" → Choose "GitHub"
3. Authorize GitHub access
4. Click "New +" → "Web Service"
5. Select your GitHub repo (`job_recommender`)
6. Configuration:
   - **Name:** `job-recommender`
   - **Environment:** Docker
   - **Instance Type:** Free
7. Click "Create Web Service"
8. **Wait 5-10 minutes** for first deployment

**Your app will be live at:** `https://job-recommender-xxxxx.onrender.com`

---

## 🔐 ADD YOUR SECRETS TO RENDER (5 min)

In Render dashboard, go to your service:

1. **Settings** → **Environment**
2. Add these variables:
   - `GROQ_API_KEY` = Your Groq API key
   - `APIFY_TOKEN` = Your Apify token
3. Click "Save Changes"
4. App will restart automatically

---

## ✅ VERIFY IT WORKS

After completing all steps:

1. Visit your live app: `https://job-recommender-xxxxx.onrender.com`
2. Go to GitHub → **Actions** tab
3. You should see workflow running (green ✓)

---

## 📝 WHAT HAPPENS NEXT

Every time you push code:

```powershell
git add .
git commit -m "Your changes"
git push origin main
```

**Automatically:**
1. ✅ Tests run (GitHub Actions)
2. ✅ Docker image built
3. ✅ Pushed to DockerHub
4. ✅ Deployed to Render
5. ✅ Live app updated

**Total time: ~2 minutes** ⏱️

---

## 🆘 COMMON ISSUES

### "Poetry lock not found"
- You're using `pyproject.toml` - this is fine!
- Docker builds work with it

### "App crashes after deployment"
- Check Render logs
- Make sure secrets are added in Render dashboard

### "GitHub Actions fails"
- Check Actions tab → See error logs
- Most common: Missing secrets in GitHub

### "Docker build takes forever"
- First build always takes longer (10 min)
- Subsequent builds are cached (<1 min)

---

## 📚 NEED MORE HELP?

See `CI_CD_GUIDE.md` for complete detailed guide (all concepts explained).

---

## 🎉 YOU'RE DONE!

Once you complete all steps, you have:
- ✅ Automated testing
- ✅ Automated building
- ✅ Automated deployment
- ✅ Zero manual steps

**Congrats on setting up professional CI/CD!** 🚀

