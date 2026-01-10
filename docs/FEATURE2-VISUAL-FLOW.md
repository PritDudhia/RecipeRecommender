# Feature #2: Recipe Recommendation - Visual Flow Documentation

## 🎯 System Overview

This feature implements **two recommendation algorithms**:
1. **Collaborative Filtering**: Recommends recipes based on similar users' preferences
2. **Content-Based Filtering**: Finds similar recipes based on features

---

## 📊 Main Application Flow

```mermaid
graph TB
    Start([User Opens App]) --> TabSelect{Select Algorithm}
    
    TabSelect -->|Collaborative| UserSelect[Select User Profile<br/>10 profiles available]
    TabSelect -->|Content-Based| RecipeSelect[Browse 15 Recipes]
    
    UserSelect --> GetRecs[Click 'Get Recommendations']
    GetRecs --> API1[GET /api/recommend/user/:id]
    API1 --> ColabAlgo[Collaborative Filtering Algorithm]
    
    RecipeSelect --> ClickRecipe[Click Recipe Card]
    ClickRecipe --> API2[GET /api/recommend/similar/:id]
    API2 --> ContentAlgo[Content-Based Filtering Algorithm]
    
    ColabAlgo --> Result1[Display Predicted Ratings<br/>5 personalized recipes]
    ContentAlgo --> Result2[Display Similarity Scores<br/>5 similar recipes]
    
    Result1 --> End([User Views Recommendations])
    Result2 --> End
    
    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style ColabAlgo fill:#e1d5f0
    style ContentAlgo fill:#fce4ec
    style Result1 fill:#e1d5f0
    style Result2 fill:#fce4ec
```

---

## 🤖 Collaborative Filtering Algorithm

```mermaid
graph LR
    A[User ID<br/>user_id: 0-9] --> B[Load User Ratings<br/>user_item_matrix row]
    B --> C[Calculate User Similarity<br/>cosine_similarity]
    C --> D[For each unrated recipe]
    D --> E{Other users<br/>rated it?}
    E -->|Yes| F[Weighted Rating<br/>rating × similarity]
    E -->|No| G[Skip recipe]
    F --> H[Sum weighted ratings<br/>÷ total similarity]
    H --> I[Predicted Rating]
    I --> J[Sort by rating DESC]
    J --> K[Return Top 5]
    
    style A fill:#b39ddb
    style K fill:#ba68c8
    style I fill:#ce93d8
```

**Formula:**
$$\text{predicted\_rating} = \frac{\sum_{u \in similar\_users} (rating_u \times similarity_u)}{\sum_{u \in similar\_users} similarity_u}$$

---

## 🔍 Content-Based Filtering Algorithm

```mermaid
graph LR
    A[Recipe ID<br/>recipe_id: 1-15] --> B[Extract Features<br/>5-dimensional vector]
    B --> C[Feature Vector<br/>[prep, diff, spice, sweet, health]]
    C --> D[Calculate Similarity Matrix<br/>cosine_similarity]
    D --> E[Get row for target recipe]
    E --> F[Sort similarities DESC]
    F --> G[Exclude target recipe]
    G --> H[Return Top 5]
    
    style A fill:#f48fb1
    style H fill:#f06292
    style D fill:#f8bbd0
```

**Features:**
- `prep_time`: Minutes to prepare (15-90)
- `difficulty`: Scale 1-5
- `spice_level`: Scale 0-5
- `sweetness`: Scale 0-5
- `healthiness`: Scale 1-5

---

## 🌐 API Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant React
    participant Flask
    participant ML Model
    
    Note over User,ML Model: Collaborative Filtering Flow
    
    User->>React: Select User 1 (healthy food lover)
    User->>React: Click "Get Recommendations"
    React->>Flask: GET /api/recommend/user/0?top_n=5
    Flask->>ML Model: get_user_based_recommendations(user_id=0)
    ML Model->>ML Model: Load user_item_matrix[0]
    ML Model->>ML Model: Calculate user similarities
    ML Model->>ML Model: Predict ratings for unrated recipes
    ML Model-->>Flask: recommendations[5] with predicted_rating
    Flask-->>React: JSON {recommendations: [...]}
    React->>User: Display 5 recipe cards with ratings
    
    Note over User,ML Model: Content-Based Filtering Flow
    
    User->>React: Click "Chicken Stir Fry" card
    React->>Flask: GET /api/recommend/similar/1?top_n=5
    Flask->>ML Model: get_content_based_recommendations(recipe_id=1)
    ML Model->>ML Model: Get feature vector [20, 2, 3, 1, 4]
    ML Model->>ML Model: Calculate cosine similarity to all recipes
    ML Model->>ML Model: Sort by similarity score
    ML Model-->>Flask: recommendations[5] with similarity_score
    Flask-->>React: JSON {recommendations: [...]}
    React->>User: Display 5 similar recipe cards with %
