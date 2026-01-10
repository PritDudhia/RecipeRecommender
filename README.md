# Recipe Recommender with Substitution Engine

A smart recipe recommendation system with ML-powered ingredient substitution capabilities.

## 🎯 Project Overview

This web application helps users discover recipes based on available ingredients and suggests smart substitutions when ingredients are missing.

## 🚀 Features (Implemented as Git Branches)

- **Ingredient Clustering** (`feature/ingredient-clustering`) - Groups similar ingredients using k-means
- **Recipe Recommendation** (`feature/recipe-recommendation`) - Collaborative filtering for personalized suggestions
- **Substitution Finder** (`feature/substitution-finder`) - Association rules (Apriori) for ingredient swaps
- **Cuisine Classification** (`feature/cuisine-classification`) - k-NN classifier for cuisine types
- **Nutrition Predictor** (`feature/nutrition-predictor`) - Predicts nutritional values

## 🛠️ Tech Stack

### Frontend
- React + Vite
- Tailwind CSS
- Axios for API calls

### Backend
- Python Flask
- scikit-learn, pandas, numpy
- SQLite database

## 📦 Project Structure

```
RecipeRecommender/
├── frontend/           # React + Vite app
├── backend/            # Flask API
├── data/               # Datasets and models
└── docs/               # Documentation
```

## 🏃 Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

## 📝 ML Techniques Used

- **Collaborative Filtering**: User-based recommendations
- **Association Rules (Apriori)**: Ingredient substitution patterns
- **k-NN**: Cuisine classification
- **Content-Based Filtering**: Recipe similarity
- **k-Means**: Ingredient clustering
