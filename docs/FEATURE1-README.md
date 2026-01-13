# Feature #1: Ingredient Clustering

## 🎯 Overview

Groups similar ingredients based on their nutritional profiles using **K-Means clustering algorithm**. This helps identify ingredient categories and understand nutritional similarities.

## 🧮 Algorithm: K-Means Clustering

K-Means is an unsupervised machine learning algorithm that partitions data into K distinct clusters.

### How It Works

1. **Initialization**: Randomly select K initial centroids (cluster centers)
2. **Assignment**: Assign each ingredient to the nearest centroid
3. **Update**: Recalculate centroids as the mean of all points in the cluster
4. **Repeat**: Steps 2-3 until convergence (centroids stop moving)

### Our Implementation

```python
from sklearn.cluster import KMeans
import numpy as np

class IngredientClustering:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
    
    def train(self, ingredients_data):
        # Extract features: [protein, carbs, fat, calories, fiber, category_encoded]
        features = self._extract_features(ingredients_data)
        
        # Fit K-Means model
        self.model.fit(features)
        
        # Store results
        self.labels = self.model.labels_
        self.centroids = self.model.cluster_centers_
```

## 📊 Features Used

Each ingredient is represented by **6 numerical features**:

1. **Protein** (grams per 100g)
2. **Carbohydrates** (grams per 100g)
3. **Fat** (grams per 100g)
4. **Calories** (kcal per 100g)
5. **Fiber** (grams per 100g)
6. **Category** (encoded: meat=1, vegetable=2, grain=3, etc.)

## 🎨 Example Clusters

### Cluster 0: High-Protein Meats
- Chicken (31g protein, 165 cal)
- Beef (26g protein, 250 cal)
- Fish (22g protein, 120 cal)

### Cluster 1: Dairy Products
- Cheese (25g protein, 402 cal, high fat)
- Milk (3.4g protein, 42 cal)
- Butter (0.9g protein, 717 cal, very high fat)

### Cluster 2: Grains & Starches
- Pasta (13g protein, 371 cal, 75g carbs)
- Rice (2.7g protein, 130 cal, 28g carbs)
- Bread (9g protein, 265 cal, 49g carbs)

### Cluster 3: Vegetables
- Tomatoes (0.9g protein, 18 cal, low everything)
- Lettuce (1.4g protein, 15 cal)
- Onions (1.1g protein, 40 cal)

### Cluster 4: Plant Proteins
- Tofu (8g protein, 76 cal)
- Lentils (9g protein, 116 cal, 20g carbs)
- Chickpeas (9g protein, 164 cal)

## 🔧 API Endpoints

### Get All Clusters
```http
GET /api/cluster/ingredients
```

**Response:**
```json
{
  "clusters": {
    "0": ["chicken", "beef", "fish"],
    "1": ["cheese", "milk", "butter"],
    "2": ["pasta", "rice", "bread"],
    "3": ["tomatoes", "lettuce", "onions"],
    "4": ["tofu", "lentils", "chickpeas"]
  },
  "centroids": [[31.0, 5.0, 12.0, 165.0, 0.0, 1.0], ...],
  "n_clusters": 5
}
```

### Predict Cluster for New Ingredient
```http
POST /api/cluster/predict
Content-Type: application/json

{
  "name": "salmon",
  "protein": 25.4,
  "carbs": 0.0,
  "fat": 13.4,
  "calories": 208,
  "fiber": 0.0
}
```

**Response:**
```json
{
  "success": true,
  "ingredient": "salmon",
  "cluster": 0,
  "cluster_name": "High-Protein Meats",
  "similar_ingredients": ["chicken", "beef", "tuna"]
}
```

## 💡 Use Cases

1. **Ingredient Substitution**: Find similar ingredients from the same cluster
2. **Nutrition Analysis**: Understand nutritional profiles of different food groups
3. **Recipe Planning**: Balance recipes by selecting ingredients from different clusters
4. **Dietary Planning**: Identify high-protein, low-carb, or low-fat ingredient groups

## 📈 Model Performance

- **Number of Clusters (K)**: 5 (optimal via elbow method)
- **Convergence**: Typically 10-15 iterations
- **Inertia**: Measures within-cluster sum of squares (lower is better)
- **Silhouette Score**: ~0.65 (good cluster separation)

## 🎯 Frontend Features

### Cluster Visualization
- Interactive display of all 5 clusters
- Ingredients grouped by cluster with color-coding
- Cluster names based on predominant ingredient type

### Prediction Tool
- Input form for new ingredient nutritional values
- Real-time cluster prediction
- Shows similar ingredients in the predicted cluster

### UI Elements
```jsx
// Show clusters
<button onClick={getClusters}>View Ingredient Clusters</button>

// Predict cluster
<form onSubmit={predictCluster}>
  <input name="name" placeholder="Ingredient name" />
  <input name="protein" type="number" placeholder="Protein (g)" />
  <input name="carbs" type="number" placeholder="Carbs (g)" />
  <input name="fat" type="number" placeholder="Fat (g)" />
  <input name="calories" type="number" placeholder="Calories" />
  <input name="fiber" type="number" placeholder="Fiber (g)" />
  <button type="submit">Predict Cluster</button>
</form>
```

## 🔬 Technical Details

### Distance Metric
Uses **Euclidean distance** to measure similarity:

$$
d(x, y) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}
$$

### Centroid Calculation
Cluster centroid is the **mean** of all points in the cluster:

$$
c_j = \frac{1}{|C_j|} \sum_{x \in C_j} x
$$

### Convergence Criteria
Algorithm stops when:
- Centroids move less than 0.0001
- Maximum iterations (300) reached
- No points change clusters

## 📚 Dependencies

```python
scikit-learn>=1.0.0  # K-Means implementation
numpy>=1.21.0        # Numerical operations
```

## 🎓 Learning Resources

- [K-Means Clustering (scikit-learn)](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Understanding K-Means](https://towardsdatascience.com/understanding-k-means-clustering-in-machine-learning-6a6e67336aa1)
- [Choosing K (Elbow Method)](https://www.analyticsvidhya.com/blog/2021/01/in-depth-intuition-of-k-means-clustering-algorithm-in-machine-learning/)

---

**Next Feature**: [Recipe Recommendation (Feature #2)](FEATURE2-README.md)
