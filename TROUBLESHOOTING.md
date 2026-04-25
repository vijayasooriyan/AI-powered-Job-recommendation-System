# 🔧 Troubleshooting Guide - Common Issues & Solutions

## Testing & Building Issues

### ❌ "Docker image build fails"

**Error:** `ERROR: failed to solve with frontend dockerfile.v0`

**Solution:**
1. Check your `Dockerfile` syntax - look for extra spaces or typos
2. Test locally first:
   ```powershell
   docker build -t job-recommender .
   ```
3. If that fails, check:
   - All dependencies are in `requirements.txt`
   - Python version is correct
   - No special characters in paths

---

### ❌ "Requirements.txt not found"

**Error:** `COPY requirements.txt: file not found`

**Solution:**
- Make sure `requirements.txt` exists in project root
- If using `pyproject.toml`, generate requirements:
  ```powershell
  pip install pipreqs
  pipreqs . --force
  ```

---

### ❌ "GitHub Actions test fails"

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
1. Check `requirements.txt` has all dependencies
2. Test locally:
   ```powershell
   pip install -r requirements.txt
   ```
3. If still fails, update it:
   ```powershell
   pip freeze > requirements.txt
   ```

---

## Docker & Deployment Issues

### ❌ "Cannot login to Docker Hub"

**Error:** `Error response from daemon: Get "https://registry-1.docker.io/v2/": denied`

**Solution:**
1. Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD` secrets are correct
2. Check secrets in GitHub → Settings → Secrets
3. Test DockerHub login locally:
   ```powershell
   docker login --username YOUR_USERNAME
   ```
4. If login fails in browser, reset password at hub.docker.com

---

### ❌ "Docker image push fails"

**Error:** `denied: requested access to the resource is denied`

**Solution 1:** Check if repository exists on DockerHub
```powershell
# Create repo manually at https://hub.docker.com
# Then push to: docker tag local_image YOUR_USERNAME/job-recommender
```

**Solution 2:** Make sure username matches exactly (case-sensitive)

---

### ❌ "Render deployment shows blank page"

**Error:** App runs but shows "Streamlit is loading..."

**Solution:**
1. Check Render logs: Dashboard → Your Service → Logs
2. Most common issue: Missing environment variables
   - Go to Render → Settings → Environment
   - Add all required variables:
     - `GROQ_API_KEY`
     - `APIFY_TOKEN`
3. Click "Save Changes" to trigger restart
4. Wait 2-3 minutes for restart

---

### ❌ "Port 8501 is already in use"

**Error:** `Port 8501 is already in use`

**Solution (Local Testing):**
```powershell
# Stop any running Docker containers
docker stop $(docker ps -q)

