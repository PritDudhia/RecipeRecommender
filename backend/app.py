from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models.cuisine_classifier import CuisineClassifier

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Initialize ML models
cuisine_classifier = None

def init_models():
    """Initialize all ML models"""
    global cuisine_classifier
    
    print("\n🤖 Initializing ML Models...")
    
    # Initialize Cuisine Classifier
    cuisine_classifier = CuisineClassifier(n_neighbors=5)
    cuisine_classifier.train()
    print("✅ Cuisine classifier ready!")
    
    print("\n✨ All models initialized successfully!\n")

# Initialize models on startup
init_models()

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

@app.route('/api/cuisine/predict', methods=['POST'])
def predict_cuisine():
    """Predict cuisine type from ingredients"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'No ingredients provided'
            }), 400
        
        result = cuisine_classifier.predict_cuisine(ingredients)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cuisine/stats', methods=['GET'])
def get_cuisine_stats():
    """Get cuisine classification statistics"""
    try:
        stats = cuisine_classifier.get_cuisine_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cuisine/list', methods=['GET'])
def get_cuisines():
    """Get list of all available cuisines"""
    try:
        cuisines = cuisine_classifier.get_all_cuisines()
        return jsonify({
            'success': True,
            'cuisines': cuisines,
            'total': len(cuisines)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Recipe Recommender Backend...")
    print("📍 API available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
