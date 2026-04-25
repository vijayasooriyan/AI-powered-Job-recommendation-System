# AI Job Recommender - CI/CD Ready! 🚀

A Streamlit application that recommends job positions based on your resume and extracts job listings from LinkedIn and Naukri.

## Quick Links 📚

- **🚀 [START HERE: Quick Start Guide](QUICKSTART.md)** - 5-minute setup
- 📖 [Complete CI/CD Guide](CI_CD_GUIDE.md) - Detailed explanations
- 🏗️ [Architecture & Flow](ARCHITECTURE.md) - How it all works
- 🔧 [Troubleshooting Guide](TROUBLESHOOTING.md) - Fix common issues

---

## Features ✨

- 📄 **PDF Resume Parser** - Extract text and analyze your resume
- 🔍 **AI-Powered Matching** - Uses Groq AI to match jobs to your skills
- 💼 **Multi-Platform Job Scraping** - LinkedIn and Naukri job postings
- 🤖 **MCP Server** - Model Context Protocol support
- 🐳 **Docker Ready** - Containerized for easy deployment
- ⚙️ **CI/CD Automated** - GitHub Actions + Automatic deployment

---

## Tech Stack 🛠️

- **Frontend:** Streamlit
- **Backend:** Python 3.13
- **AI:** Groq API
- **Job Scraping:** Apify
- **Container:** Docker
- **Deployment:** Render
- **CI/CD:** GitHub Actions

---

## Local Setup (Development)

### Prerequisites
- Python 3.13+
- Docker (optional, for containerized testing)
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/job_recommender.git
cd job_recommender

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env

# Add your API keys to .env
# GROQ_API_KEY=your_key_here
# APIFY_TOKEN=your_token_here

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Deployment 📦

### Option 1: Render (Recommended - Easiest)

See [QUICKSTART.md](QUICKSTART.md) for step-by-step instructions.

Live URL: `https://job-recommender-xxxxx.onrender.com`

### Option 2: Docker Locally

```bash
# Build Docker image
docker build -t job-recommender .

# Run container
docker run -e GROQ_API_KEY="your_key" \
           -e APIFY_TOKEN="your_token" \
           -p 8501:8501 \
           job-recommender
```

### Option 3: AWS / Other Cloud (Advanced)

See [CI_CD_GUIDE.md](CI_CD_GUIDE.md#step-7-choose-a-deployment-platform) for alternatives.

---

## CI/CD Pipeline 🔄

Automated workflow on every push:

```
Push to GitHub 
   ↓
Test Code (GitHub Actions)
   ↓ 
Build Docker Image
   ↓
Push to Docker Hub
   ↓
Deploy to Render
   ↓
Live! ✓
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete flow diagrams.

---

## Project Structure 📁

```
job_recommender/
├── app.py                  # Main Streamlit application
├── mcp_server.py          # MCP Server implementation
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions workflow
├── src/
│   ├── helper.py          # PDF extraction & AI
│   ├── job_api.py         # Job scraping
│   └── __init__.py
└── docs/
    ├── QUICKSTART.md      # Quick setup guide
    ├── CI_CD_GUIDE.md     # Detailed guide
    ├── ARCHITECTURE.md    # System design
    └── TROUBLESHOOTING.md # Problem solving
```

---

## Environment Variables 🔐

Create a `.env` file (copy from `.env.example`):

```env
GROQ_API_KEY=your_groq_api_key
APIFY_TOKEN=your_apify_token
OPENAI_API_KEY=optional_key
DEBUG=false
LOG_LEVEL=INFO
```

**Never commit `.env` with real secrets!**

---

## API Keys Setup 🔑

### 1. Groq API Key
1. Go to https://groq.com
2. Sign up / Login
3. Create API key
4. Add to `.env`

### 2. Apify Token
1. Go to https://apify.com
2. Sign up / Login
3. Create token in settings
4. Add to `.env`

---

## Usage 💡

1. Upload your resume (PDF)
2. Enter job preferences
3. Click "Find Jobs"
4. View AI-recommended matches
5. Click "Apply" to open job posting

---

## Troubleshooting 🆘

### Common Issues

**App won't start locally:**
```bash
pip install --upgrade streamlit
streamlit run app.py
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Environment variables not loading:**
```bash
# Make sure .env file exists and has correct values
python -c "from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"
```

**Deployment issues:**
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for comprehensive solutions.

---

## Git Workflow 🌳

First deployment:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/job_recommender.git
git push -u origin main
```

Subsequent updates:
```bash
git add .
git commit -m "Your message"
git push origin main
# Automatic deployment starts!
```

---

## Manual Deployment

If CI/CD is not set up:

```bash
# Build and run locally
docker build -t job-recommender .
docker run -p 8501:8501 -it job-recommender

# Or deploy directly to Render
# See CI_CD_GUIDE.md for manual steps
```

---

## Monitoring 📊

### Check Deployment

**GitHub Actions:**
- GitHub → Your Repo → Actions → See workflows run

**Render:**
- render.com → Your Service → Logs tab
- Real-time logs and errors

**Live App:**
- Visit your Render URL
- Test functionality

---

## Contributing 🤝

1. Fork the repository
2. Create feature branch: `git checkout -b feature/name`
3. Commit changes: `git commit -m "Description"`
4. Push branch: `git push origin feature/name`
5. Create Pull Request

---

## License 📄

MIT License - See LICENSE file for details

---

## Support 💬

- 📖 Read [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for detailed help
- 🔧 Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- 🏗️ Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- 💬 Create GitHub Issue for bugs

---

## Learning Resources 🎓

- [Streamlit Documentation](https://docs.streamlit.io)
- [Docker Guide](https://docker.com)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Render Documentation](https://render.com/docs)

---

## Roadmap 🗺️

- [ ] Add database for job history
- [ ] User authentication
- [ ] Email notifications
- [ ] Advanced filtering options
- [ ] Mobile app support
- [ ] Integration with more job boards

---

## Status ✅

- ✅ Local development ready
- ✅ Docker containerization complete
- ✅ GitHub Actions CI/CD configured
- ✅ Deployment to Render ready
- ✅ Environment variables secured
- ✅ Documentation complete

---

**Get started now!** 🚀 → [QUICKSTART.md](QUICKSTART.md)

Last updated: April 2026
