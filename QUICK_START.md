# 🚀 QUICK START GUIDE

## Hvad skal du gøre nu?

### Step 1: Download alle filerne
- Download hele `vidensbank-flask` mappen
- Placer den i `C:\Sites\vidensbank-flask`

### Step 2: Åbn PowerShell som Administrator
```powershell
# Naviger til dit projekt
cd C:\Sites\vidensbank-flask

# Opret virtual environment
python -m venv venv

# Aktiver det
.\venv\Scripts\Activate

# Installer alt
pip install -r requirements.txt
```

### Step 3: Test lokalt
```powershell
# Initialiser database
flask init-db

# Opret admin bruger
flask create-admin

# Start serveren
python app.py
```

Gå til: http://127.0.0.1:5000

### Step 4: Tilføj dine originale sider

1. **Kopiér dine HTML filer** fra `C:\Sites\vidensbank---cb-vidensbank\web-pages\` til `templates/`
2. **Konverter dem** ved at:
   - Tilføj `{% extends "base.html" %}` øverst
   - Wrap indhold i `{% block content %}...{% endblock %}`
   - Erstat Power Pages links med Flask url_for()
   
Eksempel:
```html
{% extends "base.html" %}
{% block content %}
<!-- Dit originale HTML indhold her -->
{% endblock %}
```

### Step 5: Deploy til Heroku

```powershell
# Login
heroku login

# Opret app
heroku create vidensbank

# Tilføj database
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY="en-meget-sikker-hemmelighed-123456"

# Git setup (hvis ikke allerede gjort)
git init
git add .
git commit -m "Initial deployment"

# Deploy!
git push heroku main

# Initialiser database på Heroku
heroku run flask init-db
heroku run flask create-admin

# Åbn din app
heroku open
```

## 🎯 Vigtige kommandoer

### Lokal udvikling
```powershell
python app.py              # Start server
flask init-db              # Nulstil database
flask create-admin         # Opret admin bruger
```

### Heroku
```powershell
heroku logs --tail         # Se logs
heroku restart             # Genstart app
heroku open                # Åbn app
git push heroku main       # Deploy ændringer
```

## ✅ Checklist

- [ ] Download alle filer
- [ ] Opret virtual environment
- [ ] Installer dependencies
- [ ] Test lokalt
- [ ] Tilføj dine originale sider
- [ ] Login til Heroku
- [ ] Opret Heroku app
- [ ] Tilføj database
- [ ] Deploy
- [ ] Test online
- [ ] Skift admin adgangskode

## 🆘 Problemer?

### Python ikke fundet?
- Geninstaller Python fra python.org
- Check "Add to PATH" under installation

### Virtual environment virker ikke?
```powershell
# Prøv dette i stedet
python -m venv venv
venv\Scripts\activate.bat
```

### Import errors?
```powershell
pip install -r requirements.txt --upgrade
```

### Heroku fejl?
```powershell
heroku logs --tail
```

## 📞 Næste skridt

1. Læs den fulde README.md
2. Tilpas design og farver i `static/css/style.css`
3. Tilføj dine sider fra Power Pages export
4. Test alle funktioner
5. Deploy til Heroku

**Held og lykke! 🎉**
