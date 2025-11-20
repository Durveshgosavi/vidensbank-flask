import sqlite3
import os
import random

class MockDataService:
    """
    Simulates integration with Master Data systems (Power BI, Kok'pit, DealTrack).
    In reality, this fetches from our local SQLite database and adds some simulated
    granularity that might be missing (e.g. splitting 'meat' into red/white).
    """

    def __init__(self, db_path=None):
        if db_path is None:
            # Assuming running from app root
            self.db_path = os.path.join(os.getcwd(), 'climate_data', 'climate_data.db')
        else:
            self.db_path = db_path

    def _get_db_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_canteens(self):
        """Fetch list of all canteens for the dropdown"""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, location FROM canteens ORDER BY name")
        canteens = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return canteens

    def get_canteen_details(self, canteen_id):
        """
        Fetch detailed data for a specific canteen.
        Simulates fetching from Data Warehouse.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM canteens WHERE id = ?", (canteen_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        data = dict(row)

        # SIMULATION: Split generic "meat_percent" into specific categories
        # In a real scenario, this would come from purchase data (DealTrack)
        meat_pct = data.get('meat_percent', 20)
        
        # Simulate a typical split: 40% Red, 40% Bright, 20% Fish/Other
        # We'll add some randomness based on the ID to make it feel "real"
        random.seed(canteen_id) 
        red_ratio = random.uniform(0.3, 0.5)
        bright_ratio = random.uniform(0.3, 0.5)
        # Normalize to ensure we don't exceed 100% of the meat portion
        total_ratio = red_ratio + bright_ratio
        if total_ratio > 0.9:
            red_ratio *= 0.9 / total_ratio
            bright_ratio *= 0.9 / total_ratio
            
        red_meat_pct = meat_pct * red_ratio
        bright_meat_pct = meat_pct * bright_ratio
        fish_pct = meat_pct * (1 - red_ratio - bright_ratio)
        
        # Calculate vegetarian/plant-based rest
        # If green_percent is available use it, otherwise calculate
        green_pct = data.get('green_percent', 0)
        vegetarian_pct = 100 - red_meat_pct - bright_meat_pct - fish_pct
        
        # Adjust if we have specific green data
        if green_pct > 0:
             # Balance it out
             vegetarian_pct = green_pct

        return {
            'id': data['id'],
            'name': data['name'],
            'location': data['location'],
            'employees': data['employees'],
            'meals_per_day': data['meals_per_day'],
            'operating_days': data['operating_days'],
            'current_co2_per_kg': data['co2_per_kg'],
            'menu_composition': {
                'red_meat_percent': round(red_meat_pct, 1),
                'bright_meat_percent': round(bright_meat_pct, 1),
                'fish_percent': round(fish_pct, 1),
                'vegetarian_percent': round(vegetarian_pct, 1)
            },
            'organic_profile': {
                'total_percent': data['organic_percent'],
                # Simulated breakdown
                'meat_organic': min(data['organic_percent'] * 0.5, 100), 
                'vegetables_organic': min(data['organic_percent'] * 1.2, 100),
                'dairy_organic': min(data['organic_percent'] * 1.1, 100)
            },
            'sourcing': {
                'local_percent': data['local_sourced'],
                'seasonal_percent': data['local_sourced'] * 0.9 # Correlation assumption
            }
        }

    def get_waste_metrics(self, canteen_id):
        """
        Fetch waste data.
        Simulates integration with Kok'pit.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT food_waste_percent, meals_per_day FROM canteens WHERE id = ?", (canteen_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        total_waste_pct = row['food_waste_percent']
        
        # Simulate breakdown of waste (Prep vs Plate vs Buffet)
        # Typical industry split: 40% Prep, 40% Buffet, 20% Plate
        return {
            'total_waste_percent': total_waste_pct,
            'breakdown': {
                'preparation': round(total_waste_pct * 0.4, 1),
                'buffet': round(total_waste_pct * 0.4, 1),
                'plate': round(total_waste_pct * 0.2, 1)
            },
            'daily_kg_estimate': (row['meals_per_day'] * 0.5) * (total_waste_pct / 100) # Assuming 0.5kg meal
        }
