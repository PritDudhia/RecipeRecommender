from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Recipe Recommender API is running'
    })

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes (placeholder)"""
    # TODO: Implement with database
    sample_recipes = [
        {
            'id': 1,
            'name': 'Spaghetti Carbonara',
            'cuisine': 'Italian',
            'ingredients': ['pasta', 'eggs', 'bacon', 'parmesan'],
            'difficulty': 'medium'
        },
        {
            'id': 2,
            'name': 'Chicken Stir Fry',
            'cuisine': 'Asian',
            'ingredients': ['chicken', 'vegetables', 'soy sauce', 'rice'],
            'difficulty': 'easy'
        }
    ]
    return jsonify(sample_recipes)

@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    """Recommend recipes based on ingredients"""
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    # TODO: Implement ML recommendation logic
    return jsonify({
        'message': 'Recommendation endpoint (to be implemented)',
        'input_ingredients': ingredients,
        'recommended_recipes': []
    })

@app.route('/api/substitute', methods=['POST'])
def find_substitutes():
    """Find ingredient substitutions"""
    data = request.get_json()
    ingredient = data.get('ingredient', '')
    
    # TODO: Implement substitution logic with Apriori
    return jsonify({
        'ingredient': ingredient,
        'substitutes': [],
        'message': 'Substitution endpoint (to be implemented)'
    })

if __name__ == '__main__':
    print("🚀 Starting Recipe Recommender Backend...")
    print("📍 API available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
