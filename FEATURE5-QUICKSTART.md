# Feature #5: Nutrition Predictor - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Backend
```bash
cd backend
python app.py
```

You should see:
```
🍽️  Training Nutrition Predictor...
✅ Models trained on 120 recipes
📊 Model type: Ridge Regression
✅ Nutrition predictor ready!
🚀 Starting Recipe Recommender Backend...
📍 API available at: http://localhost:5000
```

### Step 2: Start the Frontend
```bash
cd frontend
npm run dev
```

### Step 3: Use the Nutrition Predictor
1. Open http://localhost:5173
2. Click on "🍎 Nutrition Predictor" tab (it's the default)
3. Try one of these:

---

## 📝 Try These Examples

### Example 1: Custom Ingredients
**Input:** `chicken, rice, broccoli, soy sauce`

**Click:** "Predict Nutrition"

**Result:**
```
🔥 Calories:  202 kcal
💪 Protein:   11.3g
🥑 Fat:       13.1g
🍞 Carbs:     4.9g
🌾 Fiber:     -2.9g
```

---

### Example 2: Select a Recipe
**Click:** Any recipe button (e.g., "1. Kung Pao Chicken")

**Result:**
```
🍽️ Kung Pao Chicken (Chinese)

Ingredients: chicken, peanuts, soy sauce, ginger, garlic, 
            chili peppers, rice vinegar, cornstarch, scallions

Nutritional Information (per serving)
🔥 Calories:  953 kcal
💪 Protein:   64.6g
🥑 Fat:       36.3g
🍞 Carbs:     98.4g
🌾 Fiber:     16.5g
```

---

### Example 3: Compare Recipes
**Input in "Compare Multiple Recipes":** `1, 6, 11`

**Click:** "Compare"

**Result:**
```
Nutrition Comparison (3 recipes)

📖 Kung Pao Chicken (Chinese)
   🔥 953  💪 64.6g  🥑 36.3g  🍞 98.4g  🌾 16.5g

📖 Pad Thai (Thai)
   🔥 953  💪 64.6g  🥑 36.3g  🍞 98.4g  🌾 16.5g

📖 Chicken Teriyaki (Japanese)
   🔥 677  💪 46.4g  🥑 27.2g  🍞 67.7g  🌾 13.5g
```

---

## 🧪 Try the Test Script

Run all automated tests:
```bash
python test_nutrition_predictor.py
```

You'll see:
```
🍎 NUTRITION PREDICTOR - FEATURE #5 TEST SUITE
✅ Backend API is running!

🧪 TEST 1: Predict Nutrition from Custom Ingredients
🧪 TEST 2: Get Recipe Nutrition
🧪 TEST 3: Compare Multiple Recipes
🧪 TEST 4: Get Model Performance Metrics
🧪 TEST 5: Nutrition Across Different Cuisines

🎉 All tests completed!
```

---

## 🎯 More Examples to Try

### High Protein Meals
```
Input: chicken, quinoa, eggs, greek yogurt
Expected: High protein content
```

### Low Carb Options
```
Input: salmon, asparagus, olive oil, lemon
Expected: Low carb content
```

### Vegetarian
```
Input: tofu, brown rice, vegetables, soy sauce
Expected: Moderate protein from tofu
```

### Mediterranean
```
Input: pasta, tomato sauce, mozzarella, basil, olive oil
Expected: Balanced macros
```

### Asian Fusion
```
Input: shrimp, noodles, vegetables, fish sauce, ginger
Expected: High protein, moderate carbs
```

---

## 📊 Understanding the Results

### What Each Metric Means

**🔥 Calories** (kcal)
- Energy content of the meal
- Typical range: 200-1000 kcal per serving
- Goal: 400-600 for main meals

**💪 Protein** (grams)
- Essential for muscle and tissue
- Typical range: 10-70g per serving
- Goal: 20-30g for main meals

**🥑 Fat** (grams)
- Energy and nutrient absorption
- Typical range: 5-40g per serving
- Goal: 10-20g for balanced meals

**🍞 Carbs** (grams)
- Primary energy source
- Typical range: 20-100g per serving
- Goal: 40-60g for balanced meals

**🌾 Fiber** (grams)
- Digestive health
- Typical range: 2-15g per serving
- Goal: 5-10g for good nutrition

---

## 🔍 API Endpoints Reference

### 1. Predict Custom Ingredients
```bash
POST http://localhost:5000/api/nutrition/predict
Body: {"ingredients": ["chicken", "rice", "broccoli"]}
```

### 2. Get Recipe Nutrition
```bash
GET http://localhost:5000/api/nutrition/recipe/1
```

### 3. Compare Recipes
```bash
POST http://localhost:5000/api/nutrition/compare
Body: {"recipe_ids": [1, 6, 11]}
```

### 4. Model Metrics
```bash
GET http://localhost:5000/api/nutrition/metrics
```

---

## 💡 Tips & Tricks

### Best Practices
1. **Use common ingredients** - The model knows 200+ ingredients
2. **Be specific** - "chicken breast" vs "chicken"
3. **Add variety** - Include proteins, grains, and vegetables
4. **Compare similar recipes** - See which is healthier

### Common Ingredients That Work Well
- **Proteins:** chicken, beef, pork, salmon, tofu, eggs
- **Grains:** rice, pasta, bread, quinoa
- **Vegetables:** broccoli, spinach, tomatoes, carrots
- **Dairy:** milk, cheese, yogurt
- **Oils:** olive oil, sesame oil
- **Sauces:** soy sauce, tomato sauce

### Recipe IDs Reference (First 20)
```
1-5:   Chinese (Kung Pao Chicken, Mapo Tofu, etc.)
6-10:  Thai (Pad Thai, Green Curry, etc.)
11-15: Japanese (Chicken Teriyaki, Ramen, etc.)
16-20: Korean (Bibimbap, Bulgogi, etc.)
21-25: Vietnamese
26-30: Indian
31-35: Italian
36-40: Mexican
```

---

## 🎨 Frontend Features

### Input Methods
1. ✏️ **Text Input** - Type ingredients separated by commas
2. 🔘 **Recipe Buttons** - Click any of 40 recipes
3. 🔢 **Compare IDs** - Enter recipe IDs to compare

### Display Features
- 🎨 **Color-coded nutrients** - Easy to scan
- 📊 **Visual cards** - Clean, modern design
- 🌍 **Cuisine info** - Know the origin
- 🥘 **Ingredient list** - See what's included

---

## 🐛 Troubleshooting

### Backend not starting?
```bash
# Make sure you're in the right directory
cd backend

# Check if virtual environment is activated
python --version

# Install dependencies if needed
pip install -r requirements.txt
```

### Frontend not loading?
```bash
# Install dependencies
cd frontend
npm install

# Clear cache and restart
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API not responding?
- Check if backend is running on http://localhost:5000
- Look for errors in backend terminal
- Try: `curl http://localhost:5000/api/health`

---

## 📖 Learn More

- **Feature Documentation:** `docs/FEATURE5-README.md`
- **Visual Flows:** `docs/FEATURE5-VISUAL-FLOW.md`
- **Implementation Summary:** `FEATURE5-SUMMARY.md`
- **Test Script:** `test_nutrition_predictor.py`

---

**Ready to predict some nutrition? Let's go! 🚀**
