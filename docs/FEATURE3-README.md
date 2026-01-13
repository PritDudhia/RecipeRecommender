# Feature #3: Ingredient Substitution Finder 🔄

## Overview
Association rule mining system that finds ingredient substitutions based on co-occurrence patterns in recipes. Uses context similarity to suggest alternatives when you're missing ingredients.

## 📊 How It Works

### Algorithm: Association Rules (Apriori-like Approach)
- **Method:** Co-occurrence analysis with context similarity
- **Recipes:** 30 sample recipes
- **Ingredients:** 50+ unique ingredients
- **Categories:** 15 ingredient categories (proteins, dairy, grains, etc.)
- **Similarity Metric:** Cosine similarity for context matching

## Core Concept

### 1. **Co-occurrence Matrix**
```
The system builds a matrix showing how often ingredients appear together:

              soy_sauce  ginger  garlic  vegetables  oil
chicken          3         3       3        3         3
tofu             2         2       2        2         2
beef             2         2       2        2         2
```

### 2. **Context Similarity**
Instead of simple "appears together" rules, we use **context similarity**:
- Compare the co-occurrence patterns of two ingredients
- Calculate cosine similarity of their context vectors
- High similarity = ingredients are used in similar recipe contexts

### 3. **Category-Based Filtering**
Only suggest substitutions within compatible categories:
- **Protein substitutions:** chicken ↔ beef ↔ tofu ↔ shrimp
- **Dairy substitutions:** milk ↔ almond milk, cheese ↔ vegan cheese
- **Egg substitutions:** eggs ↔ flax eggs
- **Sauce substitutions:** soy sauce ↔ fish sauce

## Example: How "Chicken" Gets Substitutes

```python
# Step 1: Find chicken's co-occurrence pattern
chicken appears with: [soy sauce, ginger, garlic, vegetables, oil, lemon, herbs...]

# Step 2: Find other proteins with similar patterns
beef appears with: [soy sauce, garlic, vegetables, oil, tomato sauce...]
tofu appears with: [soy sauce, ginger, garlic, vegetables, oil...]

# Step 3: Calculate context similarity
chicken vs beef:   0.734 (73.4% similar context)
chicken vs tofu:   0.589 (58.9% similar context)
chicken vs shrimp: 0.590 (59.0% similar context)

# Step 4: Return top substitutes
1. beef     (confidence: 73.4%, category: protein_meat)
2. shrimp   (confidence: 59.0%, category: protein_seafood)
3. tofu     (confidence: 58.9%, category: protein_plant)
```

## API Endpoints

### POST `/api/substitute`
Find substitutes for an ingredient

**Request:**
```json
{
  "ingredient": "chicken",
  "top_n": 5
}
```

**Response:**
```json
{
  "ingredient": "chicken",
  "ingredient_info": {
    "ingredient": "chicken",
    "category": "protein_meat",
    "appears_in": 7,
    "total_recipes": 30,
    "frequency": 0.233
  },
  "substitutes": [
    {
      "substitute": "beef",
      "confidence": 0.734,
      "support": 0.167,
      "category": "protein_meat"
    },
    {
      "substitute": "shrimp",
      "confidence": 0.590,
      "support": 0.133,
      "category": "protein_seafood"
    }
  ],
  "total_found": 2,
  "method": "association_rules"
}
```

### GET `/api/substitute/ingredients`
Get all available ingredients

**Response:**
```json
{
  "ingredients": [
    "avocado",
    "bacon",
    "basil",
    "beef",
    "chicken",
    ...
  ],
  "total": 52
}
```

## Understanding the Metrics

### 📊 Confidence Score (0-1)
- **What it means:** How similar the ingredients are based on usage context
- **Calculation:** Cosine similarity of co-occurrence vectors
- **High value (>0.7):** Very similar usage patterns, excellent substitute
- **Medium value (0.4-0.7):** Moderately similar, good substitute
- **Low value (<0.4):** Less similar, acceptable substitute

### 📊 Support Score (0-1)
- **What it means:** How frequently the ingredient appears in recipes
- **Calculation:** (recipes containing ingredient) / (total recipes)
- **High value (>0.3):** Common ingredient, widely used
- **Low value (<0.1):** Rare ingredient, specialized

### 📊 Category
The ingredient classification for smart filtering:
- `protein_meat`: chicken, beef, bacon
- `protein_seafood`: fish, salmon, shrimp
- `protein_plant`: tofu, lentils
- `dairy`: milk, cheese, butter
- `dairy_substitute`: almond milk, vegan cheese, coconut oil
- `grain_pasta`: pasta, spaghetti
- `grain_rice`: rice
- And more...

## Sample Data

### Recipe Examples
1. **Chicken Stir Fry:** chicken, soy sauce, ginger, garlic, vegetables, oil
2. **Tofu Stir Fry:** tofu, soy sauce, ginger, garlic, vegetables, oil
3. **Beef Tacos:** beef, tortillas, cheese, salsa, avocado, lime
4. **Fish Tacos:** fish, tortillas, cheese, salsa, avocado, lime
5. **Vegan Pizza:** dough, tomato sauce, vegan cheese, basil, olive oil

### Substitution Examples

