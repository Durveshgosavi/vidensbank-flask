from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys

# Import advanced climate calculator
sys.path.append(os.path.join(os.path.dirname(__file__), 'climate_data'))
from calculator_engine import ClimateCalculatorEngine
import sqlite3

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
# EMISSIONS TOPIC ROUTES (New Structure)
# ============================================================================

@app.route('/vidensbank/emissioner')
def topic_emissions_landing():
    """Emissions topic landing page"""
    return render_template('topics/emissions/landing.html')

@app.route('/vidensbank/emissioner/hvad-er-det')
def topic_emissions_what():
    """What are food-related emissions?"""
    return render_template('topics/emissions/what.html')

@app.route('/vidensbank/emissioner/hvorfor-vigtigt')
def topic_emissions_why():
    """Why are emissions important?"""
    return render_template('topics/emissions/why.html')

@app.route('/vidensbank/emissioner/maal-og-ambition')
def topic_emissions_goal():
    """Goals and ambitions"""
    return render_template('topics/emissions/goal.html')

@app.route('/vidensbank/emissioner/mit-aftryk')
def topic_emissions_impact():
    """What is my impact?"""
    return render_template('topics/emissions/impact.html')

@app.route('/vidensbank/emissioner/tips-og-tricks')
def topic_emissions_tips():
    """Tips and tricks"""
    return render_template('topics/emissions/tips.html')

# ============================================================================
# ERNÆRING TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/ernaering')
def topic_ernaering_landing():
    """Ernæring topic landing page"""
    return render_template('topics/ernaering/landing.html')

@app.route('/vidensbank/ernaering/hvad-er-det')
def topic_ernaering_what():
    """What is Ernæring?"""
    return render_template('topics/ernaering/what.html')

@app.route('/vidensbank/ernaering/hvorfor-vigtigt')
def topic_ernaering_why():
    """Why Ernæring matters"""
    return render_template('topics/ernaering/why.html')

@app.route('/vidensbank/ernaering/maal-og-ambition')
def topic_ernaering_goal():
    """Goals and ambitions for Ernæring"""
    return render_template('topics/ernaering/goal.html')

@app.route('/vidensbank/ernaering/mit-aftryk')
def topic_ernaering_impact():
    """Impact for Ernæring"""
    return render_template('topics/ernaering/impact.html')

@app.route('/vidensbank/ernaering/tips-og-tricks')
def topic_ernaering_tips():
    """Tips and tricks for Ernæring"""
    return render_template('topics/ernaering/tips.html')

# ============================================================================
# ØKOLOGI TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/okologi')
def topic_okologi_landing():
    """Økologi topic landing page"""
    return render_template('topics/okologi/landing.html')

@app.route('/vidensbank/okologi/hvad-er-det')
def topic_okologi_what():
    """What is Økologi?"""
    return render_template('topics/okologi/what.html')

@app.route('/vidensbank/okologi/hvorfor-vigtigt')
def topic_okologi_why():
    """Why Økologi matters"""
    return render_template('topics/okologi/why.html')

@app.route('/vidensbank/okologi/maal-og-ambition')
def topic_okologi_goal():
    """Goals and ambitions for Økologi"""
    return render_template('topics/okologi/goal.html')

@app.route('/vidensbank/okologi/mit-aftryk')
def topic_okologi_impact():
    """Impact for Økologi"""
    return render_template('topics/okologi/impact.html')

@app.route('/vidensbank/okologi/tips-og-tricks')
def topic_okologi_tips():
    """Tips and tricks for Økologi"""
    return render_template('topics/okologi/tips.html')

# ============================================================================
# VANDFORBRUG TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/vandforbrug')
def topic_vandforbrug_landing():
    """Vandforbrug topic landing page"""
    return render_template('topics/vandforbrug/landing.html')

@app.route('/vidensbank/vandforbrug/hvad-er-det')
def topic_vandforbrug_what():
    """What is Vandforbrug?"""
    return render_template('topics/vandforbrug/what.html')

@app.route('/vidensbank/vandforbrug/hvorfor-vigtigt')
def topic_vandforbrug_why():
    """Why Vandforbrug matters"""
    return render_template('topics/vandforbrug/why.html')

@app.route('/vidensbank/vandforbrug/maal-og-ambition')
def topic_vandforbrug_goal():
    """Goals and ambitions for Vandforbrug"""
    return render_template('topics/vandforbrug/goal.html')

@app.route('/vidensbank/vandforbrug/mit-aftryk')
def topic_vandforbrug_impact():
    """Impact for Vandforbrug"""
    return render_template('topics/vandforbrug/impact.html')

@app.route('/vidensbank/vandforbrug/tips-og-tricks')
def topic_vandforbrug_tips():
    """Tips and tricks for Vandforbrug"""
    return render_template('topics/vandforbrug/tips.html')

# ============================================================================
# MADSPILD TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/madspild')
def topic_madspild_landing():
    """Madspild topic landing page"""
    return render_template('topics/madspild/landing.html')

@app.route('/vidensbank/madspild/hvad-er-det')
def topic_madspild_what():
    """What is Madspild?"""
    return render_template('topics/madspild/what.html')

@app.route('/vidensbank/madspild/hvorfor-vigtigt')
def topic_madspild_why():
    """Why Madspild matters"""
    return render_template('topics/madspild/why.html')

@app.route('/vidensbank/madspild/maal-og-ambition')
def topic_madspild_goal():
    """Goals and ambitions for Madspild"""
    return render_template('topics/madspild/goal.html')

@app.route('/vidensbank/madspild/mit-aftryk')
def topic_madspild_impact():
    """Impact for Madspild"""
    return render_template('topics/madspild/impact.html')

@app.route('/vidensbank/madspild/tips-og-tricks')
def topic_madspild_tips():
    """Tips and tricks for Madspild"""
    return render_template('topics/madspild/tips.html')

# ============================================================================
# TOOLS & CASES ROUTES (All Topics)
# ============================================================================

# Emissioner Tools & Cases
@app.route('/vidensbank/emissioner/tools')
def topic_emissions_tools():
    """Tools for Emissions topic"""
    return render_template('topics/emissions/tools.html')

@app.route('/vidensbank/emissioner/cases')
def topic_emissions_cases():
    """Cases for Emissions topic"""
    return render_template('topics/emissions/cases.html')

# Ernæring Tools & Cases
@app.route('/vidensbank/ernaering/tools')
def topic_ernaering_tools():
    """Tools for Ernæring topic"""
    return render_template('topics/ernaering/tools.html')

@app.route('/vidensbank/ernaering/cases')
def topic_ernaering_cases():
    """Cases for Ernæring topic"""
    return render_template('topics/ernaering/cases.html')

# Økologi Tools & Cases
@app.route('/vidensbank/okologi/tools')
def topic_okologi_tools():
    """Tools for Økologi topic"""
    return render_template('topics/okologi/tools.html')

@app.route('/vidensbank/okologi/cases')
def topic_okologi_cases():
    """Cases for Økologi topic"""
    return render_template('topics/okologi/cases.html')

# Vandforbrug Tools & Cases
@app.route('/vidensbank/vandforbrug/tools')
def topic_vandforbrug_tools():
    """Tools for Vandforbrug topic"""
    return render_template('topics/vandforbrug/tools.html')

@app.route('/vidensbank/vandforbrug/cases')
def topic_vandforbrug_cases():
    """Cases for Vandforbrug topic"""
    return render_template('topics/vandforbrug/cases.html')

# Madspild Tools & Cases
@app.route('/vidensbank/madspild/tools')
def topic_madspild_tools():
    """Tools for Madspild topic"""
    return render_template('topics/madspild/tools.html')

@app.route('/vidensbank/madspild/cases')
def topic_madspild_cases():
    """Cases for Madspild topic"""
    return render_template('topics/madspild/cases.html')

# ============================================================================
# RÅVARER (PRODUCTS) SECTION ROUTES
# ============================================================================

@app.route('/vidensbank/raavarer')
def products_overview():
    """Products database overview"""
    return render_template('products/overview.html')

# Meat Products
@app.route('/vidensbank/raavarer/oksekoed')
def product_oksekoed():
    """Beef product page"""
    return render_template('products/oksekoed.html')

@app.route('/vidensbank/raavarer/svinekoed')
def product_svinekoed():
    """Pork product page"""
    return render_template('products/svinekoed.html')

@app.route('/vidensbank/raavarer/fjerkreae')
def product_fjerkreae():
    """Poultry product page"""
    return render_template('products/fjerkreae.html')

@app.route('/vidensbank/raavarer/lam')
def product_lam():
    """Lamb product page"""
    return render_template('products/lam.html')

# Fish and Seafood
@app.route('/vidensbank/raavarer/fisk-skalddyr')
def product_fisk():
    """Fish and seafood overview"""
    return render_template('products/fisk-skalddyr.html')

# Dairy and Eggs
@app.route('/vidensbank/raavarer/mejeriprodukter')
def product_dairy():
    """Dairy products page"""
    return render_template('products/mejeriprodukter.html')

@app.route('/vidensbank/raavarer/aeg')
def product_eggs():
    """Eggs product page"""
    return render_template('products/aeg.html')

# Plant-Based
@app.route('/vidensbank/raavarer/korn-pasta')
def product_grains():
    """Grains and pasta page"""
    return render_template('products/korn-pasta.html')

@app.route('/vidensbank/raavarer/groentstager')
def product_vegetables():
    """Vegetables page"""
    return render_template('products/groentstager.html')

@app.route('/vidensbank/raavarer/frugt-baer')
def product_fruits():
    """Fruits and berries page"""
    return render_template('products/frugt-baer.html')

# Commodities
@app.route('/vidensbank/raavarer/kaffe-te-kakao')
def product_beverages():
    """Coffee, tea, cocoa page"""
    return render_template('products/kaffe-te-kakao.html')

@app.route('/vidensbank/raavarer/olier-fedt')
def product_oils():
    """Oils and fats page"""
    return render_template('products/olier-fedt.html')

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
# ADVANCED CO2 CALCULATOR
# ============================================================================

# Initialize calculator engine
calculator_engine = ClimateCalculatorEngine()

# Helper function for climate database access
def get_climate_db():
    """Get connection to climate database"""
    db_path = os.path.join(os.path.dirname(__file__), 'climate_data', 'climate_data.db')
    return sqlite3.connect(db_path)

@app.route('/calculator')
def calculator():
    """Basic climate calculator page"""
    return render_template('calculator.html')

@app.route('/calculator-advanced')
def calculator_advanced():
    """Advanced canteen climate analysis tool with 70+ canteens"""
    return render_template('calculator_advanced.html')

