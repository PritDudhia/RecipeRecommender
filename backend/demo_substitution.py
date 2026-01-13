"""Demo: Show impressive ingredient substitution across world cuisines"""

import requests
import json

API_URL = "http://localhost:5000"

print("🌍 GLOBAL INGREDIENT SUBSTITUTION DEMO")
print("=" * 70)
print()

# Test interesting ingredients from different cuisines
test_ingredients = [
    "soy sauce",
    "chicken", 
    "coconut milk",
    "ginger",
    "cheese"
]

for ingredient in test_ingredients:
    print(f"🔍 Finding substitutes for: {ingredient.upper()}")
    print("-" * 70)
    
    try:
        response = requests.post(
            f"{API_URL}/api/substitute",
            json={"ingredient": ingredient}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('substitutes'):
                for sub in data['substitutes'][:5]:  # Top 5
                    confidence = sub['confidence'] * 100
                    support = sub['support'] * 100
                    context_sim = sub['context_similarity'] * 100
                    
                    print(f"  ✨ {sub['substitute']}")
                    print(f"     📊 Confidence: {confidence:.1f}% | Support: {support:.1f}% | Context: {context_sim:.1f}%")
                    
                    # Show which recipes use both
                    recipes_using_both = []
                    for r in sub.get('example_recipes', [])[:2]:
                        recipes_using_both.append(f"{r['name']} ({r['cuisine']})")
                    
                    if recipes_using_both:
                        print(f"     📖 Used together in: {', '.join(recipes_using_both)}")
            else:
                print(f"  ℹ️  No substitutes found")
        else:
            print(f"  ❌ Error: {response.status_code}")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print()

print("=" * 70)
print("🎯 This shows how ingredients from different cuisines can substitute!")
print("💡 The system learns from 120 recipes across 32 world cuisines!")
print("=" * 70)
