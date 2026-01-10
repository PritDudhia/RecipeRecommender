import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directory
DATA_DIR = BASE_DIR.parent / 'data'
MODELS_DIR = DATA_DIR / 'models'
DATASETS_DIR = DATA_DIR / 'datasets'

# Ensure directories exist
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_PATH = DATA_DIR / 'recipes.db'

# ML Model paths
INGREDIENT_CLUSTER_MODEL = MODELS_DIR / 'ingredient_clusters.pkl'
RECIPE_RECOMMENDER_MODEL = MODELS_DIR / 'recipe_recommender.pkl'
SUBSTITUTION_MODEL = MODELS_DIR / 'substitution_rules.pkl'
CUISINE_CLASSIFIER_MODEL = MODELS_DIR / 'cuisine_classifier.pkl'
NUTRITION_PREDICTOR_MODEL = MODELS_DIR / 'nutrition_predictor.pkl'

# API Configuration
API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG = True
