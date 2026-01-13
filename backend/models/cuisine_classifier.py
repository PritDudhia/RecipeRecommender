"""
Feature #4: Cuisine Classification
Uses k-Nearest Neighbors (k-NN) to classify recipes by cuisine type based on ingredients
Analyzes 120 recipes from 32 world cuisines
"""

import numpy as np
from collections import Counter
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

try:
    from .world_recipes_data import get_world_recipes
except ImportError:
    from world_recipes_data import get_world_recipes


class CuisineClassifier:
    """
    Classifies recipes into cuisine types using k-Nearest Neighbors
    Based on ingredient presence vectors
    """
    
    def __init__(self, n_neighbors=5):
        """
        Initialize the cuisine classifier
        
        Args:
            n_neighbors: Number of neighbors to use for k-NN (default: 5)
        """
        self.n_neighbors = n_neighbors
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors, weights='distance')
        self.label_encoder = LabelEncoder()
        self.recipes = []
        self.ingredient_index = {}
        self.cuisine_labels = []
        
    def create_ingredient_vectors(self):
        """
        Create binary ingredient presence vectors for each recipe
        Returns feature matrix where each row is a recipe, each column is an ingredient
        """
        # Get all unique ingredients
        all_ingredients = set()
        for recipe in self.recipes:
            all_ingredients.update(recipe.get('ingredients', []))
        
        # Create ingredient to index mapping
        self.ingredient_index = {ing: idx for idx, ing in enumerate(sorted(all_ingredients))}
        n_ingredients = len(self.ingredient_index)
        n_recipes = len(self.recipes)
        
        # Create feature matrix (binary: 1 if ingredient present, 0 otherwise)
        feature_matrix = np.zeros((n_recipes, n_ingredients))
        
        for recipe_idx, recipe in enumerate(self.recipes):
            for ingredient in recipe.get('ingredients', []):
                ing_idx = self.ingredient_index.get(ingredient)
                if ing_idx is not None:
                    feature_matrix[recipe_idx, ing_idx] = 1
        
        return feature_matrix
    
    def train(self):
        """Train the cuisine classifier on world recipes dataset"""
        print("Training Cuisine Classifier...")
        
        # Load recipes
        self.recipes = get_world_recipes()
        
        # Extract cuisine labels
        self.cuisine_labels = [recipe.get('cuisine', 'Unknown') for recipe in self.recipes]
        
        # Encode cuisine labels to integers
        y_encoded = self.label_encoder.fit_transform(self.cuisine_labels)
        
        # Create feature vectors
        X = self.create_ingredient_vectors()
        
        # Train k-NN model
        self.model.fit(X, y_encoded)
        
        # Get cuisine counts
        cuisine_counts = Counter(self.cuisine_labels)
        n_cuisines = len(set(self.cuisine_labels))
        
        print(f"✅ Trained on {len(self.recipes)} recipes")
        print(f"✅ {n_cuisines} different cuisines")
        print(f"✅ {len(self.ingredient_index)} unique ingredients")
        print(f"✅ k-NN with k={self.n_neighbors} neighbors")
        
        return self
    
    def predict_cuisine(self, ingredients):
        """
        Predict cuisine type for given ingredients
        
        Args:
            ingredients: List of ingredient names
            
        Returns:
            Dictionary with prediction results
        """
        if not ingredients:
            return {
                'success': False,
                'error': 'No ingredients provided'
            }
        
        # Create feature vector for input ingredients
        feature_vector = np.zeros((1, len(self.ingredient_index)))
        
        matched_ingredients = []
        unmatched_ingredients = []
        
        for ingredient in ingredients:
            ing_lower = ingredient.lower().strip()
            if ing_lower in self.ingredient_index:
                ing_idx = self.ingredient_index[ing_lower]
                feature_vector[0, ing_idx] = 1
                matched_ingredients.append(ing_lower)
            else:
                unmatched_ingredients.append(ingredient)
        
        # Check if any ingredients matched
        if len(matched_ingredients) == 0:
            return {
                'success': False,
                'error': 'None of the ingredients are in our database',
                'unmatched_ingredients': unmatched_ingredients
            }
        
        # Predict cuisine
        predicted_label = self.model.predict(feature_vector)[0]
        predicted_cuisine = self.label_encoder.inverse_transform([predicted_label])[0]
        
        # Get prediction probabilities (based on neighbor distances)
        probabilities = self.model.predict_proba(feature_vector)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = []
        
        for idx in top_indices:
            cuisine = self.label_encoder.inverse_transform([idx])[0]
            probability = probabilities[idx]
            if probability > 0:
                top_predictions.append({
                    'cuisine': cuisine,
                    'probability': float(probability),
                    'percentage': float(probability * 100)
                })
        
        # Get k nearest recipes as examples
        distances, indices = self.model.kneighbors(feature_vector)
        
        nearest_recipes = []
        for idx in indices[0][:3]:  # Top 3 nearest
            recipe = self.recipes[idx]
            nearest_recipes.append({
                'name': recipe.get('name'),
                'cuisine': recipe.get('cuisine'),
                'ingredients': recipe.get('ingredients', [])[:5]  # First 5 ingredients
            })
        
        return {
            'success': True,
            'predicted_cuisine': predicted_cuisine,
            'confidence': float(probabilities[predicted_label] * 100),
            'top_predictions': top_predictions,
            'matched_ingredients': matched_ingredients,
            'unmatched_ingredients': unmatched_ingredients,
            'total_ingredients': len(ingredients),
            'matched_count': len(matched_ingredients),
            'nearest_recipes': nearest_recipes,
            'k_neighbors': self.n_neighbors
        }
    
    def get_cuisine_stats(self):
        """Get statistics about cuisines in the dataset"""
        cuisine_counts = Counter(self.cuisine_labels)
        
        return {
            'total_recipes': len(self.recipes),
            'total_cuisines': len(set(self.cuisine_labels)),
            'total_ingredients': len(self.ingredient_index),
            'cuisine_distribution': [
                {'cuisine': cuisine, 'count': count}
                for cuisine, count in sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
            ],
            'k_neighbors': self.n_neighbors
        }
    
    def get_all_cuisines(self):
        """Get list of all available cuisines"""
        return sorted(set(self.cuisine_labels))


