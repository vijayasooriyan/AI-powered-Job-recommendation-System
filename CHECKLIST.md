# ✅ DEPLOYMENT CHECKLIST - Print or Bookmark This!

## PHASE 1: GITHUB SETUP (Today)

### Day 1 - Create Accounts (5 minutes)
- [ ] Visit https://github.com
- [ ] Sign up (free)
- [ ] Verify email
- [ ] Login to GitHub

### Day 1 - Create Repository (2 minutes)
- [ ] Click "+" → "New repository"
- [ ] Name: `job_recommender`
- [ ] Choose "Public" or "Private"
- [ ] Do NOT initialize with README
- [ ] Click "Create repository"
- [ ] Copy the repository URL

### Day 1 - Push Your Code (3 minutes)
```powershell
cd g:\Job_Recommeder
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git branch -M main
git push -u origin main
```
- [ ] Code successfully pushed to GitHub
- [ ] Verify files visible at github.com/username/job_recommender

---

## PHASE 2: DOCKER HUB SETUP (Today)

### Day 1 - Create DockerHub Account (2 minutes)
- [ ] Visit https://hub.docker.com
- [ ] Sign up (free)
- [ ] Verify email
- [ ] Login to DockerHub

### Day 1 - Generate Access Token (2 minutes)
- [ ] Account → Settings → Security
- [ ] "New Access Token"
- [ ] Name: `github-actions`
- [ ] Permissions: Read & Write
- [ ] Copy token (paste below)
- [ ] Token: `dckr_pat_92b1KTXPT_tL6NFiKv-9buF0pjY`

---

## PHASE 3: GITHUB SECRETS (Today)

### Day 1 - Add GitHub Secrets (2 minutes)
Go to: GitHub → Your Repo → Settings → Secrets and variables → Actions

Click "New repository secret" and add each:

#### Secret 1: DOCKERHUB_USERNAME
- [ ] Name: `DOCKERHUB_USERNAME`
- [ ] Value: `your_dockerhub_username`
- [ ] Click "Add Secret"

#### Secret 2: DOCKERHUB_PASSWORD  
- [ ] Name: `DOCKERHUB_PASSWORD`
- [ ] Value: `your_docker_hub_access_token_from_above`
- [ ] Click "Add Secret"

#### Secret 3: GROQ_API_KEY
- [ ] Go to https://groq.com
- [ ] Get your API key
- [ ] Name: `GROQ_API_KEY`
- [ ] Value: `your_groq_api_key`
- [ ] Click "Add Secret"

#### Secret 4: APIFY_TOKEN
- [ ] Go to https://apify.com
- [ ] Get your token
- [ ] Name: `APIFY_TOKEN`
- [ ] Value: `your_apify_token`
- [ ] Click "Add Secret"

✅ **Verification:**
- [ ] All 4 secrets added to GitHub
- [ ] Secrets are hidden (masked)

---

## PHASE 4: RENDER DEPLOYMENT (Today)

### Day 1 - Create Render Account (1 minute)
- [ ] Visit https://render.com
- [ ] Click "Sign up"
- [ ] Choose "Continue with GitHub"
- [ ] Authorize access
- [ ] Verify email

### Day 1 - Deploy Service (5 minutes)
- [ ] Render dashboard
- [ ] Click "New +" → "Web Service"
- [ ] Select your GitHub repo
- [ ] Configuration:
  - [ ] Name: `job-recommender`
  - [ ] Environment: `Docker`
  - [ ] Build Command: (leave blank)
  - [ ] Start Command: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
  - [ ] Instance Type: `Free`
- [ ] Click "Create Web Service"
- [ ] **Wait 10 minutes** for first deployment

### Day 1 - Note Your URL
- [ ] Your app URL: `https://job-recommender-3k1m.onrender.com`

---

## PHASE 5: ADD ENVIRONMENT VARIABLES TO RENDER (Today)

### Day 1 - Add Secrets to Render (3 minutes)
Go to: Render → Your Service → Settings → Environment

Click "Add Environment Variable" for each:

