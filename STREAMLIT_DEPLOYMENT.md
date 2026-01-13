# 🚀 Streamlit Deployment Guide

## Quick Deploy to Streamlit Cloud (FREE)

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Step-by-Step Deployment

#### 1. Prepare Your Repository

Make sure your repo has these files:
```
RecipeRecommender/
├── streamlit_app.py          # Main Streamlit app
├── requirements.txt           # Dependencies
└── backend/
    └── models/                # All your ML models
        ├── __init__.py
        ├── recipe_recommender.py
        ├── ingredient_clustering.py
        ├── ingredient_substitution.py
        ├── cuisine_classifier.py
        └── nutrition_predictor.py
```

#### 2. Push to GitHub

```bash
git add .
git commit -m "Add Streamlit app for deployment"
git push origin main
```

#### 3. Deploy on Streamlit Cloud

1. **Go to**: https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the details**:
   - Repository: `your-username/RecipeRecommender`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Click "Deploy!"**

6. **Wait 2-3 minutes** for deployment

7. **Get your URL**: `https://your-app-name.streamlit.app`

#### 4. Share with Interviewers

Your app will be live at:
```
https://[your-app-name].streamlit.app
```

✅ **App stays active** - no sleep time!  
✅ **Free forever** for public repos  
✅ **Auto-deploys** when you push to GitHub  

---

## Local Testing Before Deployment

Test your app locally first:

```bash
# Activate your virtual environment
.\.venv\Scripts\Activate.ps1

# Install Streamlit
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` to test.

---

## Interview Tips

### During the Interview:

1. **Share the live link** before the interview starts
2. **Have it open** in your browser
3. **Walk through each feature**:
   - Start with Collaborative Filtering
   - Show Content-Based recommendations
   - Demonstrate Clustering
   - Predict cuisines
   - Show nutrition predictions

### What to Say:

> "I built a comprehensive ML recipe recommender with 5 different algorithms. 
> It's deployed on Streamlit Cloud and you can access it at [your-link]. 
> Let me walk you through the features..."

### Demo Flow (5 minutes):

1. **Home page** (30 sec) - Show 5 ML features
2. **Collaborative Filtering** (1 min) - Show personalized recommendations
3. **Content-Based** (1 min) - Search by ingredients
4. **Clustering** (1 min) - Show ingredient groups
5. **Cuisine Classification** (1 min) - Predict cuisine
6. **Nutrition** (30 sec) - Show nutritional analysis

---

## Troubleshooting

### If deployment fails:

**Check requirements.txt**:
- Make sure all packages are listed
- Use compatible versions

**Check file paths**:
- All imports should use relative paths
- `from backend.models.xxx import yyy`

**Check logs**:
- Click "Manage app" on Streamlit Cloud
- View logs to see errors

### Common Issues:

**Issue**: Module not found  
**Fix**: Add to `requirements.txt`

**Issue**: Import errors  
**Fix**: Make sure `backend/models/__init__.py` exists

**Issue**: App crashes on startup  
**Fix**: Check model training code - reduce data size if needed

---

## Making Updates

After deployment, to update your app:

```bash
# Make changes to streamlit_app.py
git add .
git commit -m "Update feature X"
git push origin main
```

Streamlit Cloud will **auto-deploy** in 1-2 minutes!

---

## Alternative: Run Locally and Share via ngrok

If you need to demo quickly without GitHub:

```bash
# Install ngrok
# Download from: https://ngrok.com/download

# Run Streamlit
streamlit run streamlit_app.py

# In another terminal, expose it
ngrok http 8501
```

Share the `https://xxxx.ngrok.io` URL for live demo.

**Note**: Free ngrok URLs expire after 2 hours.

---

## For Your Resume

Add this line:
```
• Deployed full-stack ML recipe recommender on Streamlit Cloud
• Live demo: https://[your-app].streamlit.app
```

---

## Post-Interview

Keep the app running! Interviewers often:
- Share the link with their team
- Revisit it later
- Compare candidates

Free Streamlit hosting = permanent portfolio piece! 🎉
