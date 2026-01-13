"""
Recipe Recommender - Streamlit App
Multi-Feature ML System for Recipe Recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from models.recipe_recommender import RecipeRecommender
from models.ingredient_clustering import get_trained_model
from models.ingredient_substitution import IngredientSubstitutionFinder
from models.cuisine_classifier import CuisineClassifier
from models.nutrition_predictor import NutritionPredictor

# Page config
st.set_page_config(
    page_title="Recipe Recommender",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize models with caching
@st.cache_resource
def load_models():
    """Load all ML models"""
    with st.spinner("🤖 Loading ML models..."):
        models = {
            'recommender': RecipeRecommender(),
            'clusterer': get_trained_model(),
            'substitution': IngredientSubstitutionFinder(min_support=0.02, min_confidence=0.15),
            'cuisine': CuisineClassifier(n_neighbors=5),
            'nutrition': NutritionPredictor(use_ridge=True, alpha=1.0)
        }
        
        # Train models
        models['recommender'].train()
        models['substitution'].train()
        models['cuisine'].train()
        models['nutrition'].train()
        
        return models

# Load models
models = load_models()

# Header
st.markdown('<p class="main-header">🍳 Recipe Recommender</p>', unsafe_allow_html=True)
st.markdown("**5 ML Features** | Collaborative Filtering • Content-Based • Clustering • Classification • Regression")

# Sidebar Navigation
st.sidebar.title("🎯 Features")
feature = st.sidebar.radio(
    "Choose a feature:",
    [
        "🏠 Home",
        "🤝 Collaborative Filtering",
        "📝 Content-Based Filtering",
        "🧩 Ingredient Clustering",
        "🔄 Ingredient Substitution",
        "🌍 Cuisine Classification",
        "🥗 Nutrition Prediction"
    ]
)

# ===== HOME PAGE =====
if feature == "🏠 Home":
    st.header("Welcome to Recipe Recommender!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h2>5</h2><p>ML Features</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h2>15+</h2><p>Recipes</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h2>100+</h2><p>Ingredients</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Features Overview
    
    #### 1. 🤝 Collaborative Filtering
    - Get personalized recipe recommendations based on user preferences
    - Uses user-item rating matrix and cosine similarity
    - **Algorithm**: Matrix Factorization with Cosine Similarity
    
    #### 2. 📝 Content-Based Filtering
    - Find similar recipes based on ingredients and features
    - Recommends recipes with your available ingredients
    - **Algorithm**: TF-IDF Vectorization + Similarity Matching
    
    #### 3. 🧩 Ingredient Clustering
    - Discover ingredient groups using unsupervised learning
    - Find similar ingredients for meal planning
    - **Algorithm**: K-Means Clustering
    
    #### 4. 🔄 Ingredient Substitution
    - Find smart ingredient substitutes
    - Based on ingredient co-occurrence patterns
    - **Algorithm**: Apriori Association Rules
    
    #### 5. 🌍 Cuisine Classification
    - Predict cuisine type from ingredients
    - Explore recipes from different cultures
    - **Algorithm**: k-Nearest Neighbors (k-NN)
    
    #### 6. 🥗 Nutrition Prediction
    - Estimate nutritional values from ingredients
    - Compare recipes by healthiness
    - **Algorithm**: Ridge Regression
    """)

# ===== COLLABORATIVE FILTERING =====
elif feature == "🤝 Collaborative Filtering":
    st.header("🤝 Collaborative Filtering")
    st.markdown("Get personalized recipe recommendations based on user preferences")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Settings")
        user_id = st.number_input("Select User ID", min_value=0, max_value=9, value=0, step=1)
        top_n = st.slider("Number of recommendations", 1, 10, 5)
        
        if st.button("Get Recommendations", type="primary"):
            st.session_state.cf_recs = models['recommender'].get_user_based_recommendations(user_id, top_n)
    
    with col2:
        if 'cf_recs' in st.session_state:
            st.subheader(f"Top {top_n} Recommendations for User {user_id}")
            
            for idx, rec in enumerate(st.session_state.cf_recs, 1):
                with st.expander(f"#{idx} - {rec['name']} ({rec['cuisine']}) - Score: {rec['predicted_rating']:.2f}"):
                    st.write(f"**Ingredients**: {', '.join(rec['ingredients'])}")
                    
                    # Features
                    col_a, col_b, col_c = st.columns(3)
                    features = rec['features']
                    col_a.metric("Prep Time", f"{features[0]} min")
                    col_b.metric("Difficulty", f"{features[1]}/5")
                    col_c.metric("Spice Level", f"{features[2]}/5")
        else:
            st.info("👆 Select a user and click 'Get Recommendations'")

# ===== CONTENT-BASED FILTERING =====
elif feature == "📝 Content-Based Filtering":
    st.header("📝 Content-Based Filtering")
    
    tab1, tab2 = st.tabs(["Find Similar Recipes", "Search by Ingredients"])
    
    with tab1:
        st.subheader("Find recipes similar to one you like")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            recipes = models['recommender'].get_all_recipes()
            recipe_names = {f"{r['name']} ({r['cuisine']})": r['id'] for r in recipes}
            selected_recipe = st.selectbox("Select a recipe", list(recipe_names.keys()))
            top_n = st.slider("Number of similar recipes", 1, 10, 5, key="cb_slider")
            
            if st.button("Find Similar", type="primary"):
                recipe_id = recipe_names[selected_recipe]
                st.session_state.cb_recs = models['recommender'].get_content_based_recommendations(recipe_id, top_n)
                st.session_state.base_recipe = models['recommender'].get_recipe_by_id(recipe_id)
        
        with col2:
            if 'cb_recs' in st.session_state:
                st.success(f"**Base Recipe**: {st.session_state.base_recipe['name']}")
                st.write(f"Ingredients: {', '.join(st.session_state.base_recipe['ingredients'])}")
                st.markdown("---")
                
                for idx, rec in enumerate(st.session_state.cb_recs, 1):
                    with st.expander(f"#{idx} - {rec['name']} - Similarity: {rec['similarity_score']:.3f}"):
                        st.write(f"**Cuisine**: {rec['cuisine']}")
                        st.write(f"**Ingredients**: {', '.join(rec['ingredients'])}")
            else:
                st.info("👆 Select a recipe to find similar ones")
    
    with tab2:
        st.subheader("What's in your kitchen?")
        
        ingredients_input = st.text_area(
            "Enter ingredients (comma-separated)",
            placeholder="chicken, tomatoes, garlic, rice",
            height=100
        )
        
        if st.button("Find Recipes", type="primary", key="ingr_search"):
            if ingredients_input:
                ingredients = [ing.strip() for ing in ingredients_input.split(',')]
                all_recipes = models['recommender'].get_all_recipes()
                
                # Score recipes
                scored = []
                for recipe in all_recipes:
                    recipe_ings = set(ing.lower() for ing in recipe['ingredients'])
                    input_ings = set(ing.lower() for ing in ingredients)
                    overlap = len(recipe_ings.intersection(input_ings))
                    
                    if overlap > 0:
                        score = overlap / len(recipe_ings)
                        scored.append({
                            **recipe,
                            'overlap_score': score,
                            'matched': list(recipe_ings.intersection(input_ings))
                        })
                
                scored.sort(key=lambda x: x['overlap_score'], reverse=True)
                
                if scored:
                    st.success(f"Found {len(scored)} matching recipes!")
                    
                    for idx, rec in enumerate(scored[:10], 1):
                        with st.expander(f"#{idx} - {rec['name']} - Match: {rec['overlap_score']*100:.0f}%"):
                            st.write(f"**Cuisine**: {rec['cuisine']}")
                            st.write(f"**Matched ingredients**: {', '.join(rec['matched'])}")
                            st.write(f"**All ingredients**: {', '.join(rec['ingredients'])}")
                else:
                    st.warning("No recipes found with these ingredients")
            else:
                st.warning("Please enter some ingredients")

# ===== INGREDIENT CLUSTERING =====
elif feature == "🧩 Ingredient Clustering":
    st.header("🧩 Ingredient Clustering")
    st.markdown("Discover ingredient groups using K-Means clustering")
    
    tab1, tab2 = st.tabs(["View Clusters", "Predict Cluster"])
    
    with tab1:
        clusters = models['clusterer'].get_clusters()
        cluster_names = models['clusterer'].get_cluster_names()
        
        st.subheader(f"Found {len(clusters)} Ingredient Clusters")
        
        for cluster_id in sorted(clusters.keys()):
            with st.expander(f"🏷️ {cluster_names.get(cluster_id, f'Cluster {cluster_id}')} ({len(clusters[cluster_id])} ingredients)"):
                st.write(", ".join(sorted(clusters[cluster_id])))
    
    with tab2:
        st.subheader("Predict which cluster a new ingredient belongs to")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ingredient_name = st.text_input("Ingredient Name", placeholder="e.g., Quinoa")
            
            st.markdown("**Nutritional Features (per 100g):**")
            protein = st.number_input("Protein (g)", 0.0, 100.0, 10.0, 0.1)
            carbs = st.number_input("Carbohydrates (g)", 0.0, 100.0, 20.0, 0.1)
            fat = st.number_input("Fat (g)", 0.0, 100.0, 5.0, 0.1)
            calories = st.number_input("Calories (kcal)", 0, 1000, 200, 1)
            fiber = st.number_input("Fiber (g)", 0.0, 50.0, 3.0, 0.1)
            
            if st.button("Predict Cluster", type="primary"):
                features = [protein, carbs, fat, calories, fiber]
                cluster_id = models['clusterer'].predict(features)
                
                st.session_state.pred_cluster = cluster_id
                st.session_state.pred_name = ingredient_name
        
        with col2:
            if 'pred_cluster' in st.session_state:
                cluster_id = st.session_state.pred_cluster
                cluster_name = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
                
                st.success(f"**{st.session_state.pred_name}** belongs to:")
                st.info(f"### {cluster_name}")
                
                st.markdown("**Similar ingredients in this cluster:**")
                similar = clusters[cluster_id][:10]
                st.write(", ".join(similar))

# ===== INGREDIENT SUBSTITUTION =====
elif feature == "🔄 Ingredient Substitution":
    st.header("🔄 Ingredient Substitution")
    st.markdown("Find smart ingredient substitutes using association rules")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        available_ingredients = sorted(models['substitution'].substitution_rules.keys())
        
        ingredient = st.selectbox(
            "Select ingredient to substitute",
            available_ingredients
        )
        
        top_n = st.slider("Number of alternatives", 1, 10, 5, key="sub_slider")
        
        if st.button("Find Substitutes", type="primary"):
            st.session_state.substitutes = models['substitution'].get_substitutes(ingredient, top_n)
            st.session_state.sub_ingredient = ingredient
    
    with col2:
        if 'substitutes' in st.session_state:
            st.subheader(f"Substitutes for '{st.session_state.sub_ingredient}'")
            
            if st.session_state.substitutes:
                for idx, sub in enumerate(st.session_state.substitutes, 1):
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    with col_a:
                        st.markdown(f"**#{idx} {sub['substitute']}**")
                    with col_b:
                        st.metric("Confidence", f"{sub['confidence']:.0%}")
                    with col_c:
                        st.metric("Support", f"{sub['support']:.1%}")
            else:
                st.warning("No substitutes found for this ingredient")
        else:
            st.info("👆 Select an ingredient to find substitutes")

# ===== CUISINE CLASSIFICATION =====
elif feature == "🌍 Cuisine Classification":
    st.header("🌍 Cuisine Classification")
    st.markdown("Predict cuisine type from ingredients using k-NN")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Enter Ingredients")
        
        ingredients_input = st.text_area(
            "Ingredients (comma-separated)",
            placeholder="tomatoes, basil, mozzarella, olive oil",
            height=150
        )
        
        if st.button("Predict Cuisine", type="primary"):
            if ingredients_input:
                ingredients = [ing.strip() for ing in ingredients_input.split(',')]
                result = models['cuisine'].predict_cuisine(ingredients)
                st.session_state.cuisine_result = result
            else:
                st.warning("Please enter some ingredients")
    
    with col2:
        if 'cuisine_result' in st.session_state:
            result = st.session_state.cuisine_result
            
            if result['success']:
                st.success(f"### Predicted Cuisine: {result['predicted_cuisine']}")
                st.metric("Confidence", f"{result['confidence']:.1%}")
                
                st.markdown("**Top Predictions:**")
                df = pd.DataFrame(result['all_predictions'])
                st.bar_chart(df.set_index('cuisine')['probability'])
                
                st.markdown("**Similar Recipes:**")
                for recipe in result['similar_recipes'][:3]:
                    with st.expander(recipe['name']):
                        st.write(f"**Cuisine**: {recipe['cuisine']}")
                        st.write(f"**Ingredients**: {', '.join(recipe['ingredients'])}")
            else:
                st.error(result.get('error', 'Prediction failed'))
        else:
            st.info("👆 Enter ingredients to predict cuisine type")
    
    # Stats
    st.markdown("---")
    stats = models['cuisine'].get_cuisine_stats()
    
    st.subheader("📊 Cuisine Statistics")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Cuisines", stats['total_cuisines'])
    col_b.metric("Total Recipes", stats['total_recipes'])
    col_c.metric("Total Ingredients", stats['total_ingredients'])
    
    # Distribution
    st.markdown("**Recipe Distribution by Cuisine:**")
    df_stats = pd.DataFrame(stats['cuisine_distribution'])
    if not df_stats.empty:
        st.bar_chart(df_stats.set_index('cuisine')['count'])