# Test the model
if __name__ == '__main__':
    classifier = CuisineClassifier(n_neighbors=5)
    classifier.train()
    
    print("\n" + "="*60)
    print("Testing Cuisine Classification")
    print("="*60)
    
    # Test 1: Italian ingredients
    print("\nTest 1: Italian ingredients")
    result = classifier.predict_cuisine(['pasta', 'tomato sauce', 'mozzarella', 'basil', 'olive oil'])
    print(f"Predicted: {result['predicted_cuisine']} ({result['confidence']:.1f}% confidence)")
    top_3 = ', '.join([f"{p['cuisine']} ({p['percentage']:.1f}%)" for p in result['top_predictions']])
    print(f"Top 3: {top_3}")
    
    # Test 2: Asian ingredients
    print("\nTest 2: Asian ingredients")
    result = classifier.predict_cuisine(['soy sauce', 'ginger', 'garlic', 'rice', 'sesame oil'])
    print(f"Predicted: {result['predicted_cuisine']} ({result['confidence']:.1f}% confidence)")
    top_3 = ', '.join([f"{p['cuisine']} ({p['percentage']:.1f}%)" for p in result['top_predictions']])
    print(f"Top 3: {top_3}")
    
    # Test 3: Mexican ingredients
    print("\nTest 3: Mexican ingredients")
    result = classifier.predict_cuisine(['tortillas', 'beans', 'cheese', 'salsa', 'avocado', 'lime'])
    print(f"Predicted: {result['predicted_cuisine']} ({result['confidence']:.1f}% confidence)")
    top_3 = ', '.join([f"{p['cuisine']} ({p['percentage']:.1f}%)" for p in result['top_predictions']])
    print(f"Top 3: {top_3}")
    
    # Show stats
    print("\n" + "="*60)
    stats = classifier.get_cuisine_stats()
    print(f"Dataset: {stats['total_recipes']} recipes, {stats['total_cuisines']} cuisines")
    print(f"Top 5 cuisines:")
    for item in stats['cuisine_distribution'][:5]:
        print(f"  {item['cuisine']}: {item['count']} recipes")
