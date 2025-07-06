# Deployment Steps for Recurrence Feature

## Overview
We've added recurring event functionality which requires database schema changes. Here's how to deploy these changes to production.

## Steps

### 1. Verify Automatic Deployment
Since you pushed to GitHub, Render should automatically deploy the new code. Check your Render dashboard:
- Go to https://dashboard.render.com
- Look for your `calendar-app` service
- Check if a new deployment is in progress or completed

### 2. Run Database Migration on Production

You need to add the new columns to your production database. You have two options:

#### Option A: Using Render Shell (Recommended)
1. Go to your Render dashboard
2. Click on your `calendar-app` service
3. Click the **"Shell"** tab in the left sidebar
4. In the shell, run:
   ```bash
   python migrate_recurrence.py
   ```
5. You should see:
   ```
   Added recurrence_type column
   Added recurrence_group_id column and index
   Migration completed successfully!
   ```

#### Option B: Using Render CLI
1. In your terminal, run:
   ```bash
   render ssh --service calendar-app
   ```
2. Once connected, run:
   ```bash
   python migrate_recurrence.py
   ```
3. Exit the shell:
   ```bash
   exit
   ```

### 3. Verify the Deployment

1. **Check Application Status:**
   - Visit your app URL: `https://calendar-app-xxxx.onrender.com`
   - Open the browser console (F12)
   - Try creating a new event with recurrence options

2. **Check Database Schema (Optional):**
   - In Supabase dashboard (https://app.supabase.com)
   - Go to your project
   - Click "Table Editor"
   - Select the `events` table
   - Verify the new columns exist:
     - `recurrence_type` (varchar)
     - `recurrence_group_id` (varchar)

### 4. Troubleshooting

If the migration fails:

1. **Check if columns already exist:**
   The migration script checks for existing columns, so it's safe to run multiple times.

2. **Manual migration via Supabase:**
   If the script fails, you can add columns manually:
   - Go to Supabase Table Editor
   - Select `events` table
   - Add columns:
     - Name: `recurrence_type`, Type: `text`, Nullable: ✓
     - Name: `recurrence_group_id`, Type: `text`, Nullable: ✓
   - Add index on `recurrence_group_id` via SQL Editor:
     ```sql
     CREATE INDEX idx_events_recurrence_group_id ON events(recurrence_group_id);
     ```

### 5. Monitor Logs

Check for any errors:
```bash
# Using Render CLI
render logs --tail

# Or in Render Dashboard
# Click on "Logs" tab
```

## Summary

The deployment process is mostly automatic through GitHub integration. The critical step is running the database migration to add the new columns. Once that's done, users can start creating recurring events!