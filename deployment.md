# Calendar App Deployment Guide - Step by Step

This guide will walk you through deploying your FastAPI calendar application using Render (for hosting) and Supabase (for PostgreSQL database).

## Prerequisites

- Git repository with your calendar app code
- Web browser
- Terminal/Command line access

## Step 1: Create Supabase Account and Database

### 1.1 Sign up for Supabase
1. Open your browser and go to **[https://supabase.com](https://supabase.com)**
2. Click **"Start your project"** (green button)
3. Sign up using either:
   - GitHub (recommended for developers)
   - Email and password

### 1.2 Create a New Project
Once logged in:

1. Click **"New Project"**
2. Fill in the project details:
   - **Organization**: Select or create one
   - **Project name**: `calendar-app` (or your preferred name)
   - **Database Password**: Choose a strong password and **SAVE IT** (you'll need this later)
   - **Region**: Choose the closest to your location
   - **Pricing Plan**: Free tier is fine

3. Click **"Create new project"**
4. Wait for the project to initialize (this takes 1-2 minutes)

**✅ When you see the project dashboard, move to Step 2**

---

## Step 2: Get Supabase Connection String

### 2.1 Navigate to Database Settings
1. In your Supabase project dashboard, click **"Settings"** (gear icon) in the left sidebar
2. Click **"Database"** in the settings menu

### 2.2 Copy the Connection String
1. Scroll down to **"Connection string"** section
2. Make sure **"URI"** tab is selected
3. You'll see a connection string like:
   ```
   postgresql://postgres.[your-project-ref]:[YOUR-PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
   ```
4. Click **"Copy"** button
5. **IMPORTANT**: Replace `[YOUR-PASSWORD]` with the database password you created in Step 1

### 2.3 Save the Connection String
Create a temporary text file and save your connection string. It should look like:
```
postgresql://postgres.abcdefghijklmnop:YourActualPassword123!@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**✅ Once you have your connection string saved, move to Step 3**

---

## Step 3: Install Render CLI

### 3.1 Download Render CLI

For **macOS** (Intel or Apple Silicon):
```bash
# In your terminal, run:
curl -L https://github.com/render-oss/cli/releases/latest/download/render-darwin-arm64 -o render
chmod +x render
sudo mv render /usr/local/bin/
```

For **Windows**:
1. Go to https://github.com/render-oss/cli/releases
2. Download `render-windows-amd64.exe`
3. Rename it to `render.exe`
4. Add it to your PATH or move to a directory in your PATH

### 3.2 Verify Installation
```bash
# Test if it's installed:
render --version
```

You should see something like: `render version 1.x.x`

**✅ If you see the version number, move to Step 4**

---

## Step 4: Create Render Account

### 4.1 Sign up for Render
1. Go to **[https://render.com](https://render.com)**
2. Click **"Get Started for Free"**
3. Sign up using:
   - GitHub (recommended - easier deployment)
   - GitLab
   - Google
   - Email

### 4.2 Connect GitHub Repository
If you signed up with GitHub:
1. You'll be asked to authorize Render to access your repositories
2. Grant access to your repositories
3. You should see your `task_calendar` repository in the list

### 4.3 Login via CLI
In your terminal:
```bash
render login
```

This will:
1. Open a browser window
2. Ask you to authorize the CLI
3. Show "Login successful" in your terminal

**✅ Once logged in, move to Step 5**

---

## Step 5: Configure Environment Variables

### 5.1 Create a .env.production file

Create a file called `.env.production` in your project root and add:
```
# Production Environment Variables
# Copy your Supabase connection string here
DATABASE_URL=your_supabase_connection_string_here
ENVIRONMENT=production
ALLOWED_ORIGINS=https://calendar-app.onrender.com
```

### 5.2 Update .env.production with your connection string

Open `.env.production` in your text editor and replace `your_supabase_connection_string_here` with your actual Supabase connection string from Step 2.

**IMPORTANT**: This file contains secrets and should never be committed to git. Make sure `.env.production` is in your `.gitignore` file.

**✅ Once you've updated .env.production with your connection string, move to Step 6**

---

## Step 6: Deploy to Render

### 6.1 Deploy Using Render Dashboard (Easier Method)

Since this is your first deployment, let's use the web dashboard:

1. Go to **[https://dashboard.render.com](https://dashboard.render.com)**
2. Click **"New +"** button
3. Select **"Web Service"**
4. Connect your GitHub repository:
   - Search for `task_calendar`
   - Click **"Connect"**

### 6.2 Configure the Web Service

Fill in these settings:

**Basic Settings:**
- **Name**: `calendar-app` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 6.3 Add Environment Variables

Scroll down to **"Environment Variables"** and add:

1. Click **"Add Environment Variable"**
   - **Key**: `DATABASE_URL`
   - **Value**: [Paste your Supabase connection string]

2. Add another:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.12.0`

3. Add another:
   - **Key**: `ENVIRONMENT`
   - **Value**: `production`

### 6.4 Create Web Service

1. Select **"Free"** instance type
2. Click **"Create Web Service"**

Render will now:
- Clone your repository
- Install dependencies
- Start your application

**This takes 3-5 minutes. You'll see the build logs in real-time.**

**✅ When you see "Live" status, move to Step 7**

---

## Step 7: Initialize Database on Production

### 7.1 Access Render Shell

You have two options:

**Option A: Using Render CLI**
```bash
# List your services
render services

# Select your calendar-app service and choose "SSH"
# Or directly:
render ssh --service calendar-app
```

**Option B: Using Render Dashboard**
1. In your Render dashboard, click on your `calendar-app` service
2. Click **"Shell"** tab in the left sidebar
3. This opens a web-based terminal

### 7.2 Initialize the Database

In the shell (either method), run:
```bash
python database.py
```

You should see:
```
Database tables created successfully!
```

### 7.3 Exit the Shell
```bash
exit
```

**✅ Database is now initialized! Move to Step 8**

---

## Step 8: Test the Deployed Application

### 8.1 Get Your App URL

**From Render Dashboard:**
1. In your service page, look at the top
2. You'll see your URL like: `https://calendar-app-xxxx.onrender.com`
3. Click on it to open your app

**From CLI:**
```bash
render services list
```

### 8.2 Test the Application

1. **Open the URL** in your browser
2. **Test functionality:**
   - Click on a calendar date
   - Add a new event
   - Refresh the page - event should persist
   - Edit an event
   - Delete an event

### 8.3 Check Logs (if needed)

If something isn't working:

**From Dashboard:**
- Click **"Logs"** tab in your service

**From CLI:**
```bash
render logs --tail
```

### 8.4 Verify Database Connection

You can also check your Supabase dashboard:
1. Go to your Supabase project
2. Click **"Table Editor"** in the left sidebar
3. You should see an `events` table
4. Any events you create should appear here

---

## 🎉 Congratulations!

Your calendar app is now deployed and running on:
- **Frontend & API**: Render (Free tier)
- **Database**: Supabase PostgreSQL (Free tier)

### Important Notes:

1. **Free Tier Limitations:**
   - Render services sleep after 15 minutes of inactivity
   - First request after sleeping takes ~30 seconds (cold start)
   - Supabase pauses after 7 days of inactivity

2. **Your URLs:**
   - App: `https://calendar-app-xxxx.onrender.com`
   - API Docs: `https://calendar-app-xxxx.onrender.com/docs`

3. **Monitoring:**
   - Render Dashboard: https://dashboard.render.com
   - Supabase Dashboard: https://app.supabase.com

## Troubleshooting

### Common Issues:

1. **"Database connection failed"**
   - Double-check your DATABASE_URL in Render environment variables
   - Ensure you replaced [YOUR-PASSWORD] with your actual password
   - Check if Supabase project is active

2. **"Module not found" errors**
   - Make sure all dependencies are in requirements.txt
   - Check Python version matches runtime.txt

3. **App crashes on startup**
   - Check logs for specific error messages
   - Verify all environment variables are set correctly

4. **"Port binding failed"**
   - Make sure your start command uses `$PORT` not a hardcoded port

### Getting Help:

- **Render Status**: https://status.render.com
- **Supabase Status**: https://status.supabase.com
- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs

## Future Improvements

Once your app is running, consider:

1. **Custom Domain**: Add your own domain name
2. **Monitoring**: Set up uptime monitoring (e.g., UptimeRobot)
3. **Backups**: Configure regular database backups
4. **Scaling**: Upgrade to paid tiers for better performance
5. **CI/CD**: Set up automated testing before deployment