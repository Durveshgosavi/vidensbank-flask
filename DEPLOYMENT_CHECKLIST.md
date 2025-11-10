# 📋 COMPLETE DEPLOYMENT CHECKLIST

## Phase 1: Local Setup (30 minutes)

### ✅ Prerequisites
- [ ] Python 3.12+ installed and in PATH
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] PowerShell or Terminal access

### ✅ Download & Setup
```powershell
# 1. Navigate to your Sites folder
cd C:\Sites

# 2. Create project directory (if files not already there)
mkdir vidensbank-flask
cd vidensbank-flask

# 3. Download all files from outputs to this directory

# 4. Verify files
dir
# You should see: app.py, requirements.txt, Procfile, static/, templates/
```

### ✅ Create Virtual Environment
```powershell
# 1. Create venv
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate

# You should see (venv) in your prompt

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt
```

### ✅ Test Locally
```powershell
# 1. Initialize database
flask init-db

# 2. Create admin user
flask create-admin
# Username: admin
# Password: admin123

# 3. Run the app
python app.py

# 4. Open browser to http://127.0.0.1:5000
```

### ✅ Verify Local Installation
- [ ] Home page loads
- [ ] Navigation works
- [ ] Can access /login page
- [ ] Can access /calculator page
- [ ] Can access /contact page
- [ ] Login with admin/admin123 works
- [ ] No console errors in browser

---

## Phase 2: Migration of Your Content (1-2 hours)

### ✅ Prepare Your Original Content
```powershell
# 1. Your Power Pages export is here:
C:\Sites\vidensbank---cb-vidensbank\

# 2. Web pages are here:
C:\Sites\vidensbank---cb-vidensbank\web-pages\
```

### ✅ Option A: Automated Conversion (Easier)
```powershell
# Run the converter script
python convert_pages.py "C:\Sites\vidensbank---cb-vidensbank\web-pages"

# This will create Flask templates from your HTML files
```

### ✅ Option B: Manual Conversion (More Control)
For each page you want to migrate:

