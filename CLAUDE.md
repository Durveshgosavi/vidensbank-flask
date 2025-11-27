# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vidensbank is a Flask-based knowledge bank application with user authentication, page management, and contact forms. The application is deployed on Heroku with PostgreSQL database.

- **Framework**: Flask 3.0.0
- **Database**: SQLAlchemy with PostgreSQL (production) / SQLite (development)
- **Authentication**: Flask-Login
- **Deployment**: Heroku (vidensbank-dk)
- **Python Version**: 3.12

## Common Commands

### Local Development

```bash
# Activate virtual environment (Windows)
.venv\Scripts\activate

# Run application locally
python app.py
# Access at: http://127.0.0.1:5000

# Initialize local database
python init_db.py

# Install dependencies
python -m pip install -r requirements.txt
```

### Deployment

```bash
# Deploy to Heroku
git push heroku main

# View logs
heroku logs --tail

# Initialize Heroku database
heroku run python init_db.py

# Check app status
heroku apps:info

# Open deployed app
heroku open
# Or visit: https://vidensbank-dk-f236e4b0da33.herokuapp.com/
```

### Git Operations

```bash
# Commit changes
git add .
git commit -m "description"

# Push to Heroku
git push heroku main
```

## Architecture

### Application Structure

- **app.py**: Main application file containing:
  - Database models (User, Page, ContactForm)
  - Routes and view functions
  - Authentication logic
  - App configuration

- **init_db.py**: Database initialization script
  - Creates all database tables
  - Safe to run multiple times (doesn't drop data)

- **templates/**: Jinja2 HTML templates
  - Base template with navigation
  - Individual page templates
  - Forms for login, registration, etc.

- **static/**: CSS, JavaScript, images
  - Custom styles
  - Client-side functionality

### Database Models

**User Model** (`app.py:23-35`):
- Authentication and authorization
- Fields: username, email, password_hash, role, created_at
- Roles: user, admin, editor

**Page Model** (`app.py:37-45`):
- Content management
- Fields: title, slug, content, topic, is_published, timestamps
- Used for knowledge base articles

**ContactForm Model** (`app.py:47+`):
- Contact submissions
- Fields: name, email, message, timestamp

### Configuration

Environment variables (stored in `.env` locally, Heroku config for production):
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: development/production
- `FLASK_DEBUG`: 1/0 for debug mode

Heroku automatically sets `DATABASE_URL` when PostgreSQL addon is added.

### Authentication Flow

1. User registration creates new User with hashed password
2. Login validates credentials and creates session
3. `@login_required` decorator protects authenticated routes
4. User role determines admin access

## Development Guidelines

### Adding New Features

1. **Update models** in app.py if database changes needed
2. **Create routes** for new functionality
3. **Add templates** in templates/ directory
4. **Test locally** with `python app.py`
5. **Commit changes** with descriptive message
6. **Deploy to Heroku**

### Database Changes

When modifying database schema:
1. Update models in app.py
2. Test locally: `python init_db.py`
3. Deploy: `git push heroku main`
4. Initialize Heroku DB: `heroku run python init_db.py`

**Note**: `db.create_all()` only creates missing tables. It doesn't alter existing schema. For production, consider using Flask-Migrate for database migrations.

### Adding Dependencies

```bash
# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Commit and deploy
git add requirements.txt
git commit -m "chore: add package-name"
git push heroku main
```

### Static Files

- Place CSS in `static/css/`
- Place JavaScript in `static/js/`
- Place images in `static/images/`
- Reference in templates: `{{ url_for('static', filename='css/style.css') }}`
- Tailwind CSS is used for styling. To build the CSS, run the following command:
  ```bash
  curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
  chmod +x tailwindcss-linux-x64
  ./tailwindcss-linux-x64 -i ./static/src/input.css -o ./static/dist/output.css
  ```

### Templates

- Extend base template: `{% extends "base.html" %}`
- Use template inheritance for consistent layout
- Flash messages for user feedback: `flash('message', 'category')`
- Display flashed messages in templates: `get_flashed_messages()`

## Important Files

- **app.py**: Main application - routes, models, configuration
- **init_db.py**: Database initialization
- **requirements.txt**: Python dependencies
- **Procfile**: Heroku process definition (`web: gunicorn app:app`)
- **.python-version**: Python version for Heroku (3.12)
- **.env**: Local environment variables (never commit)
- **.gitignore**: Excludes .env, .venv, *.db, etc.

## Deployment Process

1. Code changes committed to git
2. Push to Heroku: `git push heroku main`
3. Heroku builds application:
   - Installs Python 3.12
   - Installs dependencies from requirements.txt
   - Starts gunicorn server
4. Application runs on Heroku dyno
5. PostgreSQL database managed by Heroku addon

## Troubleshooting

### Common Issues

**Application Error on Heroku**:
```bash
heroku logs --tail  # Check for errors
heroku restart      # Restart application
```

**Database Issues**:
```bash
heroku run python init_db.py  # Reinitialize tables
heroku pg:info                # Check database status
```

**Local Environment**:
```bash
# Ensure .env file exists with:
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///vidensbank.db
FLASK_ENV=development
FLASK_DEBUG=1
```

**Dependencies**:
```bash
python -m pip install -r requirements.txt  # Reinstall all
```

## Security Considerations

- Never commit `.env` file (in .gitignore)
- SECRET_KEY must be strong in production (set in Heroku config)
- Passwords are hashed using Werkzeug security
- Use HTTPS in production (Heroku provides)
- Validate and sanitize all user inputs
- Use CSRF protection for forms

## Performance Notes

- SQLite for local development (simple, file-based)
- PostgreSQL for production (robust, concurrent)
- Static files served by Flask in development
- Consider CDN for static files in production at scale
- Database connection pooling handled by SQLAlchemy

## Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Heroku Python: https://devcenter.heroku.com/categories/python-support
- Flask-Login: https://flask-login.readthedocs.io/

## Workflow Documentation

See `WORKFLOW.md` for detailed development and deployment workflows, troubleshooting guides, and best practices.
