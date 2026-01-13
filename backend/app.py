from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models.ingredient_clustering import get_trained_model
from models.recipe_recommender import RecipeRecommender
from models.ingredient_substitution import IngredientSubstitutionFinder
from models.cuisine_classifier import CuisineClassifier

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Initialize ML models
ingredient_clusterer = None
recipe_recommender = None
substitution_finder = None
cuisine_classifier = None

def init_models():
    """Initialize all ML models"""
    global ingredient_clusterer, recipe_recommender, substitution_finder, cuisine_classifier
    
    print("\n🤖 Initializing ML Models...")
    
    # Initialize Ingredient Clustering
    ingredient_clusterer = get_trained_model()
    print("✅ Ingredient clustering model ready!")
    
    # Initialize Recipe Recommender
    recipe_recommender = RecipeRecommender()
    recipe_recommender.train()
    print("✅ Recipe recommendation model ready!")
    
    # Initialize Ingredient Substitution Finder
    substitution_finder = IngredientSubstitutionFinder(min_support=0.02, min_confidence=0.15)
    substitution_finder.train()
    print("✅ Ingredient substitution finder ready!")
    
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

@app.route('/api/cluster/ingredients', methods=['GET'])
def cluster_ingredients():
    """Get ingredient clusters using k-means"""
    try:
        clusters = ingredient_clusterer.get_clusters()
        cluster_names = ingredient_clusterer.get_cluster_names()
        
        # Format response
        result = []
        for cluster_id, ingredients in clusters.items():
            result.append({
                'cluster_id': cluster_id,
                'cluster_name': cluster_names.get(cluster_id, f"Cluster {cluster_id}"),
                'ingredients': ingredients,
                'count': len(ingredients)
            })
        
        # Sort by cluster_id
        result.sort(key=lambda x: x['cluster_id'])
        
        return jsonify({
            'success': True,
            'clusters': result,
            'total_clusters': len(result),
            'total_ingredients': sum(c['count'] for c in result),
            'algorithm': 'K-Means Clustering'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cluster/predict', methods=['POST'])
def predict_cluster():
    """Predict which cluster a new ingredient belongs to"""
    try:
        data = request.get_json()
        features = data.get('features', [])
        ingredient_name = data.get('name', 'Unknown Ingredient')
        
        if len(features) != 5:
            return jsonify({
                'success': False,
                'error': 'Features must include: protein, carbs, fat, calories, fiber'
            }), 400
        
        cluster_id = ingredient_clusterer.predict(features)
        cluster_names = ingredient_clusterer.get_cluster_names()
        clusters = ingredient_clusterer.get_clusters()
        
        return jsonify({
            'success': True,
            'ingredient': ingredient_name,
            'cluster_id': cluster_id,
            'cluster_name': cluster_names.get(cluster_id, f"Cluster {cluster_id}"),
            'similar_ingredients': clusters.get(cluster_id, [])
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===== FEATURE #3: INGREDIENT SUBSTITUTION ENDPOINTS =====

@app.route('/api/substitute', methods=['POST'])
def find_substitutes():
    """Find ingredient substitutes using association rules"""
    try:
        data = request.get_json()
        ingredient = data.get('ingredient', '').lower().strip()
        top_n = data.get('top_n', 5)
        
        if not ingredient:
            return jsonify({
                'success': False,
                'error': 'No ingredient provided'
            }), 400
        
        result = substitution_finder.get_substitutes(ingredient, top_n=top_n)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/substitute/ingredients', methods=['GET'])
def get_available_ingredients():
    """Get list of all ingredients with substitution rules"""
    try:
        ingredients = list(substitution_finder.substitution_rules.keys())
        return jsonify({
            'success': True,
            'ingredients': sorted(ingredients),
            'total': len(ingredients)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===== FEATURE #4: CUISINE CLASSIFICATION ENDPOINTS =====

@app.route('/api/cuisine/predict', methods=['POST'])
def predict_cuisine():
    """Predict cuisine type from ingredients using k-NN"""
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
