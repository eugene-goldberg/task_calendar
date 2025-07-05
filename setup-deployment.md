# Quick Deployment Setup Guide

## Prerequisites Installation

### 1. Install Render CLI

```bash
# macOS/Linux
curl -L https://github.com/render-oss/cli/releases/latest/download/render-darwin-amd64 -o render
chmod +x render
sudo mv render /usr/local/bin/

# Or download from: https://github.com/render-oss/cli/releases
```

### 2. Install Supabase CLI (Optional - for local testing)

```bash
# macOS
brew install supabase/tap/supabase

# Linux
brew install supabase/tap/supabase

# Or via NPM
npm install -g supabase
```

## Step-by-Step Deployment

### Step 1: Create Supabase Database

1. Go to [supabase.com](https://supabase.com)
2. Sign up/Login
3. Click "New Project"
4. Choose a name and password
5. Select a region (choose closest to your users)
6. Wait for project to initialize

### Step 2: Get Database Connection String

1. In Supabase Dashboard, go to Settings → Database
2. Copy the "Connection string" (URI tab)
3. Replace `[YOUR-PASSWORD]` with your database password
4. Save it securely

### Step 3: Prepare Your Project

```bash
# Make deployment script executable
chmod +x deploy-render.sh

# Set environment variable
export SUPABASE_DB_URL='your-connection-string-here'

# Initialize database (run migration)
python migrate_data.py
```

### Step 4: Deploy to Render

```bash
# Login to Render
render login

# Run deployment
./deploy-render.sh
```

## Alternative: Manual Render Setup

If you prefer the web interface:

1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: calendar-app
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `DATABASE_URL`: Your Supabase connection string
   - `PYTHON_VERSION`: 3.12.0
   - `ENVIRONMENT`: production
7. Click "Create Web Service"

## Post-Deployment

### Verify Deployment

```bash
# Check service status
render services

# View logs
render logs --tail

# Get service URL
render services list
```

### Initialize Database

Once deployed, you need to create the database tables:

```bash
# SSH into Render service (if needed)
render ssh

# Run database initialization
python database.py
```

## Monitoring

- **Render Dashboard**: https://dashboard.render.com
- **Supabase Dashboard**: https://app.supabase.com
- Check application logs regularly
- Monitor database usage in Supabase

## Troubleshooting

### Common Issues:

1. **Database Connection Error**
   - Verify DATABASE_URL is set correctly
   - Check Supabase project is active

2. **Module Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version matches runtime.txt

3. **Port Binding Error**
   - Make sure to use `$PORT` environment variable
   - Don't hardcode port numbers

### Debug Commands:

```bash
# View environment variables
render env

# Check deployment status
render deploys list

# Access service shell
render ssh
```

## Free Tier Limitations

Remember:
- **Render**: Services spin down after 15 minutes of inactivity
- **Supabase**: Project pauses after 7 days of inactivity
- Both can be reactivated from their dashboards