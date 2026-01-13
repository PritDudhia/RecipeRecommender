"""Quick script to show the comprehensive world dataset coverage"""

from models.world_recipes_data import get_world_recipes, get_ingredient_categories

recipes = get_world_recipes()
categories = get_ingredient_categories()

print('=' * 60)
print('🌍 COMPREHENSIVE WORLD RECIPE DATASET')
print('=' * 60)
print(f'\n📊 Total Recipes: {len(recipes)}')
print(f'🥘 Total Unique Ingredients: {len(categories)}')

# Count by cuisine
cuisines = {}
for r in recipes:
    c = r.get('cuisine', 'Unknown')
    cuisines[c] = cuisines.get(c, 0) + 1

print('\n🌎 GLOBAL CUISINE COVERAGE:')
print('-' * 60)
for cuisine, count in sorted(cuisines.items()):
    print(f'   {cuisine:25} {count:3} recipes')

print('\n' + '=' * 60)
print('Sample recipes from each continent:')
print('=' * 60)

shown = set()
for r in recipes[:30]:  # Show first 30 diverse recipes
    cuisine = r.get('cuisine', 'Unknown')
    if cuisine not in shown:
        print(f"\n{cuisine}: {r['name']}")
        print(f"   Ingredients: {', '.join(r['ingredients'][:5])}...")
        shown.add(cuisine)

print('\n' + '=' * 60)
print('🎯 READY FOR CO-OP INTERVIEW! 🎯')
print('=' * 60)
print('This dataset covers recipes from:')
print('  ✅ Asia (Chinese, Thai, Japanese, Korean, Indian, Vietnamese)')
print('  ✅ Europe (Italian, French, Spanish, Greek, German, British)')
print('  ✅ Americas (Mexican, American, Cajun)')
print('  ✅ Middle East (Lebanese, Turkish, Persian)')
print('  ✅ Africa (Moroccan, Ethiopian)')
print('  ✅ Fusion cuisines')
print('=' * 60)
