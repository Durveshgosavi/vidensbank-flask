
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from services.mock_data_service import MockDataService
from climate_data.calculator_engine import ClimateCalculatorEngine

def test_backend_logic():
    print("Testing Mock Data Service...")
    mock = MockDataService()
    canteens = mock.get_all_canteens()
    print(f"Found {len(canteens)} canteens.")
    
    if canteens:
        details = mock.get_canteen_details(canteens[0]['id'])
        print(f"Details for {details['name']}: Meat % = {details['menu_composition']}")
        
        waste = mock.get_waste_metrics(canteens[0]['id'])
        print(f"Waste metrics: {waste}")

    print("\nTesting Calculator Engine...")
    engine = ClimateCalculatorEngine()
    params = {
        'employees': 100,
        'meals_per_day': 1.0,
        'operating_days': 240,
        'attendance_rate': 0.85,
        'meat_distribution': {
            'red_meat_percent': 30,
            'bright_meat_percent': 30,
            'fish_percent': 20,
            'vegetarian_percent': 20
        },
        'organic_percent': {'meat': 50, 'vegetables': 50, 'dairy': 50},
        'waste': {'preparation': 10, 'plate': 10, 'buffet': 10},
        'portion_sizes': {'protein_gram': 120, 'vegetables_gram': 200, 'carbs_gram': 150},
        'local_sourcing': 50,
        'seasonal_produce': 50
    }
    
    result = engine.calculate_canteen_impact(params)
    print(f"Calculation Result: {result.annual_tons:.2f} tons CO2e/year")
    print(f"Recommendations: {len(result.recommendations)}")

if __name__ == "__main__":
    test_backend_logic()
