"""
Test script for Ingredient Substitution API
Run this to test the substitution feature
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test if API is running"""
    print("=" * 60)
    print("Testing API Health...")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✅ API is running!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ API returned status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the backend server is running!")
    print()

def test_get_ingredients():
    """Test getting all available ingredients"""
    print("=" * 60)
    print("Testing: Get All Ingredients")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/substitute/ingredients")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total']} ingredients:")
            print(f"   {', '.join(data['ingredients'][:10])}...")
        else:
            print(f"❌ Error: Status code {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

def test_find_substitutes(ingredient):
    """Test finding substitutes for an ingredient"""
    print("=" * 60)
    print(f"Testing: Find Substitutes for '{ingredient}'")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/substitute",
            json={"ingredient": ingredient, "top_n": 5}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📦 Ingredient: {data['ingredient']}")
            
            if data.get('ingredient_info'):
                info = data['ingredient_info']
                print(f"   Category: {info['category']}")
                print(f"   Appears in: {info['appears_in']}/{info['total_recipes']} recipes")
                print(f"   Frequency: {info['frequency']*100:.1f}%")
            
            print(f"\n🔄 Substitutes ({data['total_found']} found):")
            
            if data['substitutes']:
                for i, sub in enumerate(data['substitutes'], 1):
                    print(f"\n   {i}. {sub['substitute']}")
                    print(f"      Confidence: {sub['confidence']*100:.1f}%")
                    print(f"      Support: {sub['support']*100:.1f}%")
                    print(f"      Category: {sub['category']}")
            else:
                print("   No substitutes found")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    print()

if __name__ == "__main__":
    print("\n🧪 INGREDIENT SUBSTITUTION API TEST SUITE\n")
    
    # Test 1: Health check
    test_health()
    
    # Test 2: Get all ingredients
    test_get_ingredients()
    
    # Test 3: Find substitutes for common ingredients
    test_ingredients = [
        'chicken',
        'milk',
        'eggs',
        'cheese',
        'pasta',
        'beef',
        'tofu'
    ]
    
    for ingredient in test_ingredients:
        test_find_substitutes(ingredient)
    
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
