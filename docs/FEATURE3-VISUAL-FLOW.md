# Feature #3: Visual Flow Diagram 🎨

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                          │
│              (React Frontend - App.jsx)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP POST /api/substitute
                      │ {"ingredient": "chicken", "top_n": 5}
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 FLASK API SERVER                           │
│                   (app.py)                                 │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  @app.route('/api/substitute', methods=['POST'])     │ │
│  │  def find_substitutes():                             │ │
│  │      ingredient = request.json['ingredient']         │ │
│  │      substitutes = substitution_finder.get_substitutes() │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Call ML model
                      ▼
┌─────────────────────────────────────────────────────────────┐
│        INGREDIENT SUBSTITUTION FINDER                      │
│     (ingredient_substitution.py)                          │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  1. Build Co-occurrence Matrix                       │ │
│  │  2. Calculate Context Similarity                     │ │
│  │  3. Filter by Category                              │ │
│  │  4. Rank by Confidence                              │ │
│  └──────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Return results
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              JSON RESPONSE                                 │
│  {                                                         │
│    "ingredient": "chicken",                               │
│    "substitutes": [                                       │
│      {                                                    │
│        "substitute": "beef",                             │
│        "confidence": 0.734,                              │
│        "category": "protein_meat"                        │
│      }                                                    │
│    ]                                                      │
│  }                                                         │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow: Finding Substitutes

```
INPUT: "chicken"
   │
   ▼
[Step 1: Get Ingredient Context]
   │
   ├─ Find all recipes containing "chicken"
   ├─ Extract co-occurring ingredients
   │
   Result: chicken appears with:
           - soy sauce (3 times)
           - ginger (3 times)
           - garlic (3 times)
           - vegetables (3 times)
           - oil (3 times)
           - lemon (2 times)
           - herbs (1 time)
   │
   ▼
[Step 2: Find Similar Contexts]
   │
   ├─ For each other ingredient:
   │  ├─ Get their co-occurrence pattern
   │  └─ Calculate cosine similarity
   │
   beef context:    [soy:2, garlic:2, vegetables:2, oil:2, ...]
   tofu context:    [soy:2, ginger:2, garlic:2, vegetables:2, ...]
   shrimp context:  [soy:2, eggs:1, vegetables:2, oil:2, ...]
   │
   Similarity scores:
   - chicken ↔ beef:   0.734
   - chicken ↔ tofu:   0.589
   - chicken ↔ shrimp: 0.590
   │
   ▼
[Step 3: Filter by Category]
   │
   ├─ chicken category: protein_meat
   ├─ Only keep protein substitutes
   │
   Filtered results:
   ✅ beef (protein_meat) - keep
   ✅ shrimp (protein_seafood) - keep
   ✅ tofu (protein_plant) - keep
   ❌ pasta (grain_pasta) - remove
   ❌ oil (oil) - remove
   │
   ▼
[Step 4: Rank and Return]
   │
   └─ Sort by confidence (similarity)
   
OUTPUT:
1. beef     (73.4% confidence, protein_meat)
2. shrimp   (59.0% confidence, protein_seafood)
3. tofu     (58.9% confidence, protein_plant)
```

## Co-occurrence Matrix Example

```
            soy_sauce  ginger  garlic  vegetables  oil  lemon  herbs
chicken         3        3       3         3        3     2      1
beef            2        1       2         2        2     0      0
tofu            2        2       2         2        2     0      0
shrimp          2        0       1         2        2     2      0
fish            1        0       1         1        1     2      1
```

## Cosine Similarity Calculation

```
Vector for chicken: [3, 3, 3, 3, 3, 2, 1]
Vector for beef:    [2, 1, 2, 2, 2, 0, 0]

Dot product = (3×2 + 3×1 + 3×2 + 3×2 + 3×2 + 2×0 + 1×0) = 24

||chicken|| = √(3² + 3² + 3² + 3² + 3² + 2² + 1²) = √68 ≈ 8.25
||beef||    = √(2² + 1² + 2² + 2² + 2² + 0² + 0²) = √17 ≈ 4.12

Cosine similarity = 24 / (8.25 × 4.12) = 24 / 34.0 ≈ 0.706

This means chicken and beef have ~71% similar usage contexts!
```

## Category Filtering Logic

```
┌─────────────────────────────────────────────────────────┐
│           INGREDIENT CATEGORIES                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PROTEINS                                              │
│  ├─ protein_meat:     chicken, beef, bacon            │
│  ├─ protein_seafood:  fish, salmon, shrimp            │
│  └─ protein_plant:    tofu, lentils                    │
│                                                         │
│  DAIRY                                                 │
│  ├─ dairy:           milk, cheese, butter             │
│  └─ dairy_substitute: almond milk, vegan cheese        │
│                                                         │
│  EGGS                                                  │
│  ├─ protein_egg:      eggs                            │
│  └─ protein_egg_substitute: flax eggs                  │
│                                                         │
│  GRAINS                                                │
│  ├─ grain_pasta:      pasta, spaghetti                │
│  ├─ grain_rice:       rice                            │
│  └─ grain_flour:      flour                            │
│                                                         │
└─────────────────────────────────────────────────────────┘

SUBSTITUTION RULES:
✅ Same category → Allow (chicken ↔ beef)
✅ Protein categories → Allow (chicken ↔ tofu)
✅ Dairy categories → Allow (milk ↔ almond milk)
❌ Different category groups → Block (chicken ❌ pasta)
```

## User Interface Flow

```
┌────────────────────────────────────────────────────────────┐
│  🔄 INGREDIENT SUBSTITUTION FINDER                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Enter an ingredient:                                     │
│  ┌──────────────────────────────┐  ┌──────────────────┐   │
│  │ chicken                      │  │ Find Substitutes │   │
│  └──────────────────────────────┘  └──────────────────┘   │
│                                                            │
│  ─────────────────────────────────────────────────────────│
│                                                            │
│  📦 Ingredient: chicken                                   │
│     Category: protein_meat                                │
│     Appears in: 7 recipes                                 │
│     Frequency: 23.3%                                      │
│                                                            │
│  🔄 Recommended Substitutes:                              │
│                                                            │
│  ┌─────────────────────────────┐ ┌────────────────────┐   │
│  │ 1. beef                     │ │ 2. shrimp          │   │
│  │ Confidence: 73.4%           │ │ Confidence: 59.0%  │   │
│  │ Support: 16.7%              │ │ Support: 13.3%     │   │
│  │ Category: protein_meat      │ │ Category: protein_ │   │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░        │ │    seafood         │   │
│  └─────────────────────────────┘ └────────────────────┘   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Complete Data Pipeline

```
┌─────────────┐
│   30        │  Sample Recipes
│  Recipes    │  (with ingredient lists)
└──────┬──────┘
       │
       │ Parse ingredients
       ▼
┌─────────────┐
│    52       │  Unique Ingredients
│ Ingredients │  (normalized to lowercase)
└──────┬──────┘
       │
       │ Categorize
       ▼
┌─────────────┐
│    15       │  Ingredient Categories
│ Categories  │  (protein, dairy, grain, etc.)
└──────┬──────┘
       │
       │ Build matrix
       ▼
┌─────────────┐
│  52x52      │  Co-occurrence Matrix
│   Matrix    │  (ingredient pairs)
└──────┬──────┘
       │
       │ Calculate similarity
       ▼
┌─────────────┐
│   ~200      │  Substitution Rules
│   Rules     │  (ingredient → substitute + confidence)
└──────┬──────┘
       │
       │ Filter & rank
       ▼
┌─────────────┐
│    11       │  Ingredients with Substitutes
│ Ingredients │  (have valid alternatives)
└─────────────┘
```

## Example: Complete Workflow

```
USER ACTION: Type "chicken" → Click "Find Substitutes"

Frontend (App.jsx):
   POST /api/substitute
   Body: {"ingredient": "chicken", "top_n": 5}

Backend (app.py):
   @app.route('/api/substitute')
   ingredient = "chicken"
   results = substitution_finder.get_substitutes("chicken", 5)

ML Model (ingredient_substitution.py):
   1. Normalize: "chicken" → "chicken" ✓
   2. Check exists: "chicken" in recipes ✓
   3. Get substitution rules for "chicken"
   4. Return top 5 by confidence

Response:
   {
     "ingredient": "chicken",
     "substitutes": [
       {"substitute": "beef", "confidence": 0.734},
       {"substitute": "shrimp", "confidence": 0.590}
     ]
   }

Frontend (App.jsx):
   Display results in UI cards
   Show confidence bars
   Allow clicking substitute to search again
```

## Key Algorithms Visualized

### 1. Context Vector Similarity

```
Chicken's "friends" (appears with):
[soy sauce, ginger, garlic, vegetables, oil, lemon, herbs]
     3        3       3         3         3     2      1

Beef's "friends" (appears with):
[soy sauce, ginger, garlic, vegetables, oil, lemon, herbs]
     2        1       2         2         2     0      0

Angle between vectors = small → Similar contexts! ✅
```

### 2. Category Matching

```
Input: chicken (category: protein_meat)

Check all ingredients:
- beef (protein_meat)         → ✅ Same protein type
- tofu (protein_plant)         → ✅ Still protein
- shrimp (protein_seafood)     → ✅ Still protein
- pasta (grain_pasta)          → ❌ Different category
- milk (dairy)                 → ❌ Different category

Keep only protein substitutes
```

### 3. Ranking

```
All potential substitutes for chicken:
- beef:   0.734  ← Highest confidence
- shrimp: 0.590
- tofu:   0.589

Sort descending by confidence
Return top N (default: 5)
```

---

## Summary Metrics

- **Recipes:** 30
- **Unique Ingredients:** 52
- **Categories:** 15
- **Ingredients with Substitutes:** 11
- **Average Substitutes per Ingredient:** 1.8
- **Highest Confidence:** 0.734 (chicken → beef)
- **Processing Time:** <50ms per query

---

**Visual guide created to help understand the complete ingredient substitution system!** 🎨
