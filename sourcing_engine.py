import json
import os

class SourcingEngine:
    def __init__(self, data_path='data/sourcing_data.json'):
        self.data_path = os.path.join(os.path.dirname(__file__), data_path)
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.data_path}")
            return {}

    def get_monthly_recommendations(self, month_index):
        """
        Returns a list of items with calculated scores for the given month (0-11).
        """
        recommendations = []
        month_key = str(month_index)

        for item_key, item_data in self.data.items():
            if month_key not in item_data['months']:
                continue

            month_data = item_data['months'][month_key]
            co2_base = item_data.get('co2_base', 0.5) # Default fallback
            
            # Calculate Scores for DK and Import
            dk_co2 = self._calculate_co2(co2_base, 'DK')
            dk_score = self._calculate_score(
                price=month_data.get('dk_price', 0),
                quality=month_data.get('dk_quality', 0),
                co2=dk_co2,
                is_local=True
            )
            
            import_origin = month_data.get('import_origin', 'World')
            import_co2 = self._calculate_co2(co2_base, import_origin)
            import_score = self._calculate_score(
                price=month_data.get('import_price', 0),
                quality=month_data.get('import_quality', 0),
                co2=import_co2,
                is_local=False
            )

            # Determine Recommendation
            if dk_score >= import_score and month_data.get('dk_status') != 'Ude':
                rec_origin = 'DK'
                rec_status = month_data.get('dk_status')
                rec_price = month_data.get('dk_price')
                rec_quality = month_data.get('dk_quality')
                rec_co2 = dk_co2
                score = dk_score
                is_import = False
            else:
                rec_origin = import_origin
                rec_status = 'Import'
                rec_price = month_data.get('import_price')
                rec_quality = month_data.get('import_quality')
                rec_co2 = import_co2
                score = import_score
                is_import = True

            recommendations.append({
                'id': item_key,
                'name': item_data['name'],
                'category': item_data['category'],
                'origin': rec_origin,
                'status': rec_status,
                'price': rec_price,
                'co2': round(rec_co2, 2),
                'quality': rec_quality,
                'score': round(score * 100),
                'is_import': is_import
            })

        # Sort by score descending
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)

    def _calculate_co2(self, base_co2, origin):
        """
        Calculate total CO2 based on origin transport multipliers.
        """
        multipliers = {
            'DK': 1.0,
            'EU': 1.2,     # Truck transport
            'World': 1.5,  # Ship transport (avg)
            'N/A': 1.0
        }
        # Special case for air freight could be handled here if data supported it
        return base_co2 * multipliers.get(origin, 1.5)

    def _calculate_score(self, price, quality, co2, is_local):
        """
        Calculates a score from 0 to 1 based on weighted factors.
        """
        if price == 0 or quality == 0: return 0 # Unavailable

        # Normalize inputs
        # Price: 1 is best (1.0), 3 is worst (0.0)
        norm_price = (3 - price) / 2
        
        # Quality: 3 is best (1.0), 1 is worst (0.0)
        norm_quality = (quality - 1) / 2
        
        # CO2: Normalize against a reasonable max (e.g., 5.0 kg CO2e)
        # Lower is better. 0.1 -> 1.0, 5.0 -> 0.0
        norm_co2 = max(0, (5.0 - co2) / 5.0)

        # Weights
        w_price = 0.35
        w_quality = 0.45
        w_co2 = 0.20

        # Bonus for local if quality is comparable
        local_bonus = 0.1 if is_local else 0

        total_score = (norm_price * w_price) + (norm_quality * w_quality) + (norm_co2 * w_co2) + local_bonus
        
        return min(total_score, 1.0) # Cap at 1.0
