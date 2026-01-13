from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models.ingredient_clustering import get_trained_model
from models.recipe_recommender import RecipeRecommender
from models.ingredient_substitution import IngredientSubstitutionFinder
from models.cuisine_classifier import CuisineClassifier
from models.nutrition_predictor import NutritionPredictor

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
nutrition_predictor = None

def init_models():
    """Initialize all ML models"""
    global ingredient_clusterer, recipe_recommender, substitution_finder, cuisine_classifier, nutrition_predictor
    
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
    
    # Initialize Nutrition Predictor
    nutrition_predictor = NutritionPredictor(use_ridge=True, alpha=1.0)
    nutrition_predictor.train()
    print("✅ Nutrition predictor ready!")
    
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
    """Recommend recipes based on ingredients using content-based filtering"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'No ingredients provided'
            }), 400
        
        # Get all recipes
        all_recipes = recipe_recommender.get_all_recipes()
        
        # Score recipes based on ingredient overlap
        scored_recipes = []
        for recipe in all_recipes:
            recipe_ingredients = set([ing.lower() for ing in recipe.get('ingredients', [])])
            input_ingredients = set([ing.lower().strip() for ing in ingredients])
            
            # Calculate overlap
            overlap = len(recipe_ingredients.intersection(input_ingredients))
            if overlap > 0:
                score = overlap / len(recipe_ingredients)  # Percentage of recipe ingredients matched
                scored_recipes.append({
                    'recipe': recipe,
                    'matched_ingredients': list(recipe_ingredients.intersection(input_ingredients)),
                    'overlap_score': round(score, 3),
                    'total_ingredients': len(recipe_ingredients)
                })
        
        # Sort by overlap score
        scored_recipes.sort(key=lambda x: x['overlap_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'input_ingredients': ingredients,
            'recommended_recipes': scored_recipes[:10],  # Top 10
            'total_matches': len(scored_recipes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        
        substitutes = substitution_finder.get_substitutes(ingredient, top_n=top_n)
        
        return jsonify({
            'success': True,
            'ingredient': ingredient,
            'substitutes': substitutes
        })
    
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

# ===== FEATURE #5: NUTRITION PREDICTION ENDPOINTS =====

@app.route('/api/nutrition/predict', methods=['POST'])
def predict_nutrition():
    """Predict nutritional information from ingredients using regression"""
    try:
        data = request.get_json()
        ingredients = data.get('ingredients', [])
        
        if not ingredients:
            return jsonify({
                'success': False,
                'error': 'No ingredients provided'
            }), 400
        
        predictions = nutrition_predictor.predict(ingredients)
        
        return jsonify({
            'success': True,
            'ingredients': ingredients,
            'nutrition': predictions,
            'model': 'Ridge Regression' if nutrition_predictor.use_ridge else 'Linear Regression'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nutrition/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_nutrition(recipe_id):
    """Get predicted nutrition for a specific recipe"""
    try:
        result = nutrition_predictor.predict_recipe(recipe_id=recipe_id)
        return jsonify({
            'success': True,
            **result
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nutrition/compare', methods=['POST'])
def compare_recipe_nutrition():
    """Compare nutritional values of multiple recipes"""
    try:
        data = request.get_json()
        recipe_ids = data.get('recipe_ids', [])
        
        if not recipe_ids:
            return jsonify({
                'success': False,
                'error': 'No recipe IDs provided'
            }), 400
        
        results = nutrition_predictor.compare_recipes(recipe_ids)
        
        return jsonify({
            'success': True,
            'recipes': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nutrition/metrics', methods=['GET'])
def get_nutrition_metrics():
    """Get model performance metrics"""
    try:
        metrics = nutrition_predictor.get_metrics()
        return jsonify({
            'success': True,
            'metrics': metrics,
            'model_type': 'Ridge Regression' if nutrition_predictor.use_ridge else 'Linear Regression'
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
