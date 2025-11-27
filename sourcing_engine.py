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
            
            # Calculate Scores for DK and Import
            dk_score = self._calculate_score(
                price=month_data.get('dk_price', 0),
                quality=month_data.get('dk_quality', 0),
                climate=1, # DK is baseline climate (1)
                is_local=True
            )
            
            import_score = self._calculate_score(
                price=month_data.get('import_price', 0),
                quality=month_data.get('import_quality', 0),
                climate=2 if month_data.get('import_origin') == 'EU' else 3,
                is_local=False
            )

            # Determine Recommendation
            if dk_score >= import_score and month_data.get('dk_status') != 'Ude':
                rec_origin = 'DK'
                rec_status = month_data.get('dk_status')
                rec_price = month_data.get('dk_price')
                rec_quality = month_data.get('dk_quality')
                rec_climate = 1
                score = dk_score
                is_import = False
            else:
                rec_origin = month_data.get('import_origin', 'World')
                rec_status = 'Import'
                rec_price = month_data.get('import_price')
                rec_quality = month_data.get('import_quality')
                rec_climate = 2 if rec_origin == 'EU' else 3
                score = import_score
                is_import = True

            recommendations.append({
                'id': item_key,
                'name': item_data['name'],
                'category': item_data['category'],
                'origin': rec_origin,
                'status': rec_status,
                'price': rec_price,
                'climate': rec_climate,
                'quality': rec_quality,
                'score': round(score * 100),
                'is_import': is_import
            })

        # Sort by score descending
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)

    def _calculate_score(self, price, quality, climate, is_local):
        """
        Calculates a score from 0 to 1 based on weighted factors.
        """
        if price == 0 or quality == 0: return 0 # Unavailable

        # Normalize inputs (assuming 1-3 scale)
        # Price: 1 is best (1.0), 3 is worst (0.0)
        norm_price = (3 - price) / 2
        
        # Quality: 3 is best (1.0), 1 is worst (0.0)
        norm_quality = (quality - 1) / 2
        
        # Climate: 1 is best (1.0), 3 is worst (0.0)
        norm_climate = (3 - climate) / 2

        # Weights
        w_price = 0.4
        w_quality = 0.4
        w_climate = 0.2

        # Bonus for local if quality is comparable
        local_bonus = 0.1 if is_local else 0

        total_score = (norm_price * w_price) + (norm_quality * w_quality) + (norm_climate * w_climate) + local_bonus
        
        return min(total_score, 1.0) # Cap at 1.0
