# Vidensbank Flask Application

En Flask webapplikation for bæredygtighed og klimadata, migreret fra Microsoft Power Pages.

## 📋 Indhold

- [Funktioner](#funktioner)
- [Teknologier](#teknologier)
- [Lokal Installation](#lokal-installation)
- [Heroku Deployment](#heroku-deployment)
- [Brug](#brug)
- [Tilpasning](#tilpasning)

## ✨ Funktioner

- ✅ **Brugerautentifikation** (Login, registrering, roller)
- ✅ **CO2 Beregner** med interaktiv API
- ✅ **Søgefunktionalitet**
- ✅ **Kontaktformular**
- ✅ **Responsivt design** med flip cards og KPI dashboards
- ✅ **Admin panel** for indholdsstyring
- ✅ **PostgreSQL database** support
- ✅ **Heroku-klar** deployment

## 🛠 Teknologier

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Database:** PostgreSQL (production), SQLite (development)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Heroku med Gunicorn

## 💻 Lokal Installation

### Forudsætninger

- Python 3.12 eller nyere
- Git
- Virtual environment (anbefalet)

### Trin-for-Trin Guide

1. **Åbn PowerShell og naviger til dit projekt**
   ```powershell
   cd C:\Sites\vidensbank-flask
   ```

2. **Opret virtual environment**
   ```powershell
   python -m venv venv
   ```

3. **Aktiver virtual environment**
   ```powershell
   .\venv\Scripts\Activate
   ```

4. **Installer dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Initialiser databasen**
   ```powershell
   flask init-db
   ```

6. **Opret admin bruger (valgfrit)**
   ```powershell
   flask create-admin
   ```
   Dette opretter en admin bruger:
   - **Brugernavn:** admin
   - **Adgangskode:** admin123
   - ⚠️ **Skift dette i produktion!**

7. **Kør applikationen**
   ```powershell
   python app.py
   ```

8. **Åbn browseren**
   - Gå til: `http://127.0.0.1:5000`

## 🚀 Heroku Deployment

### Forudsætninger

- Heroku konto
- Heroku CLI installeret
- Git repository

### Deployment Steps

1. **Login til Heroku**
   ```powershell
   heroku login
   ```

2. **Opret Heroku app**
   ```powershell
   heroku create vidensbank-app
   ```
   (Erstat `vidensbank-app` med dit ønskede navn)

3. **Tilføj PostgreSQL database**
   ```powershell
   heroku addons:create heroku-postgresql:mini
   ```

4. **Sæt environment variables**
   ```powershell
   heroku config:set SECRET_KEY="din-meget-sikre-hemmelighed-her"
   heroku config:set FLASK_ENV=production
   ```

5. **Initialize Git (hvis ikke allerede gjort)**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. **Deploy til Heroku**
   ```powershell
   git push heroku main
   ```
   (Eller `git push heroku master` hvis din branch hedder master)

7. **Initialiser database på Heroku**
   ```powershell
   heroku run flask init-db
   heroku run flask create-admin
   ```

8. **Åbn din app**
   ```powershell
   heroku open
   ```

### Nyttige Heroku Kommandoer

```powershell
# Se logs
heroku logs --tail

# Restart app
heroku restart

# Se config
heroku config

# Åbn database console
heroku pg:psql

# Scale dynos
heroku ps:scale web=1
```

## 📖 Brug

### Admin Panel

1. Log ind med admin credentials
2. Gå til `/admin`
3. Administrer:
   - Brugere
   - Sider
   - Kontaktformularer

### CO2 Beregner

1. Gå til `/calculator`
2. Vælg fødevare
3. Indtast mængde
4. Klik "Beregn CO2"

### Søgefunktion

- Brug søgefeltet i navigationen
- Søg efter emner, sider eller indhold

## 🎨 Tilpasning

### Farver

Rediger CSS variabler i `static/css/style.css`:

```css
:root {
  --cheval-gron: #a0d7a5;
  --cheval-gul: #f4d03f;
  --cheval-orange: #ff9f43;
  /* ... */
}
```

### Tilføj Nye Sider

1. **Opret template** i `templates/`:
   ```html
   {% extends "base.html" %}
   {% block content %}
   <!-- Dit indhold -->
   {% endblock %}
   ```

2. **Tilføj route** i `app.py`:
   ```python
   @app.route('/din-side')
   def din_side():
       return render_template('din_side.html')
   ```

3. **Tilføj til navigation** i `templates/base.html`

### Database Modeller

Rediger modeller i `app.py` og kør:
```powershell
flask db init
flask db migrate -m "Beskrivelse"
flask db upgrade
```

## 📁 Projekt Struktur

```
vidensbank-flask/
├── app.py                      # Hoved Flask applikation
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku config
├── runtime.txt                 # Python version
├── .gitignore                  # Git ignore fil
├── static/
│   ├── css/
│   │   └── style.css          # Hoved stylesheet
│   ├── js/
│   │   └── main.js            # JavaScript
│   └── images/                # Billeder
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Forside
│   ├── emissions_sustainability.html
│   ├── calculator.html        # CO2 beregner
│   ├── login.html             # Login side
│   ├── register.html          # Registrering
│   ├── contact.html           # Kontakt
│   ├── dashboard.html         # User dashboard
│   ├── admin.html             # Admin panel
│   └── [andre sider]
└── README.md                   # Denne fil
```

## 🔒 Sikkerhed

### Produktion Checklist

- [ ] Skift `SECRET_KEY` til en sikker værdi
- [ ] Skift admin adgangskode
- [ ] Sæt `FLASK_ENV=production`
- [ ] Aktiver HTTPS (gratis på Heroku)
- [ ] Brug environment variables for følsomme data
- [ ] Implementer rate limiting (valgfrit)

## 🐛 Fejlfinding

### Database fejl
```powershell
# Slet og genopret database
rm vidensbank.db
flask init-db
```

### Import fejl
```powershell
# Geninstaller dependencies
pip install -r requirements.txt --force-reinstall
```

### Heroku fejl
```powershell
# Check logs
heroku logs --tail

# Restart
heroku restart
```

## 📝 Næste Skridt

1. ✅ Kopier dine originale HTML filer ind i templates
2. ✅ Tilføj dine billeder til `static/images/`
3. ✅ Opdater routes i `app.py` for alle dine sider
4. ✅ Tilpas design og farver
5. ✅ Test lokalt
6. ✅ Deploy til Heroku
7. ✅ Tilføj custom domain (valgfrit)

## 🆘 Support

Hvis du støder på problemer:
1. Check `heroku logs --tail`
2. Verificer alle environment variables er sat
3. Sørg for database er initialiseret
4. Check at alle dependencies er installeret

## 📄 Licens

Dette projekt er udviklet til intern brug.

---

**Bygget med ❤️ for bæredygtighed**
