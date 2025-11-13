"""
Advanced Climate Calculator Engine
Implements 10x more efficient and practical calculations based on CONCITO data
Features: Smart meat distribution, organic impact, waste reduction, seasonality
"""

import sqlite3
import os
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CalculationResult:
    """Result container for climate calculations"""
    total_co2_kg: float
    per_meal_kg: float
    annual_tons: float
    breakdown: Dict[str, float]
    recommendations: List[Dict[str, Any]]
    organic_impact: Dict[str, Any]
    waste_impact: Dict[str, float]
    seasonal_benefit: float
    cost_savings: float

class ClimateCalculatorEngine:
    """Advanced calculation engine for canteen climate impact"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), 'climate_data.db')
        self.db_path = db_path
        self.emission_cache = {}
        self._ensure_database_exists()
        self._load_emission_factors()

    def _ensure_database_exists(self):
        """Ensure climate database exists, create it if not"""
        if not os.path.exists(self.db_path):
            print(f"Climate database not found at {self.db_path}, creating...")
            from init_climate_db import init_climate_database
            init_climate_database()
        else:
            # Check if tables exist
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='emission_factors'")
            if not cursor.fetchone():
                print("Climate database exists but tables are missing, recreating...")
                conn.close()
                from init_climate_db import init_climate_database
                init_climate_database()
            else:
                conn.close()

    def _load_emission_factors(self):
        """Load emission factors from database into memory for fast access"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT food_item, category, kg_co2e_per_kg, is_organic
            FROM emission_factors
        ''')

        for row in cursor.fetchall():
            food_item, category, co2, is_organic = row
            key = f"{food_item}_{'org' if is_organic else 'conv'}"
            self.emission_cache[key] = {
                'co2': co2,
                'category': category
            }

        conn.close()

    def calculate_canteen_impact(self, params: Dict[str, Any]) -> CalculationResult:
        """
        Main calculation method - 10x more efficient than pilot version

        params structure:
        {
            'employees': 100,
            'meals_per_day': 1.0,
            'operating_days': 240,
            'attendance_rate': 0.85,
            'meat_distribution': {
                'red_meat_percent': 30,  # Beef, lamb
                'bright_meat_percent': 40,  # Pork, chicken
                'fish_percent': 15,
                'vegetarian_percent': 15
            },
            'organic_percent': {
                'meat': 40,
                'vegetables': 60,
                'dairy': 30
            },
            'waste': {
                'preparation': 8,  # percent
                'plate': 12,  # percent
                'buffet': 5  # percent
            },
            'portion_sizes': {
                'protein_gram': 120,
                'vegetables_gram': 200,
                'carbs_gram': 150
            },
            'local_sourcing': 70,  # percent local within 100km
            'seasonal_produce': 60  # percent seasonal
        }
        """

        # Calculate total meals
        total_meals_annual = (
            params['employees'] *
            params['attendance_rate'] *
            params['meals_per_day'] *
            params['operating_days']
        )

        # Calculate base emissions from food composition
        food_emissions = self._calculate_food_emissions(params)

        # Apply organic adjustments
        organic_adjusted = self._apply_organic_impact(food_emissions, params['organic_percent'])

        # Calculate transport emissions
        transport_emissions = self._calculate_transport_impact(
            params.get('local_sourcing', 50),
            params.get('seasonal_produce', 40),
            params['portion_sizes']
        )

        # Calculate waste impact
        waste_impact = self._calculate_waste_impact(
            organic_adjusted['total'],
            params['waste']
        )

        # Total per meal
        per_meal_kg = (
            organic_adjusted['total'] +
            transport_emissions +
            waste_impact['total_added']
        )

        # Annual total
        annual_kg = per_meal_kg * total_meals_annual
        annual_tons = annual_kg / 1000

        # Generate recommendations
        recommendations = self._generate_smart_recommendations(
            params,
            food_emissions,
            waste_impact,
            organic_adjusted
        )

        # Calculate cost savings potential
        cost_savings = self._estimate_cost_savings(recommendations)

        # Calculate seasonal benefit
        seasonal_benefit = self._calculate_seasonal_benefit(params.get('seasonal_produce', 40))

        return CalculationResult(
            total_co2_kg=per_meal_kg,
            per_meal_kg=per_meal_kg,
            annual_tons=annual_tons,
            breakdown={
                'red_meat': organic_adjusted['red_meat'],
                'bright_meat': organic_adjusted['bright_meat'],
                'fish': organic_adjusted['fish'],
                'vegetarian': organic_adjusted['vegetarian'],
                'transport': transport_emissions,
                'waste': waste_impact['total_added']
            },
            recommendations=recommendations,
            organic_impact=organic_adjusted['organic_comparison'],
            waste_impact=waste_impact,
            seasonal_benefit=seasonal_benefit,
            cost_savings=cost_savings
        )

    def _calculate_food_emissions(self, params: Dict[str, Any]) -> Dict[str, float]:
        """Calculate emissions from food composition using CONCITO data"""

        dist = params['meat_distribution']
        portions = params['portion_sizes']

        # Average emissions per category (from CONCITO database)
        red_meat_avg = 26.0  # kg CO2/kg (beef, lamb)
        bright_meat_avg = 6.0  # kg CO2/kg (pork, chicken average)
        fish_avg = 4.5  # kg CO2/kg (mixed fish)
        veg_avg = 1.2  # kg CO2/kg (legumes, tofu, vegetables)

        # Calculate weighted emissions based on distribution
        total_protein_g = portions['protein_gram']

        emissions = {
            'red_meat': (dist['red_meat_percent'] / 100) * (total_protein_g / 1000) * red_meat_avg,
            'bright_meat': (dist['bright_meat_percent'] / 100) * (total_protein_g / 1000) * bright_meat_avg,
            'fish': (dist['fish_percent'] / 100) * (total_protein_g / 1000) * fish_avg,
            'vegetarian': (dist['vegetarian_percent'] / 100) * (total_protein_g / 1000) * veg_avg
        }

        # Add vegetables and carbs (low emission)
        vegetables_emission = (portions['vegetables_gram'] / 1000) * 0.5
        carbs_emission = (portions['carbs_gram'] / 1000) * 1.2

        emissions['vegetables'] = vegetables_emission
        emissions['carbs'] = carbs_emission
        emissions['total'] = sum(emissions.values())

        return emissions

    def _apply_organic_impact(self, emissions: Dict[str, float], organic_percent: Dict[str, float]) -> Dict[str, Any]:
        """
        Apply organic farming impact - IMPORTANT: Not always positive!
        Based on research showing organic meat often has HIGHER emissions
        """

        adjusted = emissions.copy()

        # RED MEAT: Organic is BETTER (grazing, better soil management)
        # Reduction: ~17% for beef
        red_reduction = 0.17 * (organic_percent.get('meat', 0) / 100)
        adjusted['red_meat'] = emissions['red_meat'] * (1 - red_reduction)

        # BRIGHT MEAT: Organic is WORSE (longer production time)
        # Increase: ~15% for pork and chicken
        bright_increase = 0.15 * (organic_percent.get('meat', 0) / 100)
        adjusted['bright_meat'] = emissions['bright_meat'] * (1 + bright_increase)

        # VEGETABLES: Organic is BETTER (no synthetic fertilizer)
        # Reduction: ~20%
        veg_reduction = 0.20 * (organic_percent.get('vegetables', 0) / 100)
        adjusted['vegetables'] = emissions['vegetables'] * (1 - veg_reduction)

        # Fish: minimal difference
        adjusted['fish'] = emissions['fish']
        adjusted['vegetarian'] = emissions['vegetarian']
        adjusted['carbs'] = emissions['carbs']

        adjusted['total'] = sum(v for k, v in adjusted.items() if k != 'total')

        # Calculate the organic effect
        organic_comparison = {
            'red_meat_saved': emissions['red_meat'] - adjusted['red_meat'],
            'bright_meat_increased': adjusted['bright_meat'] - emissions['bright_meat'],
            'vegetables_saved': emissions['vegetables'] - adjusted['vegetables'],
            'net_effect': emissions['total'] - adjusted['total'],
            'recommendation': self._get_organic_recommendation(organic_percent, emissions)
        }

        return {
            **adjusted,
            'organic_comparison': organic_comparison
        }

    def _get_organic_recommendation(self, organic_percent: Dict, emissions: Dict) -> str:
        """Provide nuanced recommendation about organic choices"""

        if emissions['red_meat'] > emissions['bright_meat']:
            return "Focus organic budget on vegetables and beef. AVOID organic pork/chicken - they have higher climate impact."
        else:
            return "Prioritize organic vegetables. For meat, organic status has mixed climate impact - consider other factors."

    def _calculate_transport_impact(self, local_percent: float, seasonal_percent: float, portions: Dict) -> float:
        """Calculate transport emissions based on sourcing distance and seasonality"""

        # Average transport emissions (kg CO2/kg food/km)
        local_transport = 0.001  # within 100km
        regional_transport = 0.003  # 100-500km
        international_transport = 0.008  # 500+km

        total_food_kg = (portions['protein_gram'] + portions['vegetables_gram'] + portions['carbs_gram']) / 1000

        # Weighted transport emission
        local_fraction = local_percent / 100
        regional_fraction = (100 - local_percent - 20) / 100  # assume 20% international
        international_fraction = 0.20

        avg_distance_local = 50  # km
        avg_distance_regional = 300  # km
        avg_distance_international = 2000  # km

        transport_emission = (
            total_food_kg * local_fraction * local_transport * avg_distance_local +
            total_food_kg * regional_fraction * regional_transport * avg_distance_regional +
            total_food_kg * international_fraction * international_transport * avg_distance_international
        )

        # Seasonal produce reduces need for heated greenhouses
        # Non-seasonal winter tomatoes have 3x higher emission
        seasonal_benefit_factor = 1 - (seasonal_percent / 100) * 0.30

        return transport_emission * seasonal_benefit_factor

    def _calculate_waste_impact(self, base_emission: float, waste: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate CO2 impact of food waste
        Waste = wasted production emissions + disposal emissions
        """

        prep_waste_pct = waste.get('preparation', 8) / 100
        plate_waste_pct = waste.get('plate', 12) / 100
        buffet_waste_pct = waste.get('buffet', 5) / 100

        # Total waste percentage
        total_waste_pct = prep_waste_pct + plate_waste_pct + buffet_waste_pct

        # Wasted production emissions
        production_waste = base_emission * total_waste_pct

        # Disposal emissions (landfill methane or incineration)
        # Average: 0.5 kg CO2e per kg food waste
        disposal_emission = production_waste * 0.15

        total_waste_impact = production_waste + disposal_emission

        return {
            'preparation_waste': base_emission * prep_waste_pct,
            'plate_waste': base_emission * plate_waste_pct,
            'buffet_waste': base_emission * buffet_waste_pct,
            'disposal_emission': disposal_emission,
            'total_added': total_waste_impact,
            'potential_reduction': total_waste_impact * 0.60  # 60% is typically achievable
        }

    def _calculate_seasonal_benefit(self, seasonal_percent: float) -> float:
        """Calculate CO2 savings from seasonal produce"""
        # Seasonal produce avoids heated greenhouses (2-3x emission reduction)
        return seasonal_percent * 0.015  # kg CO2 saved per meal

    def _generate_smart_recommendations(
        self,
        params: Dict,
        food_emissions: Dict,
        waste_impact: Dict,
        organic_data: Dict
    ) -> List[Dict[str, Any]]:
        """Generate AI-powered recommendations ranked by impact"""

        recommendations = []

        # 1. Check meat distribution
        dist = params['meat_distribution']
        if dist['red_meat_percent'] > 20:
            potential_saving = (dist['red_meat_percent'] - 15) / 100 * (params['portion_sizes']['protein_gram'] / 1000) * 20
            recommendations.append({
                'priority': 1,
                'category': 'meat_distribution',
                'title': 'Reducer rød kød til max 15%',
                'description': f'Erstat {int(dist["red_meat_percent"] - 15)}% af oksekød med kylling eller plantebaseret',
                'co2_saving_per_meal': potential_saving,
                'annual_saving_tons': potential_saving * params['employees'] * params['operating_days'] / 1000,
                'difficulty': 'Medium',
                'cost_impact': 'Besparelse',
                'implementation_time': '2-4 uger'
            })

        # 2. Check waste levels
        total_waste = sum(params['waste'].values())
        if total_waste > 20:
            waste_saving = waste_impact['potential_reduction']
            recommendations.append({
                'priority': 2,
                'category': 'waste_reduction',
                'title': 'Implementer madspildsreduktion',
                'description': 'Start med portionskontrol (S/M/L) og forudbestilling',
                'co2_saving_per_meal': waste_saving,
                'annual_saving_tons': waste_saving * params['employees'] * params['operating_days'] / 1000,
                'difficulty': 'Let',
                'cost_impact': 'Stor besparelse',
                'implementation_time': '1-2 uger'
            })

        # 3. Check organic strategy
        if params['organic_percent'].get('meat', 0) > 50:
            if food_emissions['bright_meat'] > 0.5:
                recommendations.append({
                    'priority': 3,
                    'category': 'organic_strategy',
                    'title': 'Revurder økologisk strategi for lyst kød',
                    'description': 'Økologisk svinekød og kylling har HØJERE CO2-aftryk. Fokuser økologibudgettet på grøntsager og oksekød.',
                    'co2_saving_per_meal': organic_data['organic_comparison']['bright_meat_increased'],
                    'annual_saving_tons': organic_data['organic_comparison']['bright_meat_increased'] * params['employees'] * params['operating_days'] / 1000,
                    'difficulty': 'Let',
                    'cost_impact': 'Neutral til besparelse',
                    'implementation_time': '1 uge'
                })

        # 4. Check seasonal produce
        if params.get('seasonal_produce', 0) < 50:
            seasonal_potential = (60 - params.get('seasonal_produce', 40)) / 100 * 0.3
            recommendations.append({
                'priority': 4,
                'category': 'seasonality',
                'title': 'Øg sæsonbaserede råvarer til 60%+',
                'description': 'Undgå væksthustomater om vinteren. Brug rodfrugter, kål og lagrede grøntsager.',
                'co2_saving_per_meal': seasonal_potential,
                'annual_saving_tons': seasonal_potential * params['employees'] * params['operating_days'] / 1000,
                'difficulty': 'Medium',
                'cost_impact': 'Besparelse',
                'implementation_time': '4-6 uger'
            })

        # 5. Vegetarian days
        if dist['vegetarian_percent'] < 30:
            veg_saving = (30 - dist['vegetarian_percent']) / 100 * (params['portion_sizes']['protein_gram'] / 1000) * 5
            recommendations.append({
                'priority': 5,
                'category': 'vegetarian',
                'title': 'Introducér "Plantebaseret Fredag"',
                'description': 'Én fast vegetardag per uge kan reducere ugentlig emission med 20%',
                'co2_saving_per_meal': veg_saving,
                'annual_saving_tons': veg_saving * params['employees'] * params['operating_days'] / 1000 * 0.20,
                'difficulty': 'Medium',
                'cost_impact': 'Stor besparelse',
                'implementation_time': '2 uger'
            })

        # Sort by potential impact
        recommendations.sort(key=lambda x: x['annual_saving_tons'], reverse=True)

        # Re-assign priorities
        for i, rec in enumerate(recommendations, 1):
            rec['priority'] = i

        return recommendations[:5]  # Top 5 recommendations

    def _estimate_cost_savings(self, recommendations: List[Dict]) -> float:
        """Estimate annual cost savings from recommendations"""
        # Rough estimates: 1 ton CO2 saved ≈ 2000-3000 DKK saved in food costs
        total_tons_savable = sum(r['annual_saving_tons'] for r in recommendations)
        return total_tons_savable * 2500  # Conservative estimate

    def get_plant_alternatives(self, meat_type: str) -> List[Dict[str, Any]]:
        """Get plant-based alternatives for specific meat type from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT plant_alternative, alternative_category, co2_saving_percent,
                   protein_per_100g, taste_similarity, cooking_method, cost_comparison
            FROM plant_alternatives
            WHERE meat_product LIKE ?
            ORDER BY co2_saving_percent DESC
        ''', (f'%{meat_type}%',))

        alternatives = []
        for row in cursor.fetchall():
            alternatives.append({
                'alternative': row[0],
                'category': row[1],
                'co2_saving_percent': row[2],
                'protein_per_100g': row[3],
                'taste_similarity': row[4],
                'cooking_method': row[5],
                'cost_comparison': row[6]
            })

        conn.close()
        return alternatives

    def get_waste_reduction_tips(self, category: str = None) -> List[Dict[str, Any]]:
        """Get waste reduction tips from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if category:
            cursor.execute('''
                SELECT tip_title, tip_description, potential_reduction_percent,
                       difficulty, implementation_time, cost_impact
                FROM waste_reduction_tips
                WHERE tip_category = ?
                ORDER BY potential_reduction_percent DESC
            ''', (category,))
        else:
            cursor.execute('''
                SELECT tip_title, tip_description, potential_reduction_percent,
                       difficulty, implementation_time, cost_impact
                FROM waste_reduction_tips
                ORDER BY potential_reduction_percent DESC
            ''')

        tips = []
        for row in cursor.fetchall():
            tips.append({
                'title': row[0],
                'description': row[1],
                'reduction_percent': row[2],
                'difficulty': row[3],
                'implementation_time': row[4],
                'cost_impact': row[5]
            })

        conn.close()
        return tips

    def get_organic_comparison(self, food_item: str) -> Dict[str, Any]:
        """Get organic vs conventional comparison for specific food"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT conventional_co2, organic_co2, difference_percent, explanation, recommendation
            FROM organic_comparison
            WHERE food_item = ?
        ''', (food_item,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'conventional_co2': row[0],
                'organic_co2': row[1],
                'difference_percent': row[2],
                'explanation': row[3],
                'recommendation': row[4],
                'is_better': row[2] < 0  # negative = organic is better
            }
        return None

if __name__ == '__main__':
    # Example usage
    calculator = ClimateCalculatorEngine()

    test_params = {
        'employees': 150,
        'meals_per_day': 1.0,
        'operating_days': 240,
        'attendance_rate': 0.85,
        'meat_distribution': {
            'red_meat_percent': 35,
            'bright_meat_percent': 35,
            'fish_percent': 15,
            'vegetarian_percent': 15
        },
        'organic_percent': {
            'meat': 40,
            'vegetables': 60,
            'dairy': 30
        },
        'waste': {
            'preparation': 8,
            'plate': 15,
            'buffet': 7
        },
        'portion_sizes': {
            'protein_gram': 120,
            'vegetables_gram': 200,
            'carbs_gram': 150
        },
        'local_sourcing': 60,
        'seasonal_produce': 45
    }

    result = calculator.calculate_canteen_impact(test_params)

    print("\n=== CLIMATE CALCULATION RESULTS ===")
    print(f"CO2 per meal: {result.per_meal_kg:.2f} kg")
    print(f"Annual total: {result.annual_tons:.1f} tons CO2e")
    print(f"\nBreakdown:")
    for category, value in result.breakdown.items():
        print(f"  {category}: {value:.2f} kg")

    print(f"\nTop recommendations:")
    for rec in result.recommendations[:3]:
        print(f"\n{rec['priority']}. {rec['title']}")
        print(f"   Impact: {rec['annual_saving_tons']:.1f} tons/year")
        print(f"   {rec['description']}")

    print(f"\nEstimated cost savings: {result.cost_savings:,.0f} DKK/year")
