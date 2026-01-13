import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')
  const [recipes, setRecipes] = useState([])
  const [ingredients, setIngredients] = useState('')
  
  // Cuisine Classification states
  const [cuisineIngredients, setCuisineIngredients] = useState('')
  const [cuisineResult, setCuisineResult] = useState(null)
  const [cuisineLoading, setCuisineLoading] = useState(false)

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

  const predictCuisine = () => {
    const ingredientList = cuisineIngredients.split(',').map(i => i.trim()).filter(i => i)
    
    if (ingredientList.length === 0) {
      alert('Please enter some ingredients')
      return
    }
    
    setCuisineLoading(true)
    axios.post('/api/cuisine/predict', { ingredients: ingredientList })
      .then(res => {
        setCuisineResult(res.data)
        setCuisineLoading(false)
      })
      .catch(err => {
        console.error('Error:', err)
        alert('Error predicting cuisine')
        setCuisineLoading(false)
      })
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

        {/* Cuisine Classification Section */}
        <div className="max-w-4xl mx-auto mt-12">
          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              🌍 Cuisine Classifier
            </h2>
            <p className="text-gray-600 mb-6">
              Enter ingredients and our k-NN algorithm will predict the cuisine type!
            </p>

            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">
                Ingredients (comma-separated):
              </label>
              <div className="flex gap-4">
                <input
                  type="text"
                  value={cuisineIngredients}
                  onChange={(e) => setCuisineIngredients(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && predictCuisine()}
                  placeholder="e.g., pasta, tomato sauce, mozzarella, basil"
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={predictCuisine}
                  disabled={cuisineLoading}
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 font-semibold"
                >
                  {cuisineLoading ? 'Predicting...' : 'Predict Cuisine'}
                </button>
              </div>
            </div>

            {/* Results */}
            {cuisineResult && cuisineResult.success && (
              <div className="mt-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-gray-800 mb-2">
                    🎯 Predicted Cuisine: <span className="text-blue-600">{cuisineResult.predicted_cuisine}</span>
                  </h3>
                  <p className="text-lg text-gray-700">
                    Confidence: <span className="font-semibold text-green-600">{cuisineResult.confidence.toFixed(1)}%</span>
                  </p>
                </div>

                {/* Top Predictions */}
                {cuisineResult.top_predictions && cuisineResult.top_predictions.length > 0 && (
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-700 mb-3">Top 3 Predictions:</h4>
                    <div className="space-y-2">
                      {cuisineResult.top_predictions.map((pred, idx) => (
                        <div key={idx} className="bg-white rounded-lg p-3 flex items-center justify-between">
                          <span className="font-medium">{idx + 1}. {pred.cuisine}</span>
                          <div className="flex items-center gap-3">
                            <div className="w-32 bg-gray-200 rounded-full h-3">
                              <div 
                                className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full"
                                style={{ width: `${pred.percentage}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-600 w-12">{pred.percentage.toFixed(1)}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Matched Ingredients */}
                <div className="mb-4">
                  <p className="text-sm text-gray-600">
                    Matched <span className="font-semibold">{cuisineResult.matched_count}</span> out of <span className="font-semibold">{cuisineResult.total_ingredients}</span> ingredients
                  </p>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {cuisineResult.matched_ingredients.map((ing, idx) => (
                      <span key={idx} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                        ✓ {ing}
                      </span>
                    ))}
                  </div>
                  {cuisineResult.unmatched_ingredients && cuisineResult.unmatched_ingredients.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {cuisineResult.unmatched_ingredients.map((ing, idx) => (
                        <span key={idx} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">
                          ✗ {ing}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Similar Recipes */}
                {cuisineResult.nearest_recipes && cuisineResult.nearest_recipes.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-3">Similar Recipes from Dataset:</h4>
                    <div className="grid gap-3">
                      {cuisineResult.nearest_recipes.map((recipe, idx) => (
                        <div key={idx} className="bg-white rounded-lg p-4">
                          <div className="flex justify-between items-start">
                            <div>
                              <h5 className="font-semibold">{recipe.name}</h5>
                              <p className="text-sm text-gray-600">{recipe.cuisine}</p>
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-1 mt-2">
                            {recipe.ingredients.map((ing, i) => (
                              <span key={i} className="text-xs bg-gray-100 px-2 py-1 rounded">
                                {ing}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {cuisineResult && !cuisineResult.success && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-700">{cuisineResult.error}</p>
              </div>
            )}
          </div>
        </div>

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
