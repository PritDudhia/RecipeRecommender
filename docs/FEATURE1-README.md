# Feature #1: Ingredient Clustering 🔍

## Overview
K-Means machine learning algorithm that groups ingredients into 6 clusters based on nutritional similarity.

## 📊 Visual Flow Diagram
👉 **[View Flow Diagram](./FEATURE1-VISUAL-FLOW.md)** - See complete visual documentation with Mermaid diagrams!

## Quick Summary

### ML Algorithm: K-Means Clustering
- **Clusters:** 6 groups
- **Ingredients:** 28 sample foods
- **Features:** Protein, Carbs, Fat, Calories, Fiber
- **Preprocessing:** StandardScaler normalization
- **Library:** scikit-learn 1.3.2

### Two Main Capabilities

#### 1. View All Clusters 📋
- Click "View Ingredient Clusters" button
- See all 6 pre-computed clusters
- Examples:
  - **Protein-Rich Foods:** chicken, salmon, eggs, tofu, beef
  - **Grains & Carbohydrates:** rice, pasta, bread, quinoa, oats
  - **Vegetables:** broccoli, spinach, carrots, tomatoes, bell pepper
  - **Dairy Products:** milk, cheese, yogurt, butter
  - **Healthy Fats & Nuts:** olive oil, avocado, almonds, peanut butter
  - **Fruits:** banana, apple, orange, strawberries

#### 2. Predict New Ingredient 🎯
- Enter nutritional data for any ingredient
- ML model predicts which cluster it belongs to
- Example: Turkey → "Protein-Rich Foods"

## Tech Stack
- 🐍 **Backend:** Python + Flask
- 🤖 **ML:** scikit-learn (K-Means)
- ⚛️ **Frontend:** React + Vite
- 🎨 **UI:** Tailwind CSS
- 🔌 **API:** RESTful (GET & POST)

## API Endpoints

### GET `/api/cluster/ingredients`
Returns all 6 clusters with ingredients.

**Response:**
```json
{
  "success": true,
  "clusters": [
    {
      "cluster_id": 0,
      "cluster_name": "Grains & Carbohydrates",
      "count": 5,
      "ingredients": ["rice", "pasta", "bread", "quinoa", "oats"]
    }
  ],
  "total_clusters": 6,
  "total_ingredients": 28,
  "algorithm": "K-Means Clustering"
}
```

### POST `/api/cluster/predict`
Predicts cluster for new ingredient based on nutritional features.

**Request:**
```json
{
  "name": "Turkey",
  "features": [29, 0, 7, 189, 0]
}
```

**Response:**
```json
{
  "success": true,
  "ingredient": "Turkey",
  "cluster_id": 1,
  "cluster_name": "Protein-Rich Foods",
  "similar_ingredients": ["chicken breast", "salmon", "eggs", "tofu", "beef"]
}
```

## How to Test

### View Clusters:
1. Open http://localhost:5173
2. Click "View Ingredient Clusters"
3. See 6 colorful cards with ingredients

### Predict Ingredient (Example: Turkey):
1. Scroll to "🎯 Predict Ingredient Cluster"
2. Enter:
   - Name: `Turkey`
   - Protein: `29`
   - Carbs: `0`
   - Fat: `7`
   - Calories: `189`
   - Fiber: `0`
3. Click "Predict Cluster"
4. See result: "Belongs to: Protein-Rich Foods"

## File Structure
```
backend/
├── models/
│   ├── __init__.py
│   └── ingredient_clustering.py   # K-Means model implementation
├── app.py                          # Flask API endpoints
└── config.py                       # Configuration

frontend/
└── src/
    └── App.jsx                     # React UI with cluster visualization
```

## Key Code Components

### Model Training (backend/models/ingredient_clustering.py)
```python
class IngredientClusterer:
    def __init__(self, n_clusters=6):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
    
    def train(self, ingredients_data):
        X = np.array(list(ingredients_data.values()))
        X_scaled = self.scaler.fit_transform(X)
        self.kmeans.fit(X_scaled)
```

### Prediction (backend/models/ingredient_clustering.py)
```python
def predict(self, ingredient_features):
    X = np.array([ingredient_features])
    X_scaled = self.scaler.transform(X)
    return int(self.kmeans.predict(X_scaled)[0])
```

## Future Improvements
- Integrate nutrition API (USDA FoodData Central) for auto-lookup
- Expand ingredient database to 100+ items
- Add visualization of cluster centroids
- Implement silhouette score for cluster quality metrics
- Support for dietary restrictions filtering

---

**Status:** ✅ Complete and Pushed to GitHub  
**Branch:** `feature/ingredient-clustering`  
**Demo:** http://localhost:5173