# Or run on different port
docker run -p 8502:8501 job-recommender
```

---

## GitHub Actions Issues

### ❌ "Workflow not running"

**Error:** No workflow appears in Actions tab

**Solution:**
1. Check `.github/workflows/deploy.yml` path is correct
2. Verify file is committed to `main` branch:
   ```powershell
   git add .github/
   git commit -m "Add workflows"
   git push origin main
   ```
3. Go to repo → Actions → Check if workflows appear
4. If still not visible: 
   - Repo settings → Actions → Enabled

---

### ❌ "Secrets not being recognized"

**Error:** `${{ secrets.DOCKERHUB_PASSWORD }}` appears in logs (not masked)

**Solution:**
1. Secrets are case-sensitive! Check exact spelling:
   - ✅ `DOCKERHUB_PASSWORD` 
   - ❌ `dockerhub_password`
   - ❌ `DOCKERHUB_password`
2. Delete and re-add the secret
3. Wait 1-2 minutes after adding

---

### ❌ "Workflow passes locally but fails on GitHub"

**Error:** Works with `docker build` but fails on GitHub Actions

**Solution:**
1. Your local environment is different from GitHub's
2. Add this to debug:
   ```yaml
   - name: Debug info
     run: |
       python --version
       which python
       pip list
   ```
3. Check if you need to install system dependencies:
   ```dockerfile
   RUN apt-get update && apt-get install -y \
       specific-dependency \
       && rm -rf /var/lib/apt/lists/*
   ```

---

## Environment Variables & Secrets

### ❌ "API key not found at runtime"

**Error:** `GROQ_API_KEY not found` or similar

**Solution 1 (Local Testing):**
```powershell
# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env

# Load it
$env:GROQ_API_KEY="your_key_here"
```

**Solution 2 (Render):**
1. Go to Render → Your Service → Settings → Environment
2. Add the variable
3. Click Save
4. Service automatically restarts

**Solution 3 (Docker Local):**
```powershell
docker run -e GROQ_API_KEY="your_key" -p 8501:8501 job-recommender
```

---

### ❌ "Secret shows in GitHub logs"

**Error:** Your API key is exposed in logs!

**Solution (Immediate):**
1. Rotate/regenerate the key immediately
2. Remove from all logs
3. GitHub's secret masking should catch it, but act fast

**Prevention:**
- Never commit `.env` 
- Always use GitHub Secrets
- Never print `${{ secrets.XXX }}` to stdout

---

## Git & GitHub Issues

### ❌ "Git authentication fails"

**Error:** `remote: Permission to user/repo.git denied to user`

**Solution:**
1. Setup GitHub personal access token:
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` scope
2. Use token as password when git asks
3. Or use SSH keys (advanced)

---

### ❌ "Cannot push to GitHub"

**Error:** `fatal: 'origin' does not appear to be a 'git' repository`

**Solution:**
```powershell
# Check remote is set
git remote -v

# If empty, add it
git remote add origin https://github.com/YOUR_USER/job_recommender.git

# Then push
git push -u origin main
```

---

### ❌ "Files already tracked won't update"

**Error:** `.env` still appears in commits even though in `.gitignore`

**Solution:**
```powershell
# Remove from git (don't delete file)
git rm --cached .env

# Update .gitignore
echo ".env" >> .gitignore

# Commit
git commit -m "Remove .env from tracking"
git push origin main
```

---

## Performance & Optimization

### ⚠️ "Build takes too long"

**Expected times:**
- First build: 10-15 minutes (all layers built)
- Subsequent builds: 1-2 minutes (cached)

**Speed it up:**
1. Use Docker layer caching (already in our workflow)
2. Reduce image size by cleaning up:
   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```
3. Use `.dockerignore` properly (already done)

---

### ⚠️ "Container uses too much RAM"

**Solution:**
1. Render free tier has limited memory - this might be normal
2. For Streamlit, need at least 512MB
3. If repeatedly crashing, upgrade to paid tier or use AWS

---

## Render-Specific Issues

### ❌ "Render keeps showing 'Building...'"

**Error:** Service stuck in building state

**Solution:**
1. Check Render logs for errors
2. Click "Clear cache & deploy" in service settings
3. If still stuck, delete and recreate service

---

### ❌ "Render URL shows Streamlit but app not working"

**Error:** App loads but features broken

**Solution:**
1. Check environment variables added correctly
2. Check Render logs for Python errors
3. Verify Docker port is 8501
4. Try manual redeploy: Service → Manual Deploy

---

### ❌ "Free tier suspended"

**Error:** App shows "Service suspended" after inactivity

**Solution:**
- Free tier on Render auto-suspends after 15 minutes of inactivity
- Click "Refresh" button or upgrade to paid ($7/month minimum)
- Paid tier runs 24/7

---

## Quick Debugging Checklist

When something fails, check in this order:

1. **GitHub Actions Logs**
   - GitHub → Actions tab → Failed workflow → Click for details

2. **Render Logs**
   - Render → Your Service → Logs tab

3. **Local Testing**
   ```powershell
   docker build .
   docker run -p 8501:8501 -e GROQ_API_KEY="test" .
   ```

4. **Requirements Check**
   All dependencies in `requirements.txt`? Missing one?

5. **Secrets Check**
   All secrets in GitHub? All secrets in Render dashboard?

6. **File Check**
   - `Dockerfile` exists?
   - `.github/workflows/deploy.yml` exists?
   - Both committed to `main`?

---

## Still Stuck?

1. Check logs carefully - they usually have the answer
2. Google the error message
3. GitHub Discussions → Ask community
4. Render Support: https://render.com/support

Remember: Most issues are either:
- Missing environment variables ❌
- Wrong secret names ❌
- File not found ❌
- Dependencies not in requirements.txt ❌

