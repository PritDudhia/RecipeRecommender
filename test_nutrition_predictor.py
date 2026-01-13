"""
Test script for Nutrition Predictor - Feature #5
Run this to verify the nutrition prediction functionality
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def print_separator():
    print("\n" + "="*80 + "\n")

def test_predict_custom_ingredients():
    """Test predicting nutrition from custom ingredients"""
    print("🧪 TEST 1: Predict Nutrition from Custom Ingredients")
    print_separator()
    
    ingredients = ["chicken", "rice", "broccoli", "soy sauce"]
    print(f"Ingredients: {', '.join(ingredients)}")
    
    response = requests.post(f'{BASE_URL}/api/nutrition/predict', 
                            json={'ingredients': ingredients})
    data = response.json()
    
    if data['success']:
        print("\n✅ Success!")
        print(f"\nNutritional Information:")
        print(f"  🔥 Calories:  {data['nutrition']['calories']} kcal")
        print(f"  💪 Protein:   {data['nutrition']['protein']}g")
        print(f"  🥑 Fat:       {data['nutrition']['fat']}g")
        print(f"  🍞 Carbs:     {data['nutrition']['carbs']}g")
        print(f"  🌾 Fiber:     {data['nutrition']['fiber']}g")
        print(f"\n  Model: {data['model']}")
    else:
        print(f"❌ Error: {data.get('error', 'Unknown error')}")

def test_recipe_nutrition():
    """Test getting nutrition for a specific recipe"""
    print("🧪 TEST 2: Get Recipe Nutrition")
    print_separator()
    
    recipe_id = 1
    response = requests.get(f'{BASE_URL}/api/nutrition/recipe/{recipe_id}')
    data = response.json()
    
    if data['success']:
        print("✅ Success!")
        print(f"\nRecipe: {data['recipe_name']}")
        print(f"Cuisine: {data['cuisine']}")
        print(f"\nIngredients: {', '.join(data['ingredients'])}")
        print(f"\nNutritional Information:")
        print(f"  🔥 Calories:  {data['nutrition']['calories']} kcal")
        print(f"  💪 Protein:   {data['nutrition']['protein']}g")
        print(f"  🥑 Fat:       {data['nutrition']['fat']}g")
        print(f"  🍞 Carbs:     {data['nutrition']['carbs']}g")
        print(f"  🌾 Fiber:     {data['nutrition']['fiber']}g")
    else:
        print(f"❌ Error: {data.get('error', 'Unknown error')}")

def test_compare_recipes():
    """Test comparing nutrition of multiple recipes"""
    print("🧪 TEST 3: Compare Multiple Recipes")
    print_separator()
    
    recipe_ids = [1, 6, 11]
    print(f"Comparing recipes: {recipe_ids}")
    
    response = requests.post(f'{BASE_URL}/api/nutrition/compare',
                            json={'recipe_ids': recipe_ids})
    data = response.json()
    
    if data['success']:
        print(f"\n✅ Success! Comparing {data['total']} recipes:\n")
        
        for recipe in data['recipes']:
            print(f"📖 {recipe['recipe_name']} ({recipe['cuisine']})")
            print(f"   Calories: {recipe['nutrition']['calories']} | "
                  f"Protein: {recipe['nutrition']['protein']}g | "
                  f"Fat: {recipe['nutrition']['fat']}g | "
                  f"Carbs: {recipe['nutrition']['carbs']}g | "
                  f"Fiber: {recipe['nutrition']['fiber']}g")
            print()
    else:
        print(f"❌ Error: {data.get('error', 'Unknown error')}")

def test_model_metrics():
    """Test getting model performance metrics"""
    print("🧪 TEST 4: Get Model Performance Metrics")
    print_separator()
    
    response = requests.get(f'{BASE_URL}/api/nutrition/metrics')
    data = response.json()
    
    if data['success']:
        print("✅ Success!")
        print(f"\nModel Type: {data['model_type']}")
        print("\nPerformance Metrics:")
        print(f"{'Nutrient':<12} {'MAE':<10} {'R² Score':<10} {'Mean Value':<12}")
        print("-" * 50)
        
        for nutrient, metrics in data['metrics'].items():
            print(f"{nutrient.capitalize():<12} "
                  f"{metrics['mae']:<10.2f} "
                  f"{metrics['r2']:<10.3f} "
                  f"{metrics['mean_value']:<12.2f}")
    else:
        print(f"❌ Error: {data.get('error', 'Unknown error')}")

def test_various_cuisines():
    """Test nutrition prediction for various cuisines"""
    print("🧪 TEST 5: Nutrition Across Different Cuisines")
    print_separator()
    
    # Test recipes from different cuisines
    recipe_ids = [1, 6, 11, 26, 46, 66, 86, 106]  # Sample from different cuisines
    
    response = requests.post(f'{BASE_URL}/api/nutrition/compare',
                            json={'recipe_ids': recipe_ids})
    data = response.json()
    
    if data['success']:
        print(f"✅ Analyzed {data['total']} recipes from different cuisines:\n")
        
        # Group by cuisine
        cuisines = {}
        for recipe in data['recipes']:
            cuisine = recipe['cuisine']
            if cuisine not in cuisines:
                cuisines[cuisine] = []
            cuisines[cuisine].append(recipe)
        
        for cuisine, recipes in cuisines.items():
            print(f"🌍 {cuisine}:")
            for recipe in recipes:
                n = recipe['nutrition']
                print(f"   • {recipe['recipe_name']}: "
                      f"{n['calories']} cal, "
                      f"{n['protein']}g protein, "
                      f"{n['carbs']}g carbs")
            print()
    else:
        print(f"❌ Error: {data.get('error', 'Unknown error')}")

def main():
    print("\n" + "="*80)
    print("🍎 NUTRITION PREDICTOR - FEATURE #5 TEST SUITE")
    print("="*80)
    
    try:
        # Check if API is running
        response = requests.get(f'{BASE_URL}/api/health', timeout=2)
        if response.status_code == 200:
            print("\n✅ Backend API is running!\n")
        else:
            print("\n❌ Backend API returned unexpected status\n")
            return
    except requests.exceptions.RequestException:
        print("\n❌ ERROR: Backend API is not running!")
        print("Please start the backend server first:")
        print("  cd backend")
        print("  python app.py\n")
        return
    
    # Run tests
    test_predict_custom_ingredients()
    test_recipe_nutrition()
    test_compare_recipes()
    test_model_metrics()
    test_various_cuisines()
    
    print_separator()
    print("🎉 All tests completed!")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
