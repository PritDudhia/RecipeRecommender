import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')
  const [recipes, setRecipes] = useState([])
  const [ingredients, setIngredients] = useState('')
  const [clusters, setClusters] = useState([])
  const [showClusters, setShowClusters] = useState(false)
  const [loading, setLoading] = useState(false)
  const [predictionResult, setPredictionResult] = useState(null)
  const [newIngredient, setNewIngredient] = useState({
    name: '',
    protein: '',
    carbs: '',
    fat: '',
    calories: '',
    fiber: ''
  })

  useEffect(() => {
    // Check API health
    axios.get('/api/health')
      .then(res => setApiStatus(res.data.message))
      .catch(() => setApiStatus('API not reachable'))

    // Load recipes
    axios.get('/api/recipes')
      .then(res => setRecipes(res.data))
      .catch(err => console.error('Error loading recipes:', err))
  }, [])

  const handleRecommend = () => {
    const ingredientList = ingredients.split(',').map(i => i.trim()).filter(i => i)
    axios.post('/api/recommend', { ingredients: ingredientList })
      .then(res => {
        console.log('Recommendations:', res.data)
        alert('Check console for recommendations (ML logic to be implemented)')
      })
      .catch(err => console.error('Error:', err))
  }

  const loadIngredientClusters = () => {
    setLoading(true)
    axios.get('/api/cluster/ingredients')
      .then(res => {
        setClusters(res.data.clusters)
        setShowClusters(true)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading clusters:', err)
        setLoading(false)
      })
  }

  const predictIngredientCluster = () => {
    const features = [
      parseFloat(newIngredient.protein),
      parseFloat(newIngredient.carbs),
      parseFloat(newIngredient.fat),
      parseFloat(newIngredient.calories),
      parseFloat(newIngredient.fiber)
    ]
    
    if (features.some(isNaN)) {
      alert('Please fill in all nutritional values with numbers')
      return
    }

    setLoading(true)
    axios.post('/api/cluster/predict', {
      name: newIngredient.name || 'Unknown Ingredient',
      features: features
    })
      .then(res => {
        setPredictionResult(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error predicting cluster:', err)
        alert('Error predicting cluster')
        setLoading(false)
      })
  }

  const handleIngredientChange = (field, value) => {
    setNewIngredient(prev => ({
      ...prev,
      [field]: value
    }))
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🍳 Recipe Recommender
          </h1>
          <p className="text-xl text-gray-600">
            Smart recipe suggestions with ML-powered ingredient substitutions
          </p>
          <div className="mt-4 inline-block bg-white px-4 py-2 rounded-full shadow">
            <span className="text-sm text-gray-600">API Status: </span>
            <span className="font-semibold text-green-600">{apiStatus}</span>
          </div>
        </header>

        {/* Main Content */}
        <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {/* Input Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">
              Find Recipes
            </h2>
            <p className="text-gray-600 mb-4">
              Enter ingredients you have (comma-separated):
            </p>
            <textarea
              className="w-full border-2 border-gray-300 rounded-lg p-3 mb-4 focus:outline-none focus:border-primary"
              rows="4"
              placeholder="e.g., chicken, tomatoes, pasta, garlic"
              value={ingredients}
              onChange={(e) => setIngredients(e.target.value)}
            />
            <button
              onClick={handleRecommend}
              className="w-full bg-primary hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition duration-300"
            >
              Get Recommendations
            </button>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-bold mb-3 text-gray-800">
                🔍 Ingredient Clustering (K-Means)
              </h3>
              <p className="text-sm text-gray-600 mb-3">
                Discover how ingredients are grouped by nutritional similarity
              </p>
              <button
                onClick={loadIngredientClusters}
                disabled={loading}
                className="w-full bg-secondary hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg transition duration-300 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'View Ingredient Clusters'}
              </button>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-lg font-bold mb-3 text-gray-800">🎯 Predict Ingredient Cluster</h3>
              <p className="text-sm text-gray-600 mb-3">Enter nutritional data to find which cluster it belongs to</p>
              
              <input
                type="text"
                placeholder="Ingredient name"
                value={newIngredient.name}
                onChange={(e) => handleIngredientChange('name', e.target.value)}
                className="w-full border-2 border-gray-300 rounded-lg p-2 mb-2 focus:outline-none focus:border-secondary text-sm"
              />
              
              <div className="grid grid-cols-2 gap-2 mb-2">
                <input
                  type="number"
                  placeholder="Protein (g)"
                  value={newIngredient.protein}
                  onChange={(e) => handleIngredientChange('protein', e.target.value)}
                  className="border-2 border-gray-300 rounded-lg p-2 focus:outline-none focus:border-secondary text-sm"
                />
                <input
                  type="number"
                  placeholder="Carbs (g)"
                  value={newIngredient.carbs}
                  onChange={(e) => handleIngredientChange('carbs', e.target.value)}
                  className="border-2 border-gray-300 rounded-lg p-2 focus:outline-none focus:border-secondary text-sm"
                />
                <input
                  type="number"
                  placeholder="Fat (g)"
                  value={newIngredient.fat}
                  onChange={(e) => handleIngredientChange('fat', e.target.value)}
                  className="border-2 border-gray-300 rounded-lg p-2 focus:outline-none focus:border-secondary text-sm"
                />
                <input
                  type="number"
                  placeholder="Calories"
                  value={newIngredient.calories}
                  onChange={(e) => handleIngredientChange('calories', e.target.value)}
                  className="border-2 border-gray-300 rounded-lg p-2 focus:outline-none focus:border-secondary text-sm"
                />
              </div>
              
              <input
                type="number"
                placeholder="Fiber (g)"
                value={newIngredient.fiber}
                onChange={(e) => handleIngredientChange('fiber', e.target.value)}
                className="w-full border-2 border-gray-300 rounded-lg p-2 mb-3 focus:outline-none focus:border-secondary text-sm"
              />
              
              <button
                onClick={predictIngredientCluster}
                disabled={loading}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 disabled:opacity-50"
              >
                {loading ? 'Predicting...' : 'Predict Cluster'}
              </button>

              {predictionResult && (
                <div className="mt-4 p-4 bg-purple-50 border-2 border-purple-300 rounded-lg">
                  <p className="font-bold text-purple-900 mb-2">
                    🎯 {predictionResult.ingredient}
                  </p>
                  <p className="text-sm text-purple-800">
                    <strong>Belongs to:</strong> {predictionResult.cluster_name}
                  </p>
                  <p className="text-xs text-purple-700 mt-2">
                    <strong>Similar to:</strong> {predictionResult.similar_ingredients.slice(0, 5).join(', ')}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Features Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">
              ML Features
            </h2>
            <ul className="space-y-3">
              <li className="flex items-start">
                <span className="text-2xl mr-3">🔍</span>
                <div>
                  <strong>Ingredient Clustering</strong>
                  <p className="text-sm text-gray-600">Groups similar ingredients using k-means</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-2xl mr-3">🎯</span>
                <div>
                  <strong>Recipe Recommendation</strong>
                  <p className="text-sm text-gray-600">Collaborative filtering for personalized suggestions</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-2xl mr-3">🔄</span>
                <div>
                  <strong>Substitution Finder</strong>
                  <p className="text-sm text-gray-600">Smart ingredient swaps using association rules</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-2xl mr-3">🌍</span>
                <div>
                  <strong>Cuisine Classification</strong>
                  <p className="text-sm text-gray-600">k-NN classifier for cuisine types</p>
                </div>
              </li>
              <li className="flex items-start">
                <span className="text-2xl mr-3">📊</span>
                <div>
                  <strong>Nutrition Predictor</strong>
                  <p className="text-sm text-gray-600">Predicts nutritional values</p>
                </div>
              </li>
            </ul>
          </div>
        </div>

        {/* Ingredient Clusters Display */}
        {showClusters && clusters.length > 0 && (
          <div className="mt-12 max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold text-gray-800">
                Ingredient Clusters (K-Means ML)
              </h2>
              <button
                onClick={() => setShowClusters(false)}
                className="text-gray-600 hover:text-gray-800 font-semibold"
              >
                Hide ✕
              </button>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {clusters.map(cluster => (
                <div key={cluster.cluster_id} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition duration-300">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-800">
                      {cluster.cluster_name}
                    </h3>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {cluster.count} items
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {cluster.ingredients.map((ing, idx) => (
                      <span key={idx} className="bg-green-50 text-green-700 px-3 py-1 rounded-full text-sm border border-green-200">
                        {ing}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>🤖 ML Algorithm:</strong> K-Means Clustering groups {clusters.reduce((sum, c) => sum + c.count, 0)} ingredients 
                into {clusters.length} clusters based on nutritional similarity (protein, carbs, fat, calories, fiber).
              </p>
            </div>
          </div>
        )}

        {/* Sample Recipes */}
        <div className="mt-12 max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold mb-6 text-gray-800">Sample Recipes</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {recipes.map(recipe => (
              <div key={recipe.id} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition duration-300">
                <h3 className="text-xl font-bold mb-2">{recipe.name}</h3>
                <p className="text-gray-600 mb-3">
                  <span className="font-semibold">Cuisine:</span> {recipe.cuisine}
                </p>
                <p className="text-gray-600 mb-3">
                  <span className="font-semibold">Difficulty:</span> {recipe.difficulty}
                </p>
                <div>
                  <span className="font-semibold text-gray-700">Ingredients:</span>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {recipe.ingredients.map((ing, idx) => (
                      <span key={idx} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                        {ing}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
