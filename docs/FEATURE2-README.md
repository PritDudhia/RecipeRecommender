# Feature #2: Recipe Recommendation System 🎯

## Overview
Collaborative filtering and content-based filtering algorithms that provide personalized recipe recommendations based on user preferences and recipe similarity.

## 📊 Visual Flow Diagram
👉 **[View Flow Diagram](./FEATURE2-VISUAL-FLOW.md)** - See complete visual documentation with Mermaid diagrams!

## Quick Summary

### ML Algorithms: Collaborative Filtering + Content-Based Filtering
- **Methods:** 2 recommendation approaches
- **Recipes:** 15 sample recipes
- **Users:** 10 user profiles with rating history
- **Features:** Prep time, difficulty, spice level, sweetness, healthiness
- **Similarity Metric:** Cosine similarity

## How It Works

### 1. Collaborative Filtering
- Uses user-item rating matrix (10 users × 15 recipes)
- Calculates user similarity using cosine similarity
- Predicts ratings for unrated recipes based on similar users' preferences
- Returns personalized recommendations with predicted ratings

### 2. Content-Based Filtering
- Analyzes recipe features (prep time, difficulty, spice, sweetness, health)
- Calculates recipe similarity using cosine similarity
- Finds similar recipes based on feature vectors
- Returns recommendations with similarity scores

## API Endpoints

### GET `/api/recipes`
Returns all available recipes

**Response:**
```json
{
  "recipes": [
    {
      "id": 1,
      "name": "Chicken Stir Fry",
      "cuisine": "Asian",
      "ingredients": ["chicken", "vegetables", "soy sauce", "ginger"],
      "features": [20, 2, 3, 1, 4]
    }
  ],
  "total": 15
}
```

### GET `/api/recommend/user/<user_id>?top_n=5`
Get personalized recommendations using collaborative filtering

**Parameters:**
- `user_id`: User ID (0-9 for sample data)
- `top_n`: Number of recommendations (default: 5)

**Response:**
```json
{
  "user_id": 0,
  "method": "collaborative_filtering",
  "recommendations": [
    {
      "id": 2,
      "name": "Spaghetti Carbonara",
      "cuisine": "Italian",
      "predicted_rating": 4.23,
      "recommendation_type": "collaborative_filtering"
    }
  ],
  "total": 5
}
```

### GET `/api/recommend/similar/<recipe_id>?top_n=5`
Find similar recipes using content-based filtering

**Parameters:**
- `recipe_id`: Recipe ID (1-15 for sample data)
- `top_n`: Number of recommendations (default: 5)

**Response:**
```json
{
  "base_recipe": {
    "id": 1,
    "name": "Chicken Stir Fry"
  },
  "method": "content_based_filtering",
  "recommendations": [
    {
      "id": 13,
      "name": "Vegetable Stir Fry",
      "similarity_score": 0.89,
      "recommendation_type": "content_based"
    }
  ],
  "total": 5
}
```

## UI Features

### Tab 1: Collaborative Filtering
- Select from 10 user profiles (each with different preferences)
- Get personalized recommendations based on similar users
- View predicted ratings for each recommendation
- See recipe details (cuisine, ingredients, prep time, difficulty)

### Tab 2: Content-Based Filtering
- Browse all 15 recipes
- Click any recipe to find similar dishes
- View similarity scores (percentage match)
- Discover recipes with similar characteristics

## Testing Guide

### Test 1: Collaborative Filtering (User 1 - Likes healthy food)
1. Open http://localhost:5173
2. Click **"👥 Collaborative Filtering"** tab
3. Select **"User 1 - Likes healthy food"** from dropdown
4. Click **"Get Recommendations"**
5. ✅ See 5 personalized recipes with predicted ratings
6. ✅ Recommendations should favor healthy recipes (quinoa bowl, grilled salmon, greek salad)

### Test 2: Collaborative Filtering (User 4 - Loves spicy food)
1. Select **"User 4 - Loves spicy food"** from dropdown
2. Click **"Get Recommendations"**
3. ✅ See spicy recommendations (pad thai, chicken curry, beef tacos)

### Test 3: Content-Based Filtering
1. Click **"🔍 Content-Based Filtering"** tab
2. Click on **"Chicken Stir Fry"** recipe card
3. ✅ See similar recipes (Vegetable Stir Fry, Pad Thai)
4. ✅ Similarity scores displayed as percentages

### Test 4: Content-Based Filtering (Dessert)
1. Click on **"Chocolate Cake"** recipe card
2. ✅ See similar desserts and sweet dishes
3. ✅ Higher similarity scores for recipes with high sweetness

## File Structure
```
backend/
├── models/
│   ├── __init__.py
│   └── recipe_recommender.py   # Collaborative + Content-Based filtering
├── app.py                       # Flask API with 3 endpoints
└── config.py                    # Configuration

frontend/
└── src/
    └── App.jsx                  # React UI with 2 tabs (collaborative/content-based)
```

## ML Implementation Details

### User-Item Rating Matrix
```python
# 10 users × 15 recipes
# Ratings: 0 = not rated, 1-5 = user rating
user_item_matrix = np.array([
    [5, 0, 4, 0, 3, ...],  # User 1
    [0, 5, 0, 4, 5, ...],  # User 2
    ...
])
```

### Collaborative Filtering Algorithm
1. Calculate user similarity using cosine similarity
2. For each unrated recipe:
   - Find users who rated this recipe
   - Weight their ratings by similarity to target user
   - Calculate weighted average = predicted rating
3. Sort by predicted rating, return top N

### Content-Based Filtering Algorithm
1. Extract recipe features: `[prep_time, difficulty, spice_level, sweetness, healthiness]`
2. Calculate cosine similarity between all recipe pairs
3. For target recipe, get similarity scores to all other recipes
4. Sort by similarity score, return top N (excluding target)

## Key Features

✅ **Dual Recommendation Approach**: Collaborative + Content-Based
✅ **User Profiles**: 10 distinct user preference patterns
✅ **Recipe Database**: 15 diverse recipes across cuisines
✅ **Predicted Ratings**: Weighted collaborative filtering scores
✅ **Similarity Scores**: Percentage match for content-based recommendations
✅ **Interactive UI**: Tab-based interface with real-time filtering
✅ **Visual Feedback**: Color-coded cards, cuisine badges, feature details

---

**Status:** ✅ Complete | **Branch:** `feature/recipe-recommendation` | **Demo:** http://localhost:5173
