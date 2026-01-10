from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models.recipe_recommender import RecipeRecommender

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Initialize ML models
recipe_recommender = None

def init_models():
    """Initialize all ML models"""
    global recipe_recommender
    
    print("\n🤖 Initializing ML Models...")
    
    # Initialize Recipe Recommender
    recipe_recommender = RecipeRecommender()
    recipe_recommender.train()
    print("✅ Recipe recommendation model ready!")
    
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
    """Get all recipes"""
    try:
        recipes = recipe_recommender.get_all_recipes()
        return jsonify({
            'recipes': recipes,
            'total': len(recipes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/user/<int:user_id>', methods=['GET'])
def recommend_for_user(user_id):
    """
    Collaborative Filtering: Recommend recipes based on user preferences
    
    Args:
        user_id: User ID (0-9 for sample data)
    
    Query params:
        top_n: Number of recommendations (default: 5)
    """
    try:
        top_n = request.args.get('top_n', default=5, type=int)
        
        recommendations = recipe_recommender.get_user_based_recommendations(
            user_id=user_id,
            top_n=top_n
        )
        
        return jsonify({
            'user_id': user_id,
            'method': 'collaborative_filtering',
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/similar/<int:recipe_id>', methods=['GET'])
def recommend_similar_recipes(recipe_id):
    """
    Content-Based Filtering: Recommend similar recipes
    
    Args:
        recipe_id: Recipe ID (1-15 for sample data)
    
    Query params:
        top_n: Number of recommendations (default: 5)
    """
    try:
        top_n = request.args.get('top_n', default=5, type=int)
        
        # Get the base recipe
        base_recipe = recipe_recommender.get_recipe_by_id(recipe_id)
        if not base_recipe:
            return jsonify({'error': f'Recipe ID {recipe_id} not found'}), 404
        
        # Get similar recipes
        recommendations = recipe_recommender.get_content_based_recommendations(
            recipe_id=recipe_id,
            top_n=top_n
        )
        
        return jsonify({
            'base_recipe': base_recipe,
            'method': 'content_based_filtering',
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_recipes():
    """Recommend recipes based on ingredients (legacy endpoint)"""
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
