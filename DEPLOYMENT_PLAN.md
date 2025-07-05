# Calendar App Deployment Plan

## Overview

This document outlines the deployment strategy for the FastAPI calendar application with PostgreSQL database. Due to Heroku's removal of free tiers, we'll provide options for both Heroku (paid) and alternative free platforms.

## Option 1: Heroku Deployment (Paid - ~$14/month)

### Prerequisites
- Heroku CLI installed
- Heroku account with payment method added
- Git repository set up

### Cost Breakdown
- **Dyno**: Basic dyno ($7/month)
- **PostgreSQL**: Essential-0 plan ($5/month)
- **Total**: ~$12-14/month

### Deployment Steps

#### 1. Prepare Application Files

Create `Procfile` in the root directory:
```
web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Create `runtime.txt`:
```
python-3.12.0
```

Update `requirements.txt` to include all dependencies.

#### 2. Environment Configuration

Create a production-ready configuration that reads from environment variables:

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL will be automatically set by Heroku
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Fix for Heroku's postgres:// vs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
```

#### 3. Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create new Heroku app
heroku create your-calendar-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:essential-0

# Deploy
git push heroku main

# Run database initialization
heroku run python database.py

# Open the app
heroku open
```

## Option 2: Render + Supabase (Free Tier)

### Overview
- **Render**: Free web service hosting (with limitations)
- **Supabase**: Free PostgreSQL database (500MB)

### Deployment Steps

#### 1. Database Setup on Supabase

1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get database connection string from Settings > Database
4. Update `.env` with Supabase connection string

#### 2. Deploy to Render

1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Create new Web Service
4. Configure:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `DATABASE_URL`: Your Supabase connection string
   - `PYTHON_VERSION`: 3.12.0

### Limitations
- Render free tier: Spins down after 15 minutes of inactivity
- Supabase free tier: Project pauses after 7 days of inactivity

## Option 3: Railway Deployment (Trial Credits)

### Overview
- $5 trial credits (one-time)
- After credits, starts at $5/month
- Includes both app hosting and PostgreSQL

### Deployment Steps

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Get deployment URL
railway open
```

## Recommended Production Configuration

### 1. Security Updates

Update `main.py` for production:
```python
# Configure CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app-name.herokuapp.com",
        "https://your-custom-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. Database Migrations

Set up Alembic for database migrations:
```bash
# Initialize Alembic
alembic init alembic

# Create first migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

### 3. Environment Variables

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: For session management (if needed)
- `ENVIRONMENT`: production/development

### 4. Static File Serving

For production, consider using WhiteNoise:
```bash
pip install whitenoise
```

Update `main.py`:
```python
from whitenoise import WhiteNoise

app = FastAPI()
app.mount("/static", WhiteNoise(app, root="static/"), name="static")
```

## Post-Deployment Checklist

- [ ] Verify database connection
- [ ] Test all CRUD operations
- [ ] Check static file serving
- [ ] Verify CORS settings
- [ ] Set up monitoring (e.g., UptimeRobot)
- [ ] Configure custom domain (optional)
- [ ] Set up SSL certificate (automatic on most platforms)
- [ ] Create database backups schedule
- [ ] Set up error logging (e.g., Sentry)

## Monitoring and Maintenance

### Database Backups
- Heroku: Automatic daily backups on paid plans
- Supabase: Manual backups via dashboard
- Railway: Automatic backups

### Application Monitoring
- Use platform-provided metrics
- Set up external monitoring (UptimeRobot, Pingdom)
- Configure error tracking (Sentry, Rollbar)

## Cost Comparison

| Platform | App Hosting | Database | Total Monthly | Free Tier |
|----------|-------------|----------|---------------|-----------|
| Heroku | $7 | $5 | $12 | No |
| Render + Supabase | $0-7 | $0-25 | $0-32 | Yes (limited) |
| Railway | $5+ | Included | $5+ | Trial credits |
| Vercel + Supabase | $0-20 | $0-25 | $0-45 | Yes |

## Recommendation

For a production calendar app:
1. **Budget-conscious**: Start with Render + Supabase free tier
2. **Reliability-focused**: Use Heroku or Railway paid plans
3. **Growth-oriented**: Railway offers the best scaling path

The free tier options work well for personal projects or MVPs, but have limitations (cold starts, inactivity pauses) that may impact user experience.