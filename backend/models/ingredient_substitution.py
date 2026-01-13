"""
Feature #3: Ingredient Substitution Finder
Uses Association Rules (Apriori-like) to find ingredient substitutions
Based on co-occurrence patterns in recipes
Dataset: 120+ recipes from 15+ world cuisines with 200+ ingredients
"""

import numpy as np
from collections import defaultdict
import json
from .world_recipes_data import get_world_recipes, get_ingredient_categories


class IngredientSubstitutionFinder:
    """
    Finds ingredient substitutions using association rule mining
    Based on ingredient co-occurrence in recipes
    """
    
    def __init__(self, min_support=0.02, min_confidence=0.15):
        """
        Initialize the substitution finder
        
        Args:
            min_support: Minimum support threshold for frequent itemsets (lowered to 0.02 for maximum coverage)
            min_confidence: Minimum confidence for substitution rules (lowered to 0.15 for maximum coverage)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.recipes = []
        self.ingredient_index = {}  # ingredient -> index mapping
        self.substitution_rules = {}  # ingredient -> list of (substitute, confidence, support)
        self.ingredient_categories = {}  # ingredient -> category mapping
        
    def create_sample_recipe_data(self):
        """
        Load comprehensive world recipe dataset with 120+ recipes
        Covers 15+ cuisines from around the world with 260+ ingredients
        """
        # Load the comprehensive world recipes dataset
        self.recipes = get_world_recipes()
        
        # Load ingredient categories for intelligent substitutions
        self.ingredient_categories = get_ingredient_categories()
        
    def calculate_ingredient_cooccurrence(self):
        """
        Calculate co-occurrence matrix for ingredients
        Shows how often ingredients appear together
        """
        # Build ingredient index
        all_ingredients = set()
        for recipe in self.recipes:
            all_ingredients.update(recipe['ingredients'])
        
        self.ingredient_index = {ing: idx for idx, ing in enumerate(sorted(all_ingredients))}
        n_ingredients = len(self.ingredient_index)
        
        # Co-occurrence matrix
        cooccurrence = np.zeros((n_ingredients, n_ingredients))
        ingredient_counts = np.zeros(n_ingredients)
        
        # Count co-occurrences
        for recipe in self.recipes:
            ingredients = recipe['ingredients']
            for ing in ingredients:
                idx = self.ingredient_index[ing]
                ingredient_counts[idx] += 1
                
                for other_ing in ingredients:
                    if ing != other_ing:
                        other_idx = self.ingredient_index[other_ing]
                        cooccurrence[idx][other_idx] += 1
        
        return cooccurrence, ingredient_counts
    
    def find_substitution_pairs(self):
        """
        Find ingredient substitution pairs using association rules
        Based on "recipes that use X often also use Y in similar contexts"
        """
        cooccurrence, ingredient_counts = self.calculate_ingredient_cooccurrence()
        n_recipes = len(self.recipes)
        reverse_index = {idx: ing for ing, idx in self.ingredient_index.items()}
        
        self.substitution_rules = defaultdict(list)
        
        # For each ingredient pair, calculate substitution confidence
        for ing1, idx1 in self.ingredient_index.items():
            for ing2, idx2 in self.ingredient_index.items():
                if ing1 == ing2:
                    continue
                
                # Check if they're in the same category
                cat1 = self.ingredient_categories.get(ing1, 'other')
                cat2 = self.ingredient_categories.get(ing2, 'other')
                
                # Only consider substitutions within similar categories
                if not self._is_substitutable_category(cat1, cat2):
                    continue
                
                # Calculate support: how often they appear in similar contexts
                # (both appear in recipes, but not necessarily together)
                support1 = ingredient_counts[idx1] / n_recipes
                support2 = ingredient_counts[idx2] / n_recipes
                
                if support1 < self.min_support or support2 < self.min_support:
                    continue
                
                # Calculate confidence: probability of substitution
                # Based on how often they appear in similar recipe contexts
                shared_context_score = self._calculate_context_similarity(
                    ing1, ing2, cooccurrence, idx1, idx2
                )
                
                if shared_context_score >= self.min_confidence:
                    self.substitution_rules[ing1].append({
                        'substitute': ing2,
                        'confidence': round(shared_context_score, 3),
                        'support': round(min(support1, support2), 3),
                        'category': cat2
                    })
        
        # Sort substitutes by confidence
        for ing in self.substitution_rules:
            self.substitution_rules[ing].sort(key=lambda x: x['confidence'], reverse=True)
    
    def _is_substitutable_category(self, cat1, cat2):
        """Check if two categories are substitutable - RELAXED for more results"""
        # Same category
        if cat1 == cat2:
            return True
        
        # Protein substitutions (broader)
        protein_cats = {'protein_meat', 'protein_seafood', 'protein_plant', 'protein_egg', 'protein_egg_substitute'}
        if cat1 in protein_cats and cat2 in protein_cats:
            return True
        
        # Dairy/liquid substitutions (very broad - milk, cream, coconut milk, etc.)
        dairy_cats = {'dairy', 'dairy_substitute', 'oil', 'fat', 'liquid', 'cream', 'milk', 'coconut_milk'}
        if cat1 in dairy_cats and cat2 in dairy_cats:
            return True
        
        # Sauce substitutions
        if 'sauce' in cat1 and 'sauce' in cat2:
            return True
        
        # Grain substitutions
        grain_cats = {'grain_pasta', 'grain_rice', 'grain_noodles', 'grain_flour', 'grain_dough', 'grain'}
        if cat1 in grain_cats and cat2 in grain_cats:
            return True
        
        # Aromatics can substitute
        aromatic_cats = {'aromatics', 'herbs', 'spice'}
        if cat1 in aromatic_cats and cat2 in aromatic_cats:
            return True
        
        # Vegetables
        if 'vegetable' in cat1 and 'vegetable' in cat2:
            return True
        
        # Allow if either is uncategorized (more permissive)
        if cat1 == 'other' or cat2 == 'other':
            return True
        
        return False
    
    def _calculate_context_similarity(self, ing1, ing2, cooccurrence, idx1, idx2):
        """
        Calculate how similar the contexts are for two ingredients
        Based on their co-occurrence patterns with other ingredients
        """
        # Get co-occurrence vectors
        vec1 = cooccurrence[idx1]
        vec2 = cooccurrence[idx2]
        
        # Calculate cosine similarity of contexts
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return similarity
    
    def train(self):
        """Train the substitution finder"""
        print("Training Ingredient Substitution Finder...")
        
        # Create sample data
        self.create_sample_recipe_data()
        
        # Find substitution rules
        self.find_substitution_pairs()
        
        print(f"✅ Found substitution rules for {len(self.substitution_rules)} ingredients")
        print(f"✅ Total recipes analyzed: {len(self.recipes)}")
        
        return self
    
    def get_substitutes(self, ingredient, top_n=5):
        """
        Get substitute ingredients for a given ingredient
        
        Args:
            ingredient: Ingredient name (lowercase)
            top_n: Number of substitutes to return
        
        Returns:
            List of substitute dictionaries with confidence scores
        """
        ingredient = ingredient.lower().strip()
        
        if ingredient not in self.substitution_rules:
            # Try to find partial matches
            possible_matches = [
                ing for ing in self.substitution_rules.keys()
                if ingredient in ing or ing in ingredient
            ]
            
            if not possible_matches:
                return []
            
            # Use the closest match
            ingredient = possible_matches[0]
        
        substitutes = self.substitution_rules[ingredient][:top_n]
        return substitutes
    
    def get_all_ingredients(self):
        """Get list of all known ingredients"""
        return sorted(list(self.ingredient_index.keys()))
    
    def get_ingredient_info(self, ingredient):
        """Get information about an ingredient"""
        ingredient = ingredient.lower().strip()
        
        if ingredient not in self.ingredient_index:
            return None
        
        # Count recipes containing this ingredient
        recipe_count = sum(
            1 for recipe in self.recipes
            if ingredient in recipe['ingredients']
        )
        
        return {
            'ingredient': ingredient,
            'category': self.ingredient_categories.get(ingredient, 'other'),
            'appears_in': recipe_count,
            'total_recipes': len(self.recipes),
            'frequency': round(recipe_count / len(self.recipes), 3)
        }


# Global instance
_substitution_finder = None

def get_trained_substitution_finder():
    """Get or create trained substitution finder instance"""
    global _substitution_finder
    
    if _substitution_finder is None:
        _substitution_finder = IngredientSubstitutionFinder(
            min_support=0.1,  # Ingredient must appear in at least 10% of recipes
            min_confidence=0.3  # 30% context similarity for substitution
        )
        _substitution_finder.train()
    
    return _substitution_finder


if __name__ == '__main__':
    # Test the substitution finder
    print("="*60)
    print("INGREDIENT SUBSTITUTION FINDER - TEST")
    print("="*60)
    
    finder = get_trained_substitution_finder()
    
    # Test substitutions
    test_ingredients = ['chicken', 'milk', 'eggs', 'pasta', 'cheese']
    
    for ingredient in test_ingredients:
        print(f"\n🔍 Substitutes for '{ingredient}':")
        subs = finder.get_substitutes(ingredient, top_n=5)
        
        if subs:
            for i, sub in enumerate(subs, 1):
                print(f"  {i}. {sub['substitute']} "
                      f"(confidence: {sub['confidence']}, "
                      f"category: {sub['category']})")
        else:
            print("  No substitutes found")
    
    # Test ingredient info
    print("\n" + "="*60)
    print("INGREDIENT INFORMATION")
    print("="*60)
    
    info = finder.get_ingredient_info('chicken')
    if info:
        print(f"\nIngredient: {info['ingredient']}")
        print(f"Category: {info['category']}")
        print(f"Appears in: {info['appears_in']}/{info['total_recipes']} recipes")
        print(f"Frequency: {info['frequency']}")
    
    print("\n✅ All tests completed!")