# ===== NUTRITION PREDICTION =====
elif feature == "🥗 Nutrition Prediction":
    st.header("🥗 Nutrition Prediction")
    st.markdown("Estimate nutritional values using Ridge Regression")
    
    tab1, tab2, tab3 = st.tabs(["Predict from Ingredients", "Recipe Nutrition", "Compare Recipes"])
    
    with tab1:
        st.subheader("Predict nutrition from ingredients")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            ingredients_input = st.text_area(
                "Ingredients (comma-separated)",
                placeholder="chicken, rice, broccoli, olive oil",
                height=150,
                key="nutr_ingr_input"
            )
            
            if st.button("Predict Nutrition", type="primary"):
                if ingredients_input:
                    ingredients = [ing.strip() for ing in ingredients_input.split(',')]
                    predictions = models['nutrition'].predict(ingredients)
                    st.session_state.nutr_pred = predictions
                    st.session_state.nutr_ingr = ingredients
                else:
                    st.warning("Please enter ingredients")
        
        with col2:
            if 'nutr_pred' in st.session_state:
                st.success(f"Nutritional estimates for: {', '.join(st.session_state.nutr_ingr)}")
                
                pred = st.session_state.nutr_pred
                
                col_a, col_b, col_c, col_d = st.columns(4)
                col_a.metric("Calories", f"{pred['calories']:.0f} kcal")
                col_b.metric("Protein", f"{pred['protein']:.1f} g")
                col_c.metric("Carbs", f"{pred['carbs']:.1f} g")
                col_d.metric("Fat", f"{pred['fat']:.1f} g")
                
                # Macro breakdown
                st.markdown("**Macronutrient Breakdown:**")
                total = pred['protein'] + pred['carbs'] + pred['fat']
                if total > 0:
                    macro_data = {
                        'Protein': (pred['protein'] / total) * 100,
                        'Carbs': (pred['carbs'] / total) * 100,
                        'Fat': (pred['fat'] / total) * 100
                    }
                    st.bar_chart(macro_data)
            else:
                st.info("👆 Enter ingredients to predict nutrition")
    
    with tab2:
        st.subheader("Get nutrition for a recipe")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            recipes = models['recommender'].get_all_recipes()
            recipe_options = {f"{r['name']} ({r['cuisine']})": r['id'] for r in recipes}
            selected = st.selectbox("Select recipe", list(recipe_options.keys()), key="recipe_nutr")
            
            if st.button("Get Nutrition", type="primary", key="get_recipe_nutr"):
                recipe_id = recipe_options[selected]
                try:
                    result = models['nutrition'].predict_recipe(recipe_id=recipe_id)
                    st.session_state.recipe_nutr = result
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if 'recipe_nutr' in st.session_state:
                result = st.session_state.recipe_nutr
                
                if isinstance(result, dict) and 'recipe_name' in result:
                    st.success(f"**{result['recipe_name']}**")
                    st.write(f"*{result['cuisine']} cuisine*")
                    
                    nutr = result['nutrition']
                    col_a, col_b, col_c, col_d = st.columns(4)
                    col_a.metric("Calories", f"{nutr['calories']:.0f}")
                    col_b.metric("Protein", f"{nutr['protein']:.1f}g")
                    col_c.metric("Carbs", f"{nutr['carbs']:.1f}g")
                    col_d.metric("Fat", f"{nutr['fat']:.1f}g")
                    
                    st.markdown(f"**Ingredients**: {', '.join(result['ingredients'])}")
                else:
                    st.error("Invalid result format")
            else:
                st.info("👆 Select a recipe")
    
    with tab3:
        st.subheader("Compare nutrition across recipes")
        
        recipes = models['recommender'].get_all_recipes()
        recipe_options = {f"{r['name']}": r['id'] for r in recipes}
        
        selected_recipes = st.multiselect(
            "Select recipes to compare (2-5)",
            list(recipe_options.keys()),
            max_selections=5
        )
        
        if st.button("Compare", type="primary", key="compare_btn"):
            if len(selected_recipes) >= 2:
                recipe_ids = [recipe_options[name] for name in selected_recipes]
                results = models['nutrition'].compare_recipes(recipe_ids)
                st.session_state.compare_results = results
            else:
                st.warning("Please select at least 2 recipes")
        
        if 'compare_results' in st.session_state:
            results = st.session_state.compare_results
            
            # Create comparison dataframe
            comparison_data = []
            for r in results:
                comparison_data.append({
                    'Recipe': r['recipe_name'],
                    'Calories': r['nutrition']['calories'],
                    'Protein (g)': r['nutrition']['protein'],
                    'Carbs (g)': r['nutrition']['carbs'],
                    'Fat (g)': r['nutrition']['fat']
                })
            
            df = pd.DataFrame(comparison_data)
            
            st.dataframe(df, use_container_width=True)
            
            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Calories Comparison**")
                st.bar_chart(df.set_index('Recipe')['Calories'])
            
            with col2:
                st.markdown("**Macronutrients Comparison**")
                st.bar_chart(df.set_index('Recipe')[['Protein (g)', 'Carbs (g)', 'Fat (g)']])

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Built with ❤️ using Streamlit | "
    "5 ML Models: Collaborative Filtering • Content-Based • K-Means • Association Rules • k-NN • Ridge Regression</p>",
    unsafe_allow_html=True
)
