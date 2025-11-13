# Vidensbank Flask - Development Workflow

This document provides a complete guide for developing and deploying the Vidensbank Flask application.

## Project Overview

- **Local URL**: http://127.0.0.1:5000
- **Heroku URL**: https://vidensbank-dk-f236e4b0da33.herokuapp.com/
- **Heroku App**: vidensbank-dk
- **Python Version**: 3.12 (latest patch applied automatically)

## Initial Setup (One-Time)

### 1. Prerequisites

- Python 3.12 installed
- Git installed
- Heroku CLI installed
- Git Bash (for Windows)

### 2. Clone and Setup

```bash
# Navigate to project
cd C:\Sites\vidensbank-flask

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt

# Initialize local database
python init_db.py
```

## Daily Development Workflow

### Starting Your Work Session

```bash
# 1. Navigate to project
cd C:\Sites\vidensbank-flask

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Pull latest changes
git pull origin main  # If using GitHub
# OR
git pull heroku main  # If only using Heroku

# 4. Check for any dependency updates
python -m pip install -r requirements.txt
```

### Local Development and Testing

```bash
# Run the application locally
python app.py

# App will be available at: http://127.0.0.1:5000
# Press Ctrl+C to stop the server

# Test specific features:
# - Create a user account
# - Login/logout
# - Create/edit pages
# - Test contact form
```

### Making Code Changes

1. **Edit files** in your preferred editor (VSCode, PyCharm, etc.)
2. **Test locally** using `python app.py`
3. **Check for errors** in the terminal output
4. **Verify** changes in browser at http://127.0.0.1:5000

## Git Workflow

### Checking Status

```bash
# See what files have changed
git status

# See specific changes in files
git diff
```

### Committing Changes

```bash
# Add specific files
git add filename.py

# Or add all changed files
git add .

# Commit with a descriptive message
git commit -m "feat: add new feature description"

# Common commit prefixes:
# - feat: new feature
# - fix: bug fix
# - chore: maintenance tasks
# - docs: documentation changes
# - refactor: code restructuring
# - style: formatting changes
```

### Viewing History

```bash
# View recent commits
git log --oneline -10

# View detailed history
git log
```

## Heroku Deployment Workflow

### Quick Deploy

```bash
# Deploy to Heroku (after committing changes)
git push heroku main

# The deployment process will:
# 1. Build the application
# 2. Install dependencies
# 3. Deploy to Heroku servers
# 4. Restart the application
```

### Monitoring and Troubleshooting

```bash
# View real-time logs
heroku logs --tail

# View recent logs
heroku logs --num=100

# Check app status
heroku apps:info

# Restart the app
heroku restart

# Open app in browser
heroku open
# Or manually visit: https://vidensbank-dk-f236e4b0da33.herokuapp.com/
```

### Database Management

```bash
# Initialize/reset database tables
heroku run python init_db.py

# Access PostgreSQL console (advanced)
heroku pg:psql

# View database info
heroku pg:info

# Create database backup
heroku pg:backups:capture
```

### Environment Variables

```bash
# View all config variables
heroku config

# Set a new variable
heroku config:set VARIABLE_NAME=value

# Remove a variable
heroku config:unset VARIABLE_NAME

# Current variables:
# - DATABASE_URL (automatically set by PostgreSQL addon)
# - SECRET_KEY (application secret key)
```

## Common Development Tasks

### Adding New Python Packages

```bash
# Install the package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Commit and deploy
git add requirements.txt
git commit -m "chore: add package-name dependency"
git push heroku main
```

### Creating New Routes/Pages

1. **Add route in `app.py`**:
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

2. **Create template** in `templates/new_page.html`

3. **Test locally** with `python app.py`

4. **Commit and deploy**:
```bash
git add app.py templates/new_page.html
git commit -m "feat: add new page"
git push heroku main
```

### Database Schema Changes

```bash
# 1. Update models in app.py
# 2. Test locally:
python init_db.py

# 3. Deploy to Heroku:
git add app.py
git commit -m "feat: update database schema"
git push heroku main

# 4. Re-initialize Heroku database:
heroku run python init_db.py
# WARNING: This will drop all existing data!
```

## Troubleshooting Guide

### Application Error on Heroku

```bash
# Check logs for errors
heroku logs --tail

# Common issues:
# 1. Missing environment variables → heroku config:set VAR=value
# 2. Database not initialized → heroku run python init_db.py
# 3. Dependency issues → Check requirements.txt
# 4. Memory exceeded → Consider upgrading dyno
```

### Local Database Issues

```bash
# Reset local database
rm instance/vidensbank.db  # Delete old database
python init_db.py          # Create fresh database
```

### Git Issues

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename.py

# Discard all local changes
git reset --hard HEAD
```

## File Structure Reference

```
vidensbank-flask/
├── app.py                  # Main application file
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku process configuration
├── .python-version       # Python version for Heroku
├── .env                  # Local environment variables (not in git)
├── .gitignore            # Git ignore rules
├── static/               # CSS, JavaScript, images
├── templates/            # HTML templates
└── instance/             # Local database (not in git)
```

## Quick Reference Commands

### Local Development
```bash
cd C:\Sites\vidensbank-flask
.venv\Scripts\activate
python app.py
```

### Deploy to Heroku
```bash
git add .
git commit -m "description"
git push heroku main
```

### View Logs
```bash
heroku logs --tail
```

### Open App
```bash
heroku open
```

### Database Reset
```bash
# Local:
python init_db.py

# Heroku:
heroku run python init_db.py
```

## Getting Help

### Heroku Resources
- Status: https://status.heroku.com/
- Documentation: https://devcenter.heroku.com/
- Support: `heroku help`

### Flask Resources
- Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/

### Using Claude Code

When you need help with development:

1. **Describe the issue or feature** clearly
2. **Provide error messages** if applicable
3. **Mention what you've tried** already
4. **Test suggested changes locally** before deploying
5. **Commit working code** with descriptive messages

### Saving Claude Conversations

```bash
# Create documentation from helpful Claude sessions
mkdir -p docs/claude-sessions

# Save summary in a markdown file
echo "# Feature Name - $(date +%Y-%m-%d)" > docs/claude-sessions/feature-name.md
```

## Best Practices

1. **Always test locally** before deploying to Heroku
2. **Commit frequently** with descriptive messages
3. **Check logs** after deployment
4. **Never commit sensitive data** (.env is in .gitignore)
5. **Keep requirements.txt updated** when adding packages
6. **Create database backups** before schema changes
7. **Use environment variables** for configuration
8. **Monitor Heroku dyno usage** to avoid overages

## Emergency Procedures

### Roll Back a Deployment

```bash
# View recent releases
heroku releases

# Roll back to previous version
heroku rollback v28  # Replace with version number
```

### Application Down

```bash
# 1. Check status
heroku ps

# 2. Check logs
heroku logs --tail

# 3. Restart app
heroku restart

# 4. If database issue:
heroku pg:info
heroku run python init_db.py
```

### Lost Local Changes

```bash
# Retrieve from last commit
git checkout HEAD -- filename.py

# Retrieve from Heroku
git fetch heroku
git checkout heroku/main -- filename.py
```

---

**Last Updated**: 2025-11-13
**Maintained By**: Development Team
