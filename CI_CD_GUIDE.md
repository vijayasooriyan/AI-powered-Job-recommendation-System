# Complete CI/CD Deployment Guide for AI Job Recommender

## What is CI/CD? 🎯

**CI (Continuous Integration)**: Automatically test your code when you push changes
**CD (Continuous Deployment)**: Automatically deploy tested code to production

Think of it like a robot that:
1. Watches your code for changes
2. Tests if everything works
3. Deploys to the server automatically

---

## STEP-BY-STEP SETUP

### STEP 1: Prepare Your Repository 📁

#### 1A. Create GitHub Account (if you don't have one)
- Go to https://github.com
- Sign up for free
- Verify your email

#### 1B. Create a new GitHub Repository
- Click "+" → "New repository"
- Name it: `job_recommender` (or your choice)
- Choose "Private" or "Public"
- Don't initialize with README (we'll upload our code)
- Click "Create repository"

#### 1C. Upload Your Code to GitHub
Open PowerShell in your project folder and run:

```powershell
cd g:\Job_Recommeder

# Initialize git
git init

# Add all files
git add .

# Commit your files
git commit -m "Initial commit: Project setup"

# Add remote (copy the URL from your GitHub repo page)
git remote add origin https://github.com/YOUR_USERNAME/job_recommender.git

# Upload to GitHub
git branch -M main
git push -u origin main
```

---

### STEP 2: Prepare Your Code for CI/CD 🔧

#### 2A. Create `.dockerignore` file
Create this file in your project root:

```
__pycache__/
*.pyc
.git
.gitignore
.env
.venv
venv/
*.egg-info/
.pytest_cache/
```

#### 2B. Update `.env.example` (for secrets)
Create this file to show what secrets are needed:

```
GROQ_API_KEY=your_groq_key_here
APIFY_TOKEN=your_apify_token_here
```

**⚠️ IMPORTANT**: Never commit `.env` with real keys!

#### 2C. Create `requirements.txt` (if not already good)
Make sure it exists and is up-to-date:

```
streamlit>=1.56.0
pymupdf>=1.27.2.2
python-dotenv>=1.2.2
apify-client>=2.5.0
groq>=1.1.2
```

---

### STEP 3: Create a Dockerfile 🐳

Create a file named `Dockerfile` in your project root:

```dockerfile
# Step 1: Use Python 3.13 base image
FROM python:3.13-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy project files into container
COPY . /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Set environment variables
ENV PYTHONUNBUFFERED=1

# Step 6: Expose port for Streamlit
EXPOSE 8501

# Step 7: Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**What does this do?**
- Creates a container (like a lightweight virtual machine)
- Installs your Python dependencies
- Runs your Streamlit app

---

### STEP 4: Create GitHub Actions Workflow 🚀

#### 4A. Create workflow directory
```powershell
mkdir -p .github/workflows
```

#### 4B. Create deployment workflow file
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

# Trigger: When you push to 'main' branch
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  # JOB 1: Test the code
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python 3.13
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest

      - name: Run basic import tests
        run: |
          python -c "import streamlit; print('Streamlit works!')"
          python -c "import pymupdf; print('PyMuPDF works!')"

  # JOB 2: Build and push Docker image
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKERHUB_USERNAME }}/job-recommender:latest
            ${{ secrets.DOCKERHUB_USERNAME }}/job-recommender:${{ github.sha }}
          cache-from: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/job-recommender:buildcache
          cache-to: type=registry,ref=${{ secrets.DOCKERHUB_USERNAME }}/job-recommender:buildcache,mode=max

  # JOB 3: Deploy to Render or Heroku
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to Render
        run: |
          curl https://api.render.com/deploy/${{ secrets.RENDER_DEPLOY_HOOK_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

**What this does:**
- Tests your code when you push
- Builds a Docker image
- Pushes it to DockerHub
- Deploys to Render automatically

---

### STEP 5: Set Up GitHub Secrets 🔐

These are values GitHub keeps safe (like passwords).

#### 5A. Go to GitHub Repository Settings
1. Go to your GitHub repo
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"

#### 5B. Add these secrets:

| Secret Name | Where to get it |
|-------------|-----------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username (free account at hub.docker.com) |
| `DOCKERHUB_PASSWORD` | Your DockerHub password |
| `RENDER_DEPLOY_HOOK_ID` | From Render dashboard (see Step 6) |
| `RENDER_API_KEY` | From Render dashboard (see Step 6) |
| `GROQ_API_KEY` | From your Groq account |
| `APIFY_TOKEN` | From your Apify account |

---

### STEP 6: Create DockerHub Account 🐳

**Why?** To store your Docker images online

1. Go to https://hub.docker.com
2. Sign up (free)
3. Verify email
4. Create an access token:
   - Account Settings → Security → New Access Token
   - Name: `github-actions`
   - Copy the token
   - Add to GitHub Secrets as `DOCKERHUB_PASSWORD`

---

### STEP 7: Choose a Deployment Platform 🌐

#### Option A: RENDER (Easiest for Streamlit) ⭐ RECOMMENDED

**What is Render?**
- Free tier available
- Perfect for Streamlit apps
- Automatic deploys from GitHub

**Setup Steps:**

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your GitHub repository
5. Configure:
   - Name: `job-recommender`
   - Environment: `Docker`
   - Instance Type: `Free` (sufficient for testing)
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Get your URL (like `https://job-recommender-xxxxx.onrender.com`)