```

---

## 🗂️ Data Structure

```mermaid
graph TB
    subgraph User-Item Matrix
        A[10 Users × 15 Recipes]
        A --> B[Ratings: 0-5<br/>0 = not rated]
    end
    
    subgraph Recipe Features
        C[15 Recipes]
        C --> D[5 Features per recipe<br/>[prep, diff, spice, sweet, health]]
    end
    
    subgraph Similarity Matrices
        E[User Similarity<br/>10×10 matrix]
        F[Recipe Similarity<br/>15×15 matrix]
    end
    
    A --> E
    D --> F
    
    style A fill:#e1d5f0
    style D fill:#fce4ec
    style E fill:#b39ddb
    style F fill:#f48fb1
```

---

## 🎨 UI Component Structure

```mermaid
graph TD
    App[App Component] --> Header[Header<br/>Title + API Status]
    App --> TabNav[Tab Navigation<br/>Collaborative / Content-Based]
    
    TabNav --> Tab1{Collaborative Tab}
    TabNav --> Tab2{Content-Based Tab}
    
    Tab1 --> UserDropdown[User Dropdown<br/>10 profiles]
    UserDropdown --> GetButton[Get Recommendations Button]
    GetButton --> UserResults[Recommendation Cards<br/>predicted_rating displayed]
    
    Tab2 --> RecipeGrid[Recipe Grid<br/>15 clickable cards]
    RecipeGrid --> SimilarResults[Similar Recipe Cards<br/>similarity_score displayed]
    
    App --> Footer[ML Info Footer<br/>Algorithm descriptions]
    
    style App fill:#fff9c4
    style Tab1 fill:#e1d5f0
    style Tab2 fill:#fce4ec
    style UserResults fill:#ce93d8
    style SimilarResults fill:#f48fb1
```

---

## 🧪 Testing Scenarios

### Scenario 1: Healthy Food Lover
```mermaid
graph LR
    A[Select User 1] --> B[Likes healthy food]
    B --> C[Get Recommendations]
    C --> D[Quinoa Bowl<br/>Rating: 4.8]
    C --> E[Grilled Salmon<br/>Rating: 4.5]
    C --> F[Greek Salad<br/>Rating: 4.2]
    
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style F fill:#c8e6c9
```

### Scenario 2: Find Similar to Chicken Stir Fry
```mermaid
graph LR
    A[Click Chicken Stir Fry] --> B[Asian, 20min, Spice:3]
    B --> C[Find Similar]
    C --> D[Vegetable Stir Fry<br/>89% match]
    C --> E[Pad Thai<br/>78% match]
    C --> F[Beef Tacos<br/>65% match]
    
    style D fill:#ffccbc
    style E fill:#ffccbc
    style F fill:#ffccbc
```

---

## 📦 Technology Stack

```mermaid
graph TB
    subgraph Frontend
        A[React 18.2.0]
        B[Axios HTTP Client]
        C[Tailwind CSS]
    end
    
    subgraph Backend
        D[Flask 3.0.0]
        E[Flask-CORS]
    end
    
    subgraph ML Libraries
        F[scikit-learn 1.3.2]
        G[NumPy 1.26.2]
        H[Cosine Similarity]
    end
    
    A --> D
    B --> D
    D --> F
    F --> H
    G --> H
    
    style A fill:#61dafb
    style D fill:#000000
    style F fill:#f89939
```

---

## 🎯 Key Metrics

- **User Profiles**: 10 with distinct preferences
- **Recipe Database**: 15 diverse recipes (Asian, Italian, Mexican, etc.)
- **Rating Scale**: 1-5 stars
- **Feature Dimensions**: 5 per recipe
- **Recommendation Count**: Top 5 per query
- **Similarity Metric**: Cosine similarity
- **Response Time**: <100ms

---

## 🔄 Recommendation Flow Comparison

| Aspect | Collaborative Filtering | Content-Based Filtering |
|--------|------------------------|-------------------------|
| **Input** | User ID (0-9) | Recipe ID (1-15) |
| **Data Source** | User-item rating matrix | Recipe feature vectors |
| **Similarity** | User-to-user | Recipe-to-recipe |
| **Output** | Predicted rating (0-5) | Similarity score (0-1) |
| **Use Case** | "What will I like?" | "What's similar to this?" |
| **Cold Start** | Needs user history | Works immediately |

---

**Status:** ✅ Complete | **Branch:** `feature/recipe-recommendation` | **Demo:** http://localhost:5173
