#!/bin/bash

# CampusEats - Quick Deployment Helper Script
# This script helps you push code to GitHub for deployment

echo "========================================"
echo "  CampusEats - Deployment Helper"
echo "========================================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not a git repository"
    echo "   Run this script from the project root"
    exit 1
fi

echo "📋 Checking current status..."
echo ""

# Show current branch
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"

# Show git status
echo ""
echo "Modified files:"
git status --short

echo ""
echo "========================================"
echo ""

# Ask for commit message
echo "Enter commit message (or press Enter for default):"
read -r COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Deploy: Update CampusEats app with latest changes

- Backend updates with Supabase connection
- Frontend improvements
- Bug fixes and enhancements

🤖 Generated with Claude Code"
fi

echo ""
echo "========================================"
echo "  Deployment Steps"
echo "========================================"
echo ""

# Step 1: Add all changes
echo "1️⃣  Adding all changes to git..."
git add .

if [ $? -ne 0 ]; then
    echo "❌ Failed to add changes"
    exit 1
fi

echo "   ✅ Changes added"
echo ""

# Step 2: Commit
echo "2️⃣  Committing changes..."
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo "⚠️  Nothing to commit or commit failed"
    echo "   Check if you have uncommitted changes"
fi

echo ""

# Step 3: Push
echo "3️⃣  Pushing to GitHub..."
git push origin $BRANCH

if [ $? -ne 0 ]; then
    echo "❌ Failed to push to GitHub"
    echo ""
    echo "Common issues:"
    echo "  - Not authenticated (run: gh auth login)"
    echo "  - No internet connection"
    echo "  - Remote branch doesn't exist"
    exit 1
fi

echo "   ✅ Successfully pushed to GitHub!"
echo ""

# Get the GitHub URL
REMOTE_URL=$(git config --get remote.origin.url)
GITHUB_URL=${REMOTE_URL%.git}
GITHUB_URL=${GITHUB_URL/git@github.com:/https://github.com/}

echo "========================================"
echo "  ✅ Code Deployed to GitHub!"
echo "========================================"
echo ""
echo "🔗 Repository: $GITHUB_URL"
echo ""
echo "📝 Next Steps:"
echo ""
echo "  Backend Deployment (Render.com):"
echo "    1. Visit: https://render.com/dashboard"
echo "    2. Find or create 'campuseats-backend' service"
echo "    3. Set environment variables (DATABASE_URL, etc.)"
echo "    4. Click 'Manual Deploy' to deploy latest code"
echo ""
echo "  Frontend Deployment (Vercel):"
echo "    1. Visit: https://vercel.com/dashboard"
echo "    2. Find or create project from GitHub"
echo "    3. Set VITE_API_URL environment variable"
echo "    4. Deploy will happen automatically"
echo ""
echo "📖 Full guide: Open REDEPLOY_TO_WEB.md"
echo ""
echo "🎉 Happy deploying!"