**To set up auto-deploy:**

1. In Render dashboard, go to your service
2. Settings → Deploy Hook
3. Copy the hook URL
4. Add to GitHub Secrets:
   - `RENDER_DEPLOY_HOOK_ID`: Use the hook URL
   - `RENDER_API_KEY`: Generate from Account Settings

---

#### Option B: HEROKU (Alternative, limited free tier)

1. Go to https://www.heroku.com
2. Sign up
3. Create new app
4. Connect to GitHub
5. Enable automatic deploys

**Note:** Heroku's free tier is now limited. Consider Render instead.

---

#### Option C: AWS EC2 (More control, paid)

If you want full control over server:

1. Create AWS account
2. Launch EC2 instance
3. Install Docker
4. Pull image and run:
   ```bash
   docker pull dockerhub_username/job-recommender:latest
   docker run -p 8501:8501 dockerhub_username/job-recommender:latest
   ```

---

### STEP 8: Commit Everything to GitHub 📤

```powershell
cd g:\Job_Recommeder

# Add new files
git add Dockerfile .dockerignore .env.example .github/

# Commit
git commit -m "Add CI/CD pipeline and Docker support"

# Push to GitHub
git push origin main
```

**GitHub Actions will automatically:**
1. Run tests ✓
2. Build Docker image ✓
3. Push to DockerHub ✓
4. Deploy to Render ✓

---

### STEP 9: Monitor Your Deployment 📊

#### Check GitHub Actions:
1. Go to your repo
2. Click "Actions" tab
3. Watch the workflow run
4. See if each step passes ✓

#### Check Render:
1. Go to render.com dashboard
2. Click your service
3. View logs
4. Check if deployment successful

#### Visit Your Live App:
Open: `https://your-render-url.onrender.com`

---

## TROUBLESHOOTING 🆘

### Issue: Docker build fails

**Solution:** Check logs in GitHub Actions
```powershell
# Test locally first
docker build -t job-recommender .
docker run -it -p 8501:8501 job-recommender
```

### Issue: App crashes after deployment

**Solution:** Check Render logs for errors
- Most common: Missing environment variables
- Add `.env` variables in Render dashboard

### Issue: GitHub Actions not running

**Solution:** 
- Check `.github/workflows/deploy.yml` syntax
- Ensure it's committed to `main` branch
- Check repository has Actions enabled

### Issue: "Secrets not found"

**Solution:**
- Verify secret names exactly (case-sensitive)
- Re-add secrets if needed
- Wait a few minutes for propagation

---

## QUICK REFERENCE CHECKLIST ✅

- [ ] GitHub account created
- [ ] Repository created and code pushed
- [ ] `.dockerignore` created
- [ ] `.env.example` created
- [ ] `Dockerfile` created
- [ ] `.github/workflows/deploy.yml` created
- [ ] DockerHub account created
- [ ] GitHub Secrets added
- [ ] Render account created
- [ ] Service deployed on Render
- [ ] App accessible at live URL

---

## WHAT HAPPENS NOW? 🔄

Every time you:
1. **Make changes** locally
2. **Push to GitHub**

Automatically:
1. ✅ Code is tested
2. ✅ Docker image is built
3. ✅ Image pushed to DockerHub
4. ✅ Deployed to Render
5. ✅ Live app updated

**No manual steps needed!** 🎉

---

## NEXT STEPS 🚀

- Monitor your deployments
- Write better tests
- Set up custom domain
- Add monitoring/alerting
- Optimize Docker image size

