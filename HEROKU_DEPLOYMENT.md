# Heroku Deployment Guide

## Complete Step-by-Step Instructions for Deploying to Heroku

---

## Prerequisites

Before deploying, make sure you have:
- ✅ A Heroku account (sign up at https://heroku.com)
- ✅ Git installed on your computer
- ✅ Heroku CLI installed (download from https://devcenter.heroku.com/articles/heroku-cli)

---

## Step 1: Install Heroku CLI

### Download & Install:
Visit: https://devcenter.heroku.com/articles/heroku-cli

**Windows:** Download the installer and run it.

After installation, verify:
```powershell
heroku --version
```

---

## Step 2: Login to Heroku

Open PowerShell in your project directory:
```powershell
cd c:\Sites\vidensbank-flask
heroku login
```

This will open your browser for authentication.

---

## Step 3: Initialize Git Repository (if not already done)

```powershell
# Check if git is initialized
git status

# If not initialized, run:
git init
git add .
git commit -m "Initial commit - Visual migration complete"
```

---

## Step 4: Create Heroku App

```powershell
# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create vidensbank-app

# Or let Heroku generate a random name:
heroku create
```

**Note:** App names must be unique across all of Heroku.

---

## Step 5: Verify Your Configuration Files

Your project already has these files configured:

### ✅ Procfile
```
web: gunicorn app:app
```

### ✅ runtime.txt
```
python-3.12.0
```

### ✅ requirements.txt
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
```

These are already set up correctly! ✅

---

## Step 6: Set Environment Variables

Set your SECRET_KEY for Flask sessions:

```powershell
heroku config:set SECRET_KEY="your-super-secret-key-change-this-123456"
```

**Important:** Replace with a random secret key. Generate one with:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 7: Add PostgreSQL Database

Heroku uses PostgreSQL in production:

```powershell
heroku addons:create heroku-postgresql:essential-0
```

This automatically sets the `DATABASE_URL` environment variable.

---

## Step 8: Deploy to Heroku

```powershell
# Add all files
git add .

# Commit changes
git commit -m "Ready for Heroku deployment with visual migration"

# Push to Heroku
git push heroku main
```

**Note:** If your branch is named `master` instead of `main`:
```powershell
git push heroku master
```

---

## Step 9: Initialize the Database

After deployment, create the database tables:

```powershell
heroku run python
```

Then in the Python shell:
```python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

Or create a one-liner:
```powershell
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## Step 10: Open Your App

```powershell
heroku open
```

Your Vidensbank Flask application is now live! 🎉

---

## Quick Commands Reference

### View Logs
```powershell
heroku logs --tail
```

### Restart App
```powershell
heroku restart
```

### Check App Status
```powershell
heroku ps
```

### Open App in Browser
```powershell
heroku open
```

### Check Environment Variables
```powershell
heroku config
```

### Run Commands on Heroku
```powershell
heroku run <command>
```

### Scale Dynos (if needed)
```powershell
heroku ps:scale web=1
```

---

## Troubleshooting

### If deployment fails:

1. **Check logs:**
   ```powershell
   heroku logs --tail
   ```

2. **Verify Python version:**
   Make sure `runtime.txt` has a valid Python version supported by Heroku.

3. **Check requirements.txt:**
   Ensure all dependencies are listed with versions.

4. **Database issues:**
   Run migrations:
   ```powershell
   heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### Common Issues:

**Issue:** `Application Error` or `H10 error`
**Solution:** Check that your Procfile is correct and gunicorn is in requirements.txt

**Issue:** Static files not loading
**Solution:** Make sure Bootstrap CSS was copied to `static/css/`

**Issue:** Database connection errors
**Solution:** Verify DATABASE_URL is set: `heroku config`

---

## Update Your App

After making changes:

```powershell
# Stage changes
git add .

# Commit with a message
git commit -m "Your update message"

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail
```

---

## Environment Variables You Should Set

```powershell
# Required
heroku config:set SECRET_KEY="your-secret-key-here"

# Optional (for production)
heroku config:set FLASK_ENV="production"
heroku config:set FLASK_DEBUG="False"
```

---

## Database Management

### Backup Database
```powershell
heroku pg:backups:capture
heroku pg:backups:download
```

### View Database Info
```powershell
heroku pg:info
```

### Connect to Database
```powershell
heroku pg:psql
```

---

## Monitoring

### View App Performance
```powershell
heroku logs --tail --dyno web
```

### Check Dyno Usage
Visit: https://dashboard.heroku.com/apps/your-app-name/metrics

---

## Cost Information

- **Essential-0 PostgreSQL:** ~$5/month
- **Web Dyno (Basic):** ~$7/month
- **Total:** ~$12/month minimum

**Free Alternative:** Use Heroku's free tier with limitations (sleeps after 30 min of inactivity)

---

## Production Checklist

Before going live:

- [ ] Set SECRET_KEY to a secure random value
- [ ] Set FLASK_ENV to "production"
- [ ] Set FLASK_DEBUG to "False"
- [ ] Add custom domain (if needed)
- [ ] Set up SSL certificate (automatic with Heroku)
- [ ] Configure backup schedule
- [ ] Test all routes and functionality
- [ ] Set up monitoring and alerts
- [ ] Add admin user to database

---

## Adding a Custom Domain

1. Add domain to Heroku:
```powershell
heroku domains:add www.yourdomain.com
```

2. Get DNS target:
```powershell
heroku domains
```

3. Update your DNS provider with the provided CNAME record.

---

## Complete Deployment Script

Here's everything in one script:

```powershell
# 1. Navigate to project
cd c:\Sites\vidensbank-flask

# 2. Login to Heroku
heroku login

# 3. Create app
heroku create vidensbank-app

# 4. Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key"

# 5. Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# 6. Deploy
git add .
git commit -m "Deploy with visual migration"
git push heroku main

# 7. Initialize database
heroku run python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 8. Open app
heroku open

# 9. View logs
heroku logs --tail
```

---

## Success!

Your Vidensbank Flask application with the complete visual migration from Power Pages is now running on Heroku! 🚀

Visit your app at: `https://your-app-name.herokuapp.com`

---

## Need Help?

- Heroku Documentation: https://devcenter.heroku.com/
- Heroku Status: https://status.heroku.com/
- Support: https://help.heroku.com/

Your app is production-ready with all the visual elements from Power Pages! 🎉
