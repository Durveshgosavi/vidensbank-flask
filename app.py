from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///vidensbank.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin, editor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, read, replied

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================================================
# CONTEXT PROCESSORS
# ============================================================================

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# ============================================================================
# ROUTES - PUBLIC PAGES
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emissioner-og-baeredygtighed')
def emissions_sustainability():
    return render_template('emissions_sustainability.html')

@app.route('/emissioner-og-baeredygtighed/fodevare-relaterede-emissioner')
def food_emissions():
    return render_template('food_emissions.html')

@app.route('/emissioner-og-baeredygtighed/datadrevet-tilgang')
def data_driven_approach():
    return render_template('data_driven_approach.html')

@app.route('/emissioner-og-baeredygtighed/branchepraestation')
def market_analysis():
    return render_template('market_analysis.html')

@app.route('/emissioner-og-baeredygtighed/politisk-landskab')
def political_landscape():
    return render_template('political_landscape.html')

@app.route('/emissioner-og-baeredygtighed/klimadata')
def climate_data():
    return render_template('climate_data.html')

# ============================================================================
# ØKOLOGI ROUTES
# ============================================================================

@app.route('/okologi')
def okologi():
    return render_template('okologi/main.html')

@app.route('/okologi/hvad-er')
def okologi_hvad_er():
    return render_template('okologi/okologi_hvad_er.html')

@app.route('/okologi/regulering')
def okologi_regulering():
    return render_template('okologi/okologi_regulering.html')

@app.route('/okologi/fordele')
def okologi_fordele():
    return render_template('okologi/okologi_fordele.html')

@app.route('/okologi/kantinen')
def okologi_kantinen():
    return render_template('okologi/okologi_kantinen.html')

@app.route('/okologi/esg')
def okologi_esg():
    return render_template('okologi/okologi_esg.html')

@app.route('/okologi/nuanceret')
def okologi_nuanceret():
    return render_template('okologi/okologi_nuanceret.html')

# Add more routes for your other pages here

# ============================================================================
# CO2 CALCULATOR
# ============================================================================

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/api/calculate-co2', methods=['POST'])
def calculate_co2():
    """API endpoint for CO2 calculations"""
    data = request.json
    
    # Example calculation logic - customize based on your needs
    food_type = data.get('food_type', '')
    quantity = float(data.get('quantity', 0))
    
    # CO2 emissions per kg (example values)
    emission_factors = {
        'beef': 27.0,
        'pork': 12.1,
        'chicken': 6.9,
        'fish': 5.0,
        'vegetables': 2.0,
        'dairy': 8.0,
        'grains': 1.5
    }
    
    co2_per_kg = emission_factors.get(food_type.lower(), 5.0)
    total_co2 = quantity * co2_per_kg
    
    return jsonify({
        'success': True,
        'co2_emissions': round(total_co2, 2),
        'food_type': food_type,
        'quantity': quantity,
        'unit': 'kg CO2e'
    })

# ============================================================================
# SEARCH FUNCTIONALITY
# ============================================================================

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Search in page titles and content
        results = Page.query.filter(
            db.or_(
                Page.title.ilike(f'%{query}%'),
                Page.content.ilike(f'%{query}%')
            ),
            Page.is_published == True
        ).all()
    else:
        results = []
    
    return render_template('search_results.html', query=query, results=results)

# ============================================================================
# CONTACT FORM
# ============================================================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact = ContactForm(
            name=request.form.get('name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message')
        )
        db.session.add(contact)
        db.session.commit()
        flash('Tak for din besked! Vi vender tilbage hurtigst muligt.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# ============================================================================
# AUTHENTICATION
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Ugyldigt brugernavn eller adgangskode', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Brugernavn eksisterer allerede', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email er allerede registreret', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registrering gennemført! Du kan nu logge ind.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ============================================================================
# USER DASHBOARD (Protected)
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('Du har ikke adgang til denne side', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    pages = Page.query.all()
    contacts = ContactForm.query.order_by(ContactForm.submitted_at.desc()).all()
    
    return render_template('admin.html', users=users, pages=pages, contacts=contacts)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')

@app.cli.command()
def create_admin():
    """Create an admin user."""
    admin = User(username='admin', email='admin@vidensbank.dk', role='admin')
    admin.set_password('admin123')  # Change this in production!
    db.session.add(admin)
    db.session.commit()
    print('Admin user created! Username: admin, Password: admin123')

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