#### Variable 1: GROQ_API_KEY
- [ ] Key: `GROQ_API_KEY`
- [ ] Value: `your_groq_key`
- [ ] Save

#### Variable 2: APIFY_TOKEN
- [ ] Key: `APIFY_TOKEN`
- [ ] Value: `your_apify_token`
- [ ] Save

- [ ] Service auto-restarts
- [ ] Check Logs tab for any errors

---

## PHASE 6: VERIFY EVERYTHING WORKS (Today)

### Day 1 - Check GitHub Actions
- [ ] Go to GitHub repo
- [ ] Click "Actions" tab
- [ ] You should see 1 workflow run
- [ ] Check if it says ✅ (green) or ❌ (red)
- [ ] If red: Click on it and read error logs

### Day 1 - Check Render Deployment
- [ ] Go to Render dashboard
- [ ] Click your service
- [ ] Look at "Logs" tab
- [ ] Should see deployment logs
- [ ] Should say "Successfully deployed!"

### Day 1 - Visit Your Live App! 🎉
- [ ] Copy your Render URL from Phase 4
- [ ] Paste into browser
- [ ] App should load
- [ ] Try uploading a PDF
- [ ] Try searching for jobs
- [ ] Test all features

---

## PHASE 7: FUTURE UPDATES (Next time you change code)

### Standard Workflow (Each time)
```powershell
# Make changes to your code
git add .
git commit -m "Your change description"
git push origin main

# Then:
# 1. GitHub Actions auto-tests ✓
# 2. Builds Docker image ✓
# 3. Pushes to Docker Hub ✓
# 4. Triggers Render deployment ✓
# 5. App updates automatically ✓
```

- [ ] Code committed and pushed
- [ ] Check GitHub Actions (should be running)
- [ ] Wait 15-20 minutes for full deployment
- [ ] Refresh live app to see changes

---

## 🆘 TROUBLESHOOTING CHECKS

If something fails:

### If GitHub Actions shows ❌
- [ ] Check error message in Actions log
- [ ] Common: Missing secrets (add them!)
- [ ] Common: Wrong secret names (case-sensitive!)
- [ ] See TROUBLESHOOTING.md for solutions

### If Render shows error
- [ ] Check Render Logs tab
- [ ] Most common: Missing environment variables
- [ ] Click "Settings" → "Environment" → Add variables
- [ ] Service auto-restarts after saving

### If app doesn't load
- [ ] Try different browser
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Check Render logs for Python errors
- For more help → TROUBLESHOOTING.md

---

## 📋 FINAL VERIFICATION

Before you declare victory:

- [ ] GitHub repository has your code
- [ ] GitHub secrets configured (4 total)
- [ ] Docker image in DockerHub
- [ ] Render service deployed
- [ ] Render environment variables set
- [ ] GitHub Actions all passing ✓
- [ ] Live app accessible at URL
- [ ] App features working
- [ ] Can upload PDF
- [ ] Can search jobs

---

## 🎉 SUCCESS!

If all checks are marked ✅, you have:
- ✅ Professional CI/CD pipeline
- ✅ Automated testing
- ✅ Automated deployment
- ✅ Live, working application
- ✅ Zero manual deployment steps

---

## 📞 QUICK HELP LINKS

| Problem | Solution |
|---------|----------|
| "How do I get started?" | Read QUICKSTART.md |
| "What even is CI/CD?" | Read CI_CD_GUIDE.md |
| "I'm stuck on step X" | Check TROUBLESHOOTING.md |
| "Show me a diagram" | See ARCHITECTURE.md |
| "What's deployed?" | Visit your Render URL |
| "How do I update the app?" | `git push origin main` |

---

## 🚀 NEXT STEPS

1. **Print this checklist** (or bookmark it)
2. **Follow each step in order**
3. **Check off as you complete**
4. **Ask for help if stuck**
5. **Celebrate when done!** 🎉

---

**Time to completion: ~30 minutes** ⏱️

**Ready?** Start with QUICKSTART.md!
