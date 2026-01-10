"""
Feature #2: Recipe Recommendation System
Uses collaborative filtering to recommend recipes based on user preferences
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os


class RecipeRecommender:
    """
    Collaborative Filtering Recipe Recommender
    Uses user-item rating matrix and cosine similarity
    """
    
    def __init__(self):
        self.recipes = []
        self.user_item_matrix = None
        self.recipe_features = None
        self.similarity_matrix = None
        
    def create_sample_data(self):
        """Create sample recipe dataset with user ratings"""
        
        # Sample recipes with features: [prep_time, difficulty, spice_level, sweetness, healthiness]
        self.recipes = [
            {
                'id': 1,
                'name': 'Chicken Stir Fry',
                'cuisine': 'Asian',
                'ingredients': ['chicken', 'vegetables', 'soy sauce', 'ginger'],
                'features': [20, 2, 3, 1, 4]  # prep_time, difficulty, spice, sweet, health
            },
            {
                'id': 2,
                'name': 'Spaghetti Carbonara',
                'cuisine': 'Italian',
                'ingredients': ['pasta', 'eggs', 'bacon', 'cheese'],
                'features': [25, 3, 1, 2, 2]
            },
            {
                'id': 3,
                'name': 'Greek Salad',
                'cuisine': 'Mediterranean',
                'ingredients': ['tomatoes', 'cucumber', 'feta', 'olives'],
                'features': [10, 1, 2, 1, 5]
            },
            {
                'id': 4,
                'name': 'Beef Tacos',
                'cuisine': 'Mexican',
                'ingredients': ['beef', 'tortillas', 'cheese', 'salsa'],
                'features': [30, 2, 4, 1, 3]
            },
            {
                'id': 5,
                'name': 'Mushroom Risotto',
                'cuisine': 'Italian',
                'ingredients': ['rice', 'mushrooms', 'wine', 'cheese'],
                'features': [45, 4, 1, 2, 3]
            },
            {
                'id': 6,
                'name': 'Caesar Salad',
                'cuisine': 'American',
                'ingredients': ['lettuce', 'croutons', 'cheese', 'dressing'],
                'features': [15, 1, 1, 1, 4]
            },
            {
                'id': 7,
                'name': 'Pad Thai',
                'cuisine': 'Thai',
                'ingredients': ['noodles', 'shrimp', 'peanuts', 'lime'],
                'features': [35, 3, 4, 3, 3]
            },
            {
                'id': 8,
                'name': 'Margherita Pizza',
                'cuisine': 'Italian',
                'ingredients': ['dough', 'tomatoes', 'mozzarella', 'basil'],
                'features': [20, 2, 1, 2, 2]
            },
            {
                'id': 9,
                'name': 'Chicken Curry',
                'cuisine': 'Indian',
                'ingredients': ['chicken', 'curry powder', 'coconut milk', 'rice'],
                'features': [40, 3, 5, 2, 3]
            },
            {
                'id': 10,
                'name': 'Quinoa Bowl',
                'cuisine': 'Fusion',
                'ingredients': ['quinoa', 'vegetables', 'avocado', 'chickpeas'],
                'features': [25, 2, 2, 1, 5]
            },
            {
                'id': 11,
                'name': 'French Onion Soup',
                'cuisine': 'French',
                'ingredients': ['onions', 'broth', 'cheese', 'bread'],
                'features': [60, 3, 1, 3, 2]
            },
            {
                'id': 12,
                'name': 'Fish Tacos',
                'cuisine': 'Mexican',
                'ingredients': ['fish', 'tortillas', 'cabbage', 'lime'],
                'features': [25, 2, 3, 1, 4]
            },
            {
                'id': 13,
                'name': 'Vegetable Stir Fry',
                'cuisine': 'Asian',
                'ingredients': ['vegetables', 'tofu', 'soy sauce', 'garlic'],
                'features': [15, 2, 3, 1, 5]
            },
            {
                'id': 14,
                'name': 'Chocolate Cake',
                'cuisine': 'Dessert',
                'ingredients': ['flour', 'chocolate', 'eggs', 'sugar'],
                'features': [90, 4, 0, 5, 1]
            },
            {
                'id': 15,
                'name': 'Grilled Salmon',
                'cuisine': 'Seafood',
                'ingredients': ['salmon', 'lemon', 'herbs', 'olive oil'],
                'features': [20, 2, 1, 1, 5]
            }
        ]
        
        # User-Item Rating Matrix (10 users x 15 recipes)
        # Ratings: 0 = not rated, 1-5 = user rating
        self.user_item_matrix = np.array([
            [5, 0, 4, 0, 3, 0, 0, 4, 0, 5, 0, 0, 4, 0, 5],  # User 1: Likes healthy food
            [0, 5, 0, 4, 5, 0, 0, 5, 0, 0, 4, 0, 0, 0, 0],  # User 2: Likes Italian
            [4, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 4, 5, 0, 5],  # User 3: Likes healthy/light
            [0, 4, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 0, 0, 0],  # User 4: Likes spicy
            [3, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0, 0, 5, 0],  # User 5: Likes complex dishes
            [5, 0, 5, 0, 0, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5],  # User 6: Likes quick/healthy
            [0, 4, 0, 5, 0, 0, 5, 4, 5, 0, 0, 4, 0, 0, 0],  # User 7: Likes Mexican/Asian
            [0, 5, 0, 0, 5, 0, 4, 5, 0, 0, 5, 0, 0, 4, 0],  # User 8: Likes Italian/French
            [4, 0, 5, 4, 0, 5, 0, 0, 0, 5, 0, 5, 5, 0, 5],  # User 9: Likes salads/light
            [0, 0, 0, 5, 0, 0, 5, 0, 5, 0, 0, 5, 4, 0, 0]   # User 10: Likes spicy food
        ])
        
        # Extract recipe features for content-based similarity
        self.recipe_features = np.array([recipe['features'] for recipe in self.recipes])
        
    def train(self):
        """Train the recommendation model using collaborative filtering"""
        print("Training Recipe Recommender...")
        
        # Create sample data
        self.create_sample_data()
        
        # Calculate recipe similarity matrix using cosine similarity
        # Based on recipe features (content-based approach)
        self.similarity_matrix = cosine_similarity(self.recipe_features)
        
        print(f"✅ Trained on {len(self.recipes)} recipes")
        print(f"✅ User-Item matrix shape: {self.user_item_matrix.shape}")
        
        return self
        
    def get_user_based_recommendations(self, user_id, top_n=5):
        """
        Collaborative Filtering: Recommend recipes based on similar users' preferences
        
        Args:
            user_id: User ID (0-9 for sample data)
            top_n: Number of recommendations to return
        
        Returns:
            List of recommended recipe dictionaries
        """
        if user_id >= len(self.user_item_matrix):
            raise ValueError(f"User ID must be between 0 and {len(self.user_item_matrix)-1}")
        
        # Get user's ratings
        user_ratings = self.user_item_matrix[user_id]
        
        # Calculate user similarity (collaborative filtering)
        user_similarity = cosine_similarity([user_ratings], self.user_item_matrix)[0]
        
        # Get predicted ratings for unrated recipes
        predicted_ratings = []
        
        for recipe_idx in range(len(self.recipes)):
            if user_ratings[recipe_idx] == 0:  # Not yet rated by user
                # Weighted average of ratings from similar users
                similar_users_ratings = []
                
                for other_user_idx in range(len(self.user_item_matrix)):
                    if other_user_idx != user_id and self.user_item_matrix[other_user_idx][recipe_idx] > 0:
                        similar_users_ratings.append({
                            'rating': self.user_item_matrix[other_user_idx][recipe_idx],
                            'similarity': user_similarity[other_user_idx]
                        })
                
                if similar_users_ratings:
                    # Calculate weighted rating
                    total_similarity = sum(r['similarity'] for r in similar_users_ratings)
                    if total_similarity > 0:
                        predicted_rating = sum(
                            r['rating'] * r['similarity'] for r in similar_users_ratings
                        ) / total_similarity
                    else:
                        predicted_rating = 0
                else:
                    predicted_rating = 0
                
                predicted_ratings.append({
                    'recipe': self.recipes[recipe_idx],
                    'predicted_rating': predicted_rating
                })
        
        # Sort by predicted rating
        predicted_ratings.sort(key=lambda x: x['predicted_rating'], reverse=True)
        
        # Return top N recommendations
        recommendations = []
        for item in predicted_ratings[:top_n]:
            recipe = item['recipe'].copy()
            recipe['predicted_rating'] = round(item['predicted_rating'], 2)
            recipe['recommendation_type'] = 'collaborative_filtering'
            recommendations.append(recipe)
        
        return recommendations
    
    def get_content_based_recommendations(self, recipe_id, top_n=5):
        """
        Content-Based Filtering: Recommend similar recipes based on features
        
        Args:
            recipe_id: Recipe ID (1-15 for sample data)
            top_n: Number of recommendations to return
        
        Returns:
            List of similar recipe dictionaries
        """
        # Find recipe index
        recipe_idx = None
        for idx, recipe in enumerate(self.recipes):
            if recipe['id'] == recipe_id:
                recipe_idx = idx
                break
        
        if recipe_idx is None:
            raise ValueError(f"Recipe ID {recipe_id} not found")
        
        # Get similarity scores for this recipe
        similarities = self.similarity_matrix[recipe_idx]
        
        # Get indices of similar recipes (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
        
        # Build recommendations
        recommendations = []
        for idx in similar_indices:
            recipe = self.recipes[idx].copy()
            recipe['similarity_score'] = round(similarities[idx], 2)
            recipe['recommendation_type'] = 'content_based'
            recommendations.append(recipe)
        
        return recommendations
    
    def get_all_recipes(self):
        """Return all available recipes"""
        return self.recipes
    
    def get_recipe_by_id(self, recipe_id):
        """Get a specific recipe by ID"""
        for recipe in self.recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None
    
    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'recipes': self.recipes,
            'user_item_matrix': self.user_item_matrix,
            'recipe_features': self.recipe_features,
            'similarity_matrix': self.similarity_matrix
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a trained model"""
        if os.path.exists(filepath):
            model_data = joblib.load(filepath)
            self.recipes = model_data['recipes']
            self.user_item_matrix = model_data['user_item_matrix']
            self.recipe_features = model_data['recipe_features']
            self.similarity_matrix = model_data['similarity_matrix']
            print(f"Model loaded from {filepath}")
        else:
            print(f"No saved model found at {filepath}")
            self.train()


# Test the recommender
if __name__ == "__main__":
    recommender = RecipeRecommender()
    recommender.train()
    
    # Test collaborative filtering
    print("\n=== Collaborative Filtering Recommendations for User 1 ===")
    user_recs = recommender.get_user_based_recommendations(user_id=0, top_n=5)
    for rec in user_recs:
        print(f"- {rec['name']} ({rec['cuisine']}) - Predicted Rating: {rec['predicted_rating']}")
    
    # Test content-based filtering
    print("\n=== Content-Based Recommendations for 'Chicken Stir Fry' ===")
    content_recs = recommender.get_content_based_recommendations(recipe_id=1, top_n=5)
    for rec in content_recs:
        print(f"- {rec['name']} ({rec['cuisine']}) - Similarity: {rec['similarity_score']}")
