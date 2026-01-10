import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')
  const [recipes, setRecipes] = useState([])
  const [ingredients, setIngredients] = useState('')

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
