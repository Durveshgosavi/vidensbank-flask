# Vidensbank Flask - Deployment Guide

## Repository Setup

This project uses **GitHub as the primary repository** with automatic deployment to Heroku.

### Git Remotes
- **origin**: GitHub → `https://github.com/Durveshgosavi/vidensbank-flask.git`
- **heroku**: Heroku → `https://git.heroku.com/vidensbank-dk.git`

## Deployment Workflow

### Option 1: Use the Deploy Script (Recommended)

The easiest way to deploy is using the provided script:

```bash
./deploy.sh
```

This script will:
1. Check for uncommitted changes
2. Push to GitHub
3. Deploy to Heroku
4. Show deployment status

### Option 2: Manual Deployment

If you prefer manual control:

```bash
# 1. Commit your changes
git add .
git commit -m "Your commit message"

# 2. Push to GitHub
git push origin main

# 3. Deploy to Heroku
git push heroku main
```

### Option 3: Use Git Alias

We've set up a convenient alias:

```bash
# After committing changes, run:
git deploy
```

This runs both `git push origin main` and `git push heroku main` automatically.

## Quick Deploy (Common Workflow)

```bash
# 1. Make your changes
# 2. Test locally at http://127.0.0.1:5000

# 3. Commit and deploy
git add .
git commit -m "Description of changes"
./deploy.sh
```

## Important Notes

- **Always push to GitHub first** - This ensures your code is backed up
- **GitHub is the source of truth** - All changes should go through GitHub
- **Heroku deploys automatically** - When you use the deploy script or git alias

## Deployment URLs

- **GitHub Repository**: https://github.com/Durveshgosavi/vidensbank-flask
- **Live Application**: https://vidensbank-dk-f236e4b0da33.herokuapp.com/
- **Heroku Dashboard**: https://dashboard.heroku.com/apps/vidensbank-dk

## Troubleshooting

### Check deployment status
```bash
heroku ps
```

### View Heroku logs
```bash
heroku logs --tail
```

### Check recent releases
```bash
heroku releases
```

### Verify git remotes
```bash
git remote -v
```

## Future Enhancement: GitHub Actions

Consider setting up GitHub Actions for automatic deployment when you push to main:
- No need to manually push to Heroku
- Automatic testing before deployment
- Better CI/CD pipeline

Let me know if you'd like help setting this up!
