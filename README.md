# 🍳 Recipe Recommender System

A comprehensive machine learning-powered recipe recommendation system with **3 core ML features** analyzing **120+ recipes from 32 world cuisines** with **262+ ingredients**.

## 🎯 Project Overview

This full-stack web application combines multiple machine learning algorithms to provide intelligent recipe recommendations and ingredient substitutions. Built to demonstrate ML capabilities for co-op interviews.

## ✨ Core Features

### 1️⃣ **Ingredient Clustering** (K-Means)
- Groups similar ingredients into 5 clusters based on nutritional profiles
- Uses K-Means algorithm with 6 features (protein, carbs, fat, calories, fiber, etc.)
- Interactive visualization of ingredient clusters
- **[📖 Documentation](docs/FEATURE1-README.md)**

### 2️⃣ **Recipe Recommendation** (Collaborative + Content-Based Filtering)
- **Collaborative Filtering**: User-based recommendations using cosine similarity
- **Content-Based Filtering**: Recipe similarity based on ingredient overlap
- Analyzes user preferences and recipe features
- **[📖 Documentation](docs/FEATURE2-README.md)** | **[📊 Visual Flow](docs/FEATURE2-VISUAL-FLOW.md)**

### 3️⃣ **Ingredient Substitution** (Association Rules + Cosine Similarity) ⭐ NEW
- Finds intelligent ingredient substitutes using association rule mining
- Analyzes co-occurrence patterns across 120 world recipes
- Context-aware substitutions using cosine similarity
- Cross-cultural ingredient matching (e.g., soy sauce ↔ fish sauce ↔ tamari)
- **[📖 Documentation](docs/FEATURE3-README.md)** | **[📊 Visual Flow](docs/FEATURE3-VISUAL-FLOW.md)**

## 🌍 Dataset Coverage

- **120 recipes** from **32 cuisines**:
  - 🌏 **Asia**: Chinese, Thai, Japanese, Korean, Indian, Vietnamese
  - 🌍 **Europe**: Italian, French, Spanish, Greek, German, British
  - 🌎 **Americas**: Mexican, American, Tex-Mex, Cajun, Brazilian
  - 🌏 **Middle East**: Lebanese, Turkish, Persian, Egyptian
  - 🌍 **Africa**: Moroccan, Ethiopian, Nigerian, South African
  - 🎨 **Fusion**: Creative cross-cultural dishes
- **262+ unique ingredients** with category mappings
- **15 recipe features** for content-based filtering

## 🛠️ Tech Stack

### Frontend
- **React 18** + **Vite 5.4**
- **Tailwind CSS** for styling
- **Axios** for HTTP requests
- Responsive design with interactive UI

### Backend
- **Python 3.11** + **Flask**
- **NumPy** for matrix operations
- **scikit-learn** for ML algorithms
- **Flask-CORS** for API access
- RESTful API architecture

### ML Algorithms
- **K-Means Clustering** (5 clusters)
- **Cosine Similarity** (collaborative filtering + context matching)
- **Association Rules** (Apriori-like for substitutions)
- **Content-Based Filtering** (ingredient overlap scoring)

## 📦 Project Structure

```
RecipeRecommender/
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main UI with 4 feature tabs
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app.py                   # Flask API server
│   ├── config.py
│   ├── models/
│   │   ├── ingredient_clustering.py      # Feature #1
│   │   ├── recipe_recommender.py         # Feature #2
│   │   ├── ingredient_substitution.py    # Feature #3
│   │   └── world_recipes_data.py         # 120 recipes dataset
│   └── requirements.txt
├── docs/
│   ├── FEATURE2-README.md       # Recipe Recommendation docs
│   ├── FEATURE2-VISUAL-FLOW.md
│   ├── FEATURE3-README.md       # Ingredient Substitution docs
│   └── FEATURE3-VISUAL-FLOW.md
└── README.md                    # This file
```

## 🏃 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```
Backend runs on: **http://localhost:5000**

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: **http://localhost:5173**

## 🎯 API Endpoints

### Ingredient Substitution
- `POST /api/substitute` - Find ingredient substitutes
- `GET /api/substitute/ingredients` - List all available ingredients

### Recipe Recommendation
- `GET /api/recipes` - Get all recipes
- `GET /api/recommend/user/<id>` - Collaborative filtering recommendations
- `GET /api/recommend/similar/<id>` - Content-based similar recipes

### Ingredient Clustering
- `GET /api/cluster/ingredients` - Get ingredient clusters
- `POST /api/cluster/predict` - Predict cluster for new ingredient

### Health Check
- `GET /api/health` - API status

## 📊 Key Metrics & Performance

### Feature #3: Ingredient Substitution
- **Coverage**: 10+ ingredients with substitution rules
- **Precision**: Confidence scores (15-100%)
- **Support**: Co-occurrence frequency in dataset (2-15%)
- **Context Similarity**: Cosine similarity (70-95%)

### Dataset Scale
- **120 recipes** analyzed
- **262 unique ingredients** tracked
- **32 cuisines** represented
- **~30K ingredient pairs** evaluated

## 💡 Interview Talking Points

**"I built a Recipe Recommender System with 3 ML features:"**

1. **K-Means Clustering**: Groups ingredients by nutritional similarity
2. **Collaborative + Content-Based Filtering**: Recommends recipes based on user preferences and recipe features
3. **Association Rule Mining**: Discovers ingredient substitution patterns across world cuisines

**Key Achievement**: The substitution engine learns cross-cultural flavor connections - e.g., it knows soy sauce (Chinese) ↔ fish sauce (Thai) ↔ tamari (Japanese) are interchangeable because they co-occur in fusion recipes!

**Tech Stack**: React + Flask, NumPy for matrix ops, scikit-learn for ML, 120+ recipes from 32 cuisines

**Scale**: 262 ingredients, 262×262 co-occurrence matrix, cosine similarity for context matching

## 🔧 Development Notes

- **Virtual Environment**: `.venv` folder (Python 3.11.1)
- **Hot Reload**: Both frontend (Vite) and backend (Flask debug mode) support live reload
- **CORS Enabled**: Frontend and backend run on different ports
- **No Database**: All data in-memory for demo purposes

## 📚 Documentation

- **[Feature #2: Recipe Recommendation](docs/FEATURE2-README.md)**
- **[Feature #2: Visual Flow](docs/FEATURE2-VISUAL-FLOW.md)**
- **[Feature #3: Ingredient Substitution](docs/FEATURE3-README.md)**
- **[Feature #3: Visual Flow](docs/FEATURE3-VISUAL-FLOW.md)**

## 🎨 UI Features

- **4 Interactive Tabs**: Substitution, Clustering, Collaborative Filtering, Content-Based
- **Hide/Show Controls**: Toggle results and ingredient lists
- **Search Chaining**: "Find more" buttons for exploring substitutions
- **Metric Visualization**: Confidence, support, and similarity scores with progress bars
- **Responsive Design**: Gradient cards, smooth transitions, Tailwind CSS

## 🚀 Future Enhancements

- Add user authentication and preference saving
- Expand dataset to 500+ recipes
- Add dietary restriction filtering (vegan, gluten-free, etc.)
- Implement recipe generation based on available ingredients
- Add nutritional information display

## 📝 License

Educational project for co-op interview demonstration.

---

**Built with ❤️ for ML portfolio and co-op interviews**
