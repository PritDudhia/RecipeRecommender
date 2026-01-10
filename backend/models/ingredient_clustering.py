"""
Ingredient Clustering using K-Means
Groups similar ingredients together based on their characteristics
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import json
from pathlib import Path

class IngredientClusterer:
    def __init__(self, n_clusters=5):
        """
        Initialize the ingredient clusterer
        
        Args:
            n_clusters: Number of clusters to create
        """
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.ingredient_names = []
        self.feature_names = ['protein', 'carbs', 'fat', 'calories', 'fiber']
        
    def create_sample_data(self):
        """
        Create sample ingredient data with nutritional features
        Returns dict with ingredient names and their features
        """
        # Sample ingredients with nutritional data (protein, carbs, fat, calories, fiber)
        ingredients_data = {
            # Proteins
            'chicken breast': [31, 0, 3.6, 165, 0],
            'salmon': [25, 0, 13, 206, 0],
            'eggs': [13, 1.1, 11, 155, 0],
            'tofu': [8, 2, 4, 70, 1],
            'beef': [26, 0, 15, 250, 0],
            
            # Carbs/Grains
            'rice': [2.7, 28, 0.3, 130, 0.4],
            'pasta': [5, 25, 0.9, 131, 1.8],
            'bread': [9, 49, 3.2, 265, 2.7],
            'quinoa': [4.4, 21, 1.9, 120, 2.8],
            'oats': [13, 67, 7, 389, 11],
            
            # Vegetables
            'broccoli': [2.8, 7, 0.4, 34, 2.6],
            'spinach': [2.9, 3.6, 0.4, 23, 2.2],
            'carrots': [0.9, 10, 0.2, 41, 2.8],
            'tomatoes': [0.9, 3.9, 0.2, 18, 1.2],
            'bell pepper': [1, 6, 0.3, 31, 2.1],
            
            # Dairy
            'milk': [3.4, 5, 1, 42, 0],
            'cheese': [25, 1.3, 33, 402, 0],
            'yogurt': [10, 3.6, 0.4, 59, 0],
            'butter': [0.9, 0.1, 81, 717, 0],
            
            # Fats/Oils
            'olive oil': [0, 0, 100, 884, 0],
            'avocado': [2, 9, 15, 160, 7],
            'almonds': [21, 22, 50, 579, 12],
            'peanut butter': [25, 20, 50, 588, 6],
            
            # Fruits
            'banana': [1.1, 23, 0.3, 89, 2.6],
            'apple': [0.3, 14, 0.2, 52, 2.4],
            'orange': [0.9, 12, 0.1, 47, 2.4],
            'strawberries': [0.7, 8, 0.3, 32, 2],
        }
        
        return ingredients_data
    
    def train(self, ingredients_data=None):
        """
        Train the k-means clustering model
        
        Args:
            ingredients_data: Dict of {ingredient_name: [features]}
        """
        if ingredients_data is None:
            ingredients_data = self.create_sample_data()
        
        self.ingredient_names = list(ingredients_data.keys())
        X = np.array(list(ingredients_data.values()))
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit k-means
        self.kmeans.fit(X_scaled)
        
        return self
    
    def predict(self, ingredient_features):
        """
        Predict cluster for new ingredient
        
        Args:
            ingredient_features: List of features for the ingredient
        
        Returns:
            Cluster label (int)
        """
        X = np.array([ingredient_features])
        X_scaled = self.scaler.transform(X)
        return int(self.kmeans.predict(X_scaled)[0])
    
    def get_clusters(self):
        """
        Get all ingredients organized by cluster
        
        Returns:
            Dict mapping cluster_id to list of ingredients
        """
        if not self.ingredient_names:
            raise ValueError("Model not trained yet")
        
        clusters = {}
        labels = self.kmeans.labels_
        
        for idx, label in enumerate(labels):
            label = int(label)
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.ingredient_names[idx])
        
        return clusters
    
    def get_cluster_names(self):
        """
        Get descriptive names for each cluster based on ingredients
        
        Returns:
            Dict mapping cluster_id to cluster name
        """
        clusters = self.get_clusters()
        cluster_names = {}
        
        # Simple heuristic based on common ingredients
        for cluster_id, ingredients in clusters.items():
            ingredients_lower = [ing.lower() for ing in ingredients]
            
            if any(protein in ingredients_lower for protein in ['chicken', 'beef', 'salmon', 'eggs', 'tofu']):
                cluster_names[cluster_id] = "Protein-Rich Foods"
            elif any(carb in ingredients_lower for carb in ['rice', 'pasta', 'bread', 'quinoa', 'oats']):
                cluster_names[cluster_id] = "Grains & Carbohydrates"
            elif any(veg in ingredients_lower for veg in ['broccoli', 'spinach', 'carrots', 'tomatoes', 'pepper']):
                cluster_names[cluster_id] = "Vegetables"
            elif any(dairy in ingredients_lower for dairy in ['milk', 'cheese', 'yogurt', 'butter']):
                cluster_names[cluster_id] = "Dairy Products"
            elif any(fat in ingredients_lower for fat in ['oil', 'avocado', 'almonds', 'peanut']):
                cluster_names[cluster_id] = "Healthy Fats & Nuts"
            elif any(fruit in ingredients_lower for fruit in ['banana', 'apple', 'orange', 'strawberries']):
                cluster_names[cluster_id] = "Fruits"
            else:
                cluster_names[cluster_id] = f"Cluster {cluster_id}"
        
        return cluster_names
    
    def save(self, filepath):
        """Save the trained model"""
        model_data = {
            'kmeans': self.kmeans,
            'scaler': self.scaler,
            'ingredient_names': self.ingredient_names,
            'n_clusters': self.n_clusters
        }
        joblib.dump(model_data, filepath)
    
    def load(self, filepath):
        """Load a trained model"""
        model_data = joblib.load(filepath)
        self.kmeans = model_data['kmeans']
        self.scaler = model_data['scaler']
        self.ingredient_names = model_data['ingredient_names']
        self.n_clusters = model_data['n_clusters']
        return self


# Initialize and train the model when module is imported
def get_trained_model():
    """Get a pre-trained ingredient clustering model"""
    clusterer = IngredientClusterer(n_clusters=6)
    clusterer.train()
    return clusterer
