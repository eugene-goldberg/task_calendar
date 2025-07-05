#!/bin/bash

# Render + Supabase Deployment Script
# Prerequisites: 
# 1. Render CLI installed and authenticated
# 2. Supabase project created via web dashboard
# 3. Environment variables set

echo "🚀 Starting deployment to Render..."

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found. Please install it first:"
    echo "   Download from: https://github.com/render-oss/cli/releases"
    exit 1
fi

# Check if logged in to Render
if ! render whoami &> /dev/null; then
    echo "📝 Please login to Render first:"
    render login
fi

# Check for required environment variables
if [ -z "$SUPABASE_DB_URL" ]; then
    echo "❌ SUPABASE_DB_URL not set. Please set it first:"
    echo "   export SUPABASE_DB_URL='your-supabase-connection-string'"
    exit 1
fi

# Create render.yaml if it doesn't exist
if [ ! -f "render.yaml" ]; then
    echo "📄 Creating render.yaml..."
    cat > render.yaml << EOF
services:
  - type: web
    name: calendar-app
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port \$PORT
    envVars:
      - key: DATABASE_URL
        value: ${SUPABASE_DB_URL}
      - key: ENVIRONMENT
        value: production
      - key: PYTHON_VERSION
        value: 3.12.0
EOF
fi

# Deploy to Render
echo "🔄 Deploying to Render..."
render up

echo "✅ Deployment initiated!"
echo "📊 View deployment status:"
echo "   render services"
echo "📝 View logs:"
echo "   render logs"