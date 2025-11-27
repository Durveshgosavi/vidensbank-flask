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

# Import PDF generator
from pdf_generator import PDFGenerator

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
    """Emissions - Tips & Tricks"""
    return render_template('topics/emissions/tips.html')

# --- Organic Topic Routes ---
@app.route('/vidensbank/okologi')
def topic_organic_landing():
    """Organic topic landing page"""
    return render_template('topics/organic/landing.html')

@app.route('/vidensbank/okologi/hvad-er-det')
def topic_organic_what():
    """Organic - What is it?"""
    return render_template('topics/organic/what.html')

@app.route('/vidensbank/okologi/hvorfor-er-det-vigtigt')
def topic_organic_why():
    """Organic - Why is it important?"""
    return render_template('topics/organic/why.html')

@app.route('/vidensbank/okologi/maal-og-ambition')
def topic_organic_goal():
    """Organic - Goal & Ambition"""
    return render_template('topics/organic/goal.html')

@app.route('/vidensbank/okologi/mit-aftryk')
def topic_organic_impact():
    """Organic - My Impact / Calculator"""
    return render_template('topics/organic/impact.html')

@app.route('/vidensbank/okologi/tips-og-tricks')
def topic_organic_tips():
    """Organic - Tips & Tricks"""
    return render_template('topics/organic/tips.html')

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

# Legacy Økologi routes removed in favor of new Organic topic structure
# See lines 140-170 for active routes

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

# PDF Download Route for Emissions
@app.route('/vidensbank/emissioner/download-pdf')
def emissions_download_pdf():
    """Generate and download PDF report for Emissions topic"""
    try:
        pdf_gen = PDFGenerator()
        return pdf_gen.generate_emissions_report()
    except Exception as e:
        flash(f'Der opstod en fejl ved generering af PDF: {str(e)}', 'error')
        return redirect(url_for('topic_emissions_landing'))

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
# RÅVARER (RAW MATERIALS) SECTION ROUTES
# ============================================================================

@app.route('/vidensbank/raavarer')
def raavarer_landing():
    """Raw materials landing page"""
    return render_template('raavarer/landing.html')

# Meat Products
@app.route('/vidensbank/raavarer/oksekoed')
def raavare_oksekoed():
    """Beef product page"""
    return render_template('raavarer/oksekoed.html')

@app.route('/vidensbank/raavarer/svinekoed')
def raavare_svinekoed():
    """Pork product page"""
    return render_template('raavarer/svinekoed.html')

@app.route('/vidensbank/raavarer/kylling')
def raavare_kylling():
    """Chicken product page"""
    return render_template('raavarer/kylling.html')

@app.route('/vidensbank/raavarer/lammekoed')
def raavare_lammekoed():
    """Lamb product page"""
    return render_template('raavarer/lammekoed.html')

# Fish and Seafood
@app.route('/vidensbank/raavarer/laks')
def raavare_laks():
    """Salmon product page"""
    return render_template('raavarer/laks.html')

@app.route('/vidensbank/raavarer/hvid-fisk')
def raavare_hvid_fisk():
    """White fish product page"""
    return render_template('raavarer/hvid-fisk.html')

@app.route('/vidensbank/raavarer/skaldyr')
def raavare_skaldyr():
    """Shellfish product page"""
    return render_template('raavarer/skaldyr.html')

# Dairy and Eggs
@app.route('/vidensbank/raavarer/maelk')
def raavare_maelk():
    """Milk and yogurt product page"""
    return render_template('raavarer/maelk.html')

@app.route('/vidensbank/raavarer/ost')
def raavare_ost():
    """Cheese product page"""
    return render_template('raavarer/ost.html')

@app.route('/vidensbank/raavarer/aeg')
def raavare_aeg():
    """Eggs product page"""
    return render_template('raavarer/aeg.html')

# Grains and Starch
@app.route('/vidensbank/raavarer/broed')
def raavare_broed():
    """Bread and flour product page"""
    return render_template('raavarer/broed.html')

@app.route('/vidensbank/raavarer/ris')
def raavare_ris():
    """Rice product page"""
    return render_template('raavarer/ris.html')

@app.route('/vidensbank/raavarer/kartofler')
def raavare_kartofler():
    """Potatoes product page"""
    return render_template('raavarer/kartofler.html')

# Vegetables and Legumes
@app.route('/vidensbank/raavarer/baelgfrugter')
def raavare_baelgfrugter():
    """Legumes product page"""
    return render_template('raavarer/baelgfrugter.html')

@app.route('/vidensbank/raavarer/rodfrugter')
def raavare_rodfrugter():
    """Root vegetables product page"""
    return render_template('raavarer/rodfrugter.html')

@app.route('/vidensbank/raavarer/bladgroent')
def raavare_bladgroent():
    """Leafy greens product page"""
    return render_template('raavarer/bladgroent.html')