1. **Copy HTML file to templates/**
   ```
   Emissioner-og-bæredygtighed_en-US_webpage_copy.html
   -> templates/emissions_sustainability.html
   ```

2. **Wrap in Flask template structure**
   ```html
   {% extends "base.html" %}
   
   {% block title %}Your Title - Vidensbank{% endblock %}
   
   {% block content %}
   <!-- Your original HTML content here -->
   {% endblock %}
   ```

3. **Update internal links**
   ```html
   <!-- Old Power Pages link -->
   <a href="/EmissionerogbÃ¦redygtighed/page">Link</a>
   
   <!-- New Flask link -->
   <a href="{{ url_for('page_name') }}">Link</a>
   ```

### ✅ Add Routes for New Pages
Edit `app.py` and add routes:

```python
@app.route('/din-nye-side')
def din_nye_side():
    return render_template('din_nye_side.html')
```

### ✅ Copy Assets
```powershell
# Copy images from Power Pages export
# From: C:\Sites\vidensbank---cb-vidensbank\web-files\
# To: C:\Sites\vidensbank-flask\static\images\
```

### ✅ Test All Migrated Pages
- [ ] All pages load without errors
- [ ] All links work
- [ ] Images display correctly
- [ ] Forms submit correctly
- [ ] No console errors

---

## Phase 3: Heroku Preparation (15 minutes)

### ✅ Install Heroku CLI
```powershell
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or use:
winget install heroku
```

### ✅ Verify Heroku Installation
```powershell
heroku --version
# Should show version number
```

### ✅ Login to Heroku
```powershell
heroku login
# Opens browser for login
```

### ✅ Verify Your Heroku Credits
```powershell
heroku credits
# Should show your $312 credit
```

---

## Phase 4: Git Setup (10 minutes)

### ✅ Initialize Git Repository
```powershell
# In your project folder
cd C:\Sites\vidensbank-flask

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Flask migration from Power Pages"
```

### ✅ Verify Git Status
```powershell
git status
# Should show: "nothing to commit, working tree clean"
```

---

## Phase 5: Heroku Deployment (20 minutes)

### ✅ Create Heroku App
```powershell
# Create app (choose a unique name)
heroku create vidensbank-dk

# Or let Heroku generate a name
heroku create

# Note the app URL it gives you
```

### ✅ Add PostgreSQL Database
```powershell
# Add free PostgreSQL
heroku addons:create heroku-postgresql:mini

# Verify it's added
heroku addons
```

### ✅ Set Environment Variables
```powershell
# Generate a strong secret key
# Use: https://randomkeygen.com/ or:
python -c "import secrets; print(secrets.token_hex(32))"

# Set it on Heroku
heroku config:set SECRET_KEY="your-generated-secret-key-here"

# Set Flask environment
heroku config:set FLASK_ENV=production

# Verify
heroku config
```

### ✅ Deploy to Heroku
```powershell
# Push to Heroku
git push heroku main

# Or if your branch is master:
git push heroku master

# Wait for build to complete (2-5 minutes)
```

### ✅ Initialize Database on Heroku
```powershell
# Initialize database
heroku run flask init-db

# Create admin user
heroku run flask create-admin

# Verify admin was created
```

### ✅ Open Your App
```powershell
# Open in browser
heroku open
```

---

## Phase 6: Post-Deployment (15 minutes)

### ✅ Test Production Site
- [ ] Site loads without errors
- [ ] Home page displays correctly
- [ ] All navigation links work
- [ ] Login works
- [ ] Calculator works
- [ ] Contact form works
- [ ] All your migrated pages load
- [ ] Images display correctly
- [ ] No console errors

### ✅ Security Updates
```powershell
# Change admin password via app or:
heroku run python
>>> from app import db, User
>>> admin = User.query.filter_by(username='admin').first()
>>> admin.set_password('new-secure-password')
>>> db.session.commit()
>>> exit()
```

### ✅ Monitor Application
```powershell
# View logs
heroku logs --tail

# Check status
heroku ps

# View app info
heroku info
```

### ✅ Optional: Add Custom Domain
```powershell
# If you have a domain
heroku domains:add www.yourdomain.dk
heroku domains:add yourdomain.dk

# Follow DNS instructions
```

---

## Phase 7: Maintenance & Updates

### ✅ Making Changes
```powershell
# 1. Make your changes locally
# 2. Test locally: python app.py
# 3. Commit changes
git add .
git commit -m "Description of changes"

# 4. Deploy
git push heroku main

# 5. Verify deployment
heroku open
```

### ✅ Database Backups
```powershell
# Heroku auto-backs up your database
# Manual backup:
heroku pg:backups:capture

# List backups
heroku pg:backups
```

### ✅ Useful Commands
```powershell
# Restart app
heroku restart

# View logs
heroku logs --tail

# Access database
heroku pg:psql

# Check dyno usage
heroku ps

# View config
heroku config
```

---

## 🎉 Success Criteria

Your deployment is successful when:

- ✅ Site loads on Heroku URL
- ✅ All pages render correctly
- ✅ User authentication works
- ✅ Calculator functions properly
- ✅ Forms submit successfully
- ✅ No errors in Heroku logs
- ✅ Site is responsive on mobile
- ✅ Admin can log in and manage content

---

## 📊 Resource Usage

With your $312 Heroku credit:

- **Basic Dyno:** $7/month = 44 months (3.6 years)
- **Database:** Free tier (10,000 rows) = Enough for your needs
- **SSL Certificate:** Included free
- **Custom Domain:** Free (DNS setup required)

---

## 🆘 Troubleshooting

### App won't start
```powershell
# Check logs
heroku logs --tail

# Common fixes:
heroku restart
heroku ps:scale web=1
```

### Database errors
```powershell
# Reset database
heroku pg:reset DATABASE_URL
heroku run flask init-db
heroku run flask create-admin
```

### Import errors
```powershell
# Verify requirements.txt
cat requirements.txt

# Redeploy
git push heroku main
```

### Slow loading
```powershell
# Check dyno status
heroku ps

# Upgrade if needed (costs more)
heroku ps:scale web=1:basic
```

---

## 📞 Support Resources

- **Heroku Docs:** https://devcenter.heroku.com/
- **Flask Docs:** https://flask.palletsprojects.com/
- **Heroku Status:** https://status.heroku.com/

---

**✨ Your site is now live on Heroku! ✨**

Remember to:
1. Change admin password
2. Monitor logs regularly
3. Keep dependencies updated
4. Test before deploying changes

**Tillykke! (Congratulations!)** 🎊
