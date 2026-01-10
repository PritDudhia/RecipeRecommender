from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models.ingredient_clustering import get_trained_model

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Configuration
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False

# Initialize ML models
ingredient_clusterer = None

def init_models():
    """Initialize ML models on startup"""
    global ingredient_clusterer
    print("🤖 Initializing ML models...")
    ingredient_clusterer = get_trained_model()
    print("✅ Ingredient clustering model ready!")

# Initialize models
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

if __name__ == '__main__':
    print("🚀 Starting Recipe Recommender Backend...")
    print("📍 API available at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
