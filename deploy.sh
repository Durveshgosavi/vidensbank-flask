#!/bin/bash
# Deployment script for Vidensbank Flask App
# This script pushes to both GitHub and Heroku

echo "========================================="
echo "  Vidensbank Deployment Script"
echo "========================================="
echo ""

# Check if there are uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "⚠️  You have uncommitted changes!"
    echo "Please commit your changes first:"
    echo "  git add ."
    echo "  git commit -m 'Your commit message'"
    exit 1
fi

echo "✓ No uncommitted changes"
echo ""

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main
if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi

echo ""

# Push to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main
if [ $? -eq 0 ]; then
    echo "✅ Successfully deployed to Heroku!"
else
    echo "❌ Failed to deploy to Heroku"
    exit 1
fi

echo ""
echo "========================================="
echo "  Deployment Complete! 🎉"
echo "========================================="
echo ""
echo "GitHub: https://github.com/Durveshgosavi/vidensbank-flask"
echo "Live Site: https://vidensbank-dk-f236e4b0da33.herokuapp.com/"
echo ""