| Original | Substitutes | Use Case |
|----------|------------|----------|
| Chicken | Beef, Shrimp, Tofu | Main protein source |
| Eggs | Flax eggs | Vegan cooking |
| Milk | Almond milk | Dairy-free recipes |
| Cheese | Vegan cheese, Feta cheese | Toppings & sauces |
| Beef | Chicken, Lentils | Meat alternatives |
| Butter | Coconut oil | Baking substitutes |

## Algorithm Parameters

```python
IngredientSubstitutionFinder(
    min_support=0.1,      # Ingredient must appear in ≥10% of recipes
    min_confidence=0.3    # ≥30% context similarity required
)
```

### Tuning Parameters:
- **Lower min_support:** More ingredients included, but may include rare ones
- **Higher min_support:** Only common ingredients, fewer options
- **Lower min_confidence:** More substitutes suggested, less strict matching
- **Higher min_confidence:** Fewer substitutes, stricter similarity

## Use Cases

### 🛒 Grocery Shopping
"I don't have chicken, what can I use?"
→ Suggests: beef, tofu, shrimp

### 🥗 Dietary Restrictions
"I'm vegan, what can replace eggs?"
→ Suggests: flax eggs

### 🍳 Recipe Adaptation
"I want to make tacos but with fish instead of beef"
→ Confirms: fish is a valid substitute for beef in tacos

### 📝 Meal Planning
"What proteins work well with stir-fry ingredients?"
→ Shows: chicken, tofu, beef, shrimp all work

## Technical Implementation

### Step 1: Build Co-occurrence Matrix
```python
# For each recipe, count ingredient pairs
cooccurrence[chicken][soy_sauce] += 1
cooccurrence[chicken][ginger] += 1
# ... etc
```

### Step 2: Calculate Context Similarity
```python
# Get co-occurrence vectors
chicken_context = [3, 3, 3, ...]  # appears with these ingredients
beef_context = [2, 2, 2, ...]

# Calculate cosine similarity
similarity = dot(chicken_context, beef_context) / (norm(chicken) * norm(beef))
```

### Step 3: Filter by Category
```python
# Only suggest if categories are compatible
if is_substitutable_category(chicken_category, beef_category):
    add_substitution(chicken -> beef, similarity)
```

### Step 4: Rank and Return
```python
# Sort by confidence (similarity score)
substitutes.sort(key=lambda x: x['confidence'], reverse=True)
return top_n_substitutes
```

## Advantages of This Approach

✅ **Context-Aware:** Considers how ingredients are actually used together
✅ **Category-Safe:** Only suggests sensible substitutions (protein for protein)
✅ **Data-Driven:** Based on real recipe patterns, not hard-coded rules
✅ **Scalable:** Works with any number of recipes/ingredients
✅ **Explainable:** Confidence scores show similarity strength

## Limitations

⚠️ **Sample Data:** Current system uses 30 recipes (production needs 1000s)
⚠️ **Context Only:** Doesn't consider flavor profiles or cooking methods
⚠️ **Binary Presence:** Doesn't account for ingredient quantities
⚠️ **Cold Start:** New ingredients without co-occurrence data get no suggestions

## Future Enhancements

1. **Flavor Profile Matching:** Add taste similarity (sweet, salty, umami)
2. **Nutritional Equivalence:** Match calorie/protein content
3. **Cooking Method Compatibility:** Consider preparation techniques
4. **User Ratings:** Learn from user feedback on substitutions
5. **Quantity Scaling:** Suggest measurement adjustments
6. **Cultural Context:** Region-specific substitution preferences

## Testing

### Quick Test Examples:

```bash
# Test 1: Find chicken substitutes
curl -X POST http://localhost:5000/api/substitute \
  -H "Content-Type: application/json" \
  -d '{"ingredient": "chicken", "top_n": 5}'

# Test 2: Find dairy alternatives
curl -X POST http://localhost:5000/api/substitute \
  -H "Content-Type: application/json" \
  -d '{"ingredient": "milk"}'

# Test 3: Get all ingredients
curl http://localhost:5000/api/substitute/ingredients
```

### Expected Results:

**Chicken:**
- Beef (high confidence, same protein category)
- Shrimp (medium confidence, different protein type)

**Milk:**
- May have limited results with current sample data
- In production: almond milk, soy milk, coconut milk

## Learning Points

### For Understanding ML:
1. **Association Rules:** Finding patterns in co-occurring items
2. **Cosine Similarity:** Measuring vector similarity
3. **Category Filtering:** Domain knowledge constraints
4. **Support/Confidence:** Standard association rule metrics (adapted)

### For Understanding the Code:
1. **Matrix Operations:** NumPy for co-occurrence counting
2. **Category Mapping:** Dictionary-based classification
3. **Rule Generation:** Iterating through ingredient pairs
4. **Ranking Algorithm:** Sort by confidence score

---

**ML Algorithm:** Association Rules (Modified Apriori-like approach)
**Key Innovation:** Context similarity instead of simple co-occurrence
**Data Structure:** Co-occurrence matrix + category mapping
**Output:** Ranked list of substitutions with confidence scores

🔄 **This feature demonstrates how association rule mining can solve real-world cooking problems!**