@app.route('/api/calculate-canteen-impact', methods=['POST'])
def calculate_canteen_impact():
    """
    Advanced API endpoint for complete canteen climate impact calculation
    Expects JSON payload with canteen parameters
    """
    try:
        data = request.json

        # Validate required fields
        required_fields = ['employees', 'meat_distribution', 'portion_sizes']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Set defaults for optional fields
        params = {
            'employees': int(data['employees']),
            'meals_per_day': float(data.get('meals_per_day', 1.0)),
            'operating_days': int(data.get('operating_days', 240)),
            'attendance_rate': float(data.get('attendance_rate', 0.85)),
            'meat_distribution': data['meat_distribution'],
            'organic_percent': data.get('organic_percent', {
                'meat': 40,
                'vegetables': 60,
                'dairy': 30
            }),
            'waste': data.get('waste', {
                'preparation': 8,
                'plate': 12,
                'buffet': 5
            }),
            'portion_sizes': data['portion_sizes'],
            'local_sourcing': float(data.get('local_sourcing', 60)),
            'seasonal_produce': float(data.get('seasonal_produce', 50))
        }

        # Calculate impact
        result = calculator_engine.calculate_canteen_impact(params)

        # Format response
        return jsonify({
            'success': True,
            'results': {
                'per_meal_kg': round(result.per_meal_kg, 2),
                'annual_tons': round(result.annual_tons, 1),
                'breakdown': {k: round(v, 2) for k, v in result.breakdown.items()},
                'recommendations': result.recommendations,
                'organic_impact': {
                    'net_effect_kg': round(result.organic_impact['net_effect'], 2),
                    'recommendation': result.organic_impact['recommendation']
                },
                'waste_impact': {
                    'total_added_kg': round(result.waste_impact['total_added'], 2),
                    'potential_reduction_kg': round(result.waste_impact['potential_reduction'], 2)
                },
                'seasonal_benefit_kg': round(result.seasonal_benefit, 2),
                'estimated_cost_savings_dkk': round(result.cost_savings, 0)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/plant-alternatives/<meat_type>', methods=['GET'])
def get_plant_alternatives(meat_type):
    """Get plant-based alternatives for specific meat type"""
    try:
        alternatives = calculator_engine.get_plant_alternatives(meat_type)
        return jsonify({
            'success': True,
            'meat_type': meat_type,
            'alternatives': alternatives
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/waste-reduction-tips', methods=['GET'])
def get_waste_tips():
    """Get waste reduction tips"""
    try:
        category = request.args.get('category', None)
        tips = calculator_engine.get_waste_reduction_tips(category)
        return jsonify({
            'success': True,
            'tips': tips
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/organic-comparison/<food_item>', methods=['GET'])
def get_organic_comparison(food_item):
    """Get organic vs conventional comparison"""
    try:
        comparison = calculator_engine.get_organic_comparison(food_item)
        if comparison:
            return jsonify({
                'success': True,
                'comparison': comparison
            })
        else:
            return jsonify({
                'success': False,
                'error': f'No comparison data found for {food_item}'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# CANTEEN DATABASE ENDPOINTS
# ============================================================================

@app.route('/api/canteens', methods=['GET'])
def get_all_canteens():
    """Get all canteens from database"""
    try:
        conn = get_climate_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, location, address, co2_per_kg, green_percent,
                   meat_percent, organic_percent, food_waste_percent, local_sourced,
                   employees, meals_per_day, operating_days
            FROM canteens
            ORDER BY name
        ''')

        canteens = []
        for row in cursor.fetchall():
            canteens.append({
                'id': row[0],
                'name': row[1],
                'location': row[2],
                'address': row[3],
                'baseline': {
                    'co2_per_kg': row[4],
                    'green_percent': row[5],
                    'meat_percent': row[6],
                    'organic_percent': row[7],
                    'food_waste_percent': row[8],
                    'local_sourced': row[9]
                },
                'employees': row[10],
                'meals_per_day': row[11],
                'operating_days': row[12]
            })

        conn.close()

        return jsonify({
            'success': True,
            'count': len(canteens),
            'canteens': canteens
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/canteens/<int:canteen_id>', methods=['GET'])
def get_canteen(canteen_id):
    """Get specific canteen by ID"""
    try:
        conn = get_climate_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, location, address, co2_per_kg, green_percent,
                   meat_percent, organic_percent, food_waste_percent, local_sourced,
                   employees, meals_per_day, operating_days
            FROM canteens
            WHERE id = ?
        ''', (canteen_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            canteen = {
                'id': row[0],
                'name': row[1],
                'location': row[2],
                'address': row[3],
                'baseline': {
                    'co2_per_kg': row[4],
                    'green_percent': row[5],
                    'meat_percent': row[6],
                    'organic_percent': row[7],
                    'food_waste_percent': row[8],
                    'local_sourced': row[9]
                },
                'employees': row[10],
                'meals_per_day': row[11],
                'operating_days': row[12]
            }

            return jsonify({
                'success': True,
                'canteen': canteen
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Canteen not found'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