# Specialty Items
@app.route('/vidensbank/raavarer/kaffe')
def raavare_kaffe():
    """Coffee product page"""
    return render_template('raavarer/kaffe.html')

@app.route('/vidensbank/raavarer/te')
def raavare_te():
    """Tea product page"""
    return render_template('raavarer/te.html')

@app.route('/vidensbank/raavarer/kakao')
def raavare_kakao():
    """Cocoa and chocolate product page"""
    return render_template('raavarer/kakao.html')

@app.route('/vidensbank/raavarer/olier')
def raavare_olier():
    """Oils and fats product page"""
    return render_template('raavarer/olier.html')

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

# ============================================================================
# BIODIVERSITET TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/biodiversitet')
def topic_biodiversity_landing():
    """Biodiversity topic landing page"""
    return render_template('topics/biodiversity/landing.html')

@app.route('/vidensbank/biodiversitet/hvad-er-det')
def topic_biodiversity_what():
    """Biodiversity - What is it?"""
    return render_template('topics/biodiversity/what.html')

@app.route('/vidensbank/biodiversitet/hvorfor-er-det-vigtigt')
def topic_biodiversity_why():
    """Biodiversity - Why is it important?"""
    return render_template('topics/biodiversity/why.html')

@app.route('/vidensbank/biodiversitet/maal-og-ambition')
def topic_biodiversity_goal():
    """Biodiversity - Goal & Ambition"""
    return render_template('topics/biodiversity/goal.html')

@app.route('/vidensbank/biodiversitet/mit-aftryk')
def topic_biodiversity_impact():
    """Biodiversity - My Impact"""
    return render_template('topics/biodiversity/impact.html')

@app.route('/vidensbank/biodiversitet/tips-og-tricks')
def topic_biodiversity_tips():
    """Biodiversity - Tips & Tricks"""
    return render_template('topics/biodiversity/tips.html')

# ============================================================================
# SÆSON TOPIC ROUTES
# ============================================================================

@app.route('/vidensbank/saeson')
def topic_saeson_landing():
    """Seasonality topic landing page"""
    return render_template('topics/saeson/landing.html')

@app.route('/vidensbank/saeson/hvad-er-det')
def topic_saeson_what():
    """Seasonality - What is it?"""
    return render_template('topics/saeson/what.html')

@app.route('/vidensbank/saeson/hvorfor-vigtigt')
def topic_saeson_why():
    """Seasonality - Why is it important?"""
    return render_template('topics/saeson/why.html')

@app.route('/vidensbank/saeson/maal-og-ambition')
def topic_saeson_goal():
    """Seasonality - Goal & Ambition"""
    return render_template('topics/saeson/goal.html')

@app.route('/vidensbank/saeson/mit-aftryk')
def topic_saeson_impact():
    """Seasonality - My Impact"""
    return render_template('topics/saeson/impact.html')

@app.route('/vidensbank/saeson/tips-og-tricks')
def topic_saeson_tips():
    """Seasonality - Tips & Tricks"""
    return render_template('topics/saeson/tips.html')

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
    """
    Main Climate Calculator
    Replaces the old basic calculator with the new comprehensive engine.
    """
    return render_template('calculators/comprehensive.html')

@app.route('/calculator/comprehensive')
def calculator_comprehensive():
    """Render the comprehensive calculator page."""
    return render_template('calculators/comprehensive.html')

@app.route('/api/canteens')
def api_canteens():
    """Get all canteens for dropdown."""
    canteens = mock_data_service.get_all_canteens()
    return jsonify(canteens)

@app.route('/api/canteen/<int:canteen_id>')
def api_canteen_details(canteen_id):
    """Get detailed data for a specific canteen."""
    details = mock_data_service.get_canteen_details(canteen_id)
    waste = mock_data_service.get_waste_metrics(canteen_id)
    
    if not details:
        return jsonify({'error': 'Canteen not found'}), 404
        
    return jsonify({
        'details': details,
        'waste': waste
    })

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """Run the climate calculation engine."""
    data = request.json
    
    # Transform frontend data to engine params structure if needed
    # For now assuming frontend sends correct structure matching ClimateCalculatorEngine.calculate_canteen_impact
    
    try:
        result = calculator_engine.calculate_canteen_impact(data)
        
        # Convert dataclass to dict for JSON serialization
        return jsonify({
            'total_co2_kg': result.total_co2_kg,
            'per_meal_kg': result.per_meal_kg,
            'annual_tons': result.annual_tons,
            'breakdown': result.breakdown,
            'recommendations': result.recommendations,
            'organic_impact': result.organic_impact,
            'waste_impact': result.waste_impact,
            'seasonal_benefit': result.seasonal_benefit,
            'cost_savings': result.cost_savings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
