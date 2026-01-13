import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState('checking...')
  const [recipes, setRecipes] = useState([])
  const [selectedUser, setSelectedUser] = useState(0)
  const [userRecommendations, setUserRecommendations] = useState([])
  const [selectedRecipe, setSelectedRecipe] = useState(null)
  const [similarRecipes, setSimilarRecipes] = useState([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('substitution') // 'collaborative', 'content-based', 'clustering', or 'substitution'
  const [clusters, setClusters] = useState([])
  const [showClusters, setShowClusters] = useState(false)
  const [predictionResult, setPredictionResult] = useState(null)
  const [newIngredient, setNewIngredient] = useState({
    name: '',
    protein: '',
    carbs: '',
    fat: '',
    calories: '',
    fiber: ''
  })
  
  // Substitution feature states
  const [substitutionInput, setSubstitutionInput] = useState('')
  const [substitutionResults, setSubstitutionResults] = useState(null)
  const [availableIngredients, setAvailableIngredients] = useState([])

  useEffect(() => {
    // Check API health
    axios.get('/api/health')
      .then(res => setApiStatus(res.data.message))
      .catch(() => setApiStatus('API not reachable'))

    // Load all recipes
    loadRecipes()
  }, [])

  const loadRecipes = () => {
    axios.get('/api/recipes')
      .then(res => {
        setRecipes(res.data.recipes || [])
      })
      .catch(err => console.error('Error loading recipes:', err))
  }

  const getCollaborativeRecommendations = () => {
    setLoading(true)
    axios.get(`/api/recommend/user/${selectedUser}?top_n=5`)
      .then(res => {
        setUserRecommendations(res.data.recommendations)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error getting recommendations:', err)
        setLoading(false)
      })
  }

  const getContentBasedRecommendations = (recipeId) => {
    setLoading(true)
    setSelectedRecipe(recipeId)
    axios.get(`/api/recommend/similar/${recipeId}?top_n=5`)
      .then(res => {
        setSimilarRecipes(res.data.recommendations)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error getting similar recipes:', err)
        setLoading(false)
      })
  }

  const loadIngredientClusters = () => {
    setLoading(true)
    axios.get('/api/cluster/ingredients')
      .then(res => {
        if (res.data.success) {
          setClusters(res.data.clusters)
          setShowClusters(true)
        }
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
      alert('Please fill in all nutritional values')
      return
    }

    setLoading(true)
    axios.post('/api/cluster/predict', {
      name: newIngredient.name || 'Unknown Ingredient',
      features: features
    })
      .then(res => {
        if (res.data.success) {
          setPredictionResult(res.data)
        }
        setLoading(false)
      })
      .catch(err => {
        console.error('Error predicting cluster:', err)
        setLoading(false)
      })
  }

  const handleIngredientChange = (field, value) => {
    setNewIngredient(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const findSubstitutes = () => {
    if (!substitutionInput.trim()) {
      alert('Please enter an ingredient')
      return
    }

    setLoading(true)
    axios.post('/api/substitute', {
      ingredient: substitutionInput,
      top_n: 5
    })
      .then(res => {
        setSubstitutionResults(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error finding substitutes:', err)
        alert('Could not find substitutes for that ingredient')
        setLoading(false)
      })
  }

  const loadAvailableIngredients = () => {
    axios.get('/api/substitute/ingredients')
      .then(res => {
        setAvailableIngredients(res.data.ingredients || [])
      })
      .catch(err => console.error('Error loading ingredients:', err))
  }

  const findSubstitutesFor = (ingredient) => {
    setSubstitutionInput(ingredient)
    setLoading(true)
    axios.post('/api/substitute', {
      ingredient: ingredient,
      top_n: 5
    })
      .then(res => {
        setSubstitutionResults(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error finding substitutes:', err)
        alert('Could not find substitutes for that ingredient')
        setLoading(false)
      })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🍳 Recipe Recommender
          </h1>
          <p className="text-xl text-gray-600">
            Personalized recipe suggestions using collaborative filtering
          </p>
          <div className="mt-4 inline-block bg-white px-4 py-2 rounded-full shadow">
            <span className="text-sm text-gray-600">API Status: </span>
            <span className="font-semibold text-green-600">{apiStatus}</span>
          </div>
        </header>

        {/* Tab Navigation */}
        <div className="max-w-6xl mx-auto mb-8">
          <div className="flex justify-center space-x-4 flex-wrap gap-2">
            <button
              onClick={() => setActiveTab('substitution')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'substitution'
                  ? 'bg-green-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              🔄 Ingredient Substitution
            </button>
            <button
              onClick={() => setActiveTab('clustering')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'clustering'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              🔍 Ingredient Clustering
            </button>
            <button
              onClick={() => setActiveTab('collaborative')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'collaborative'
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              👥 Collaborative Filtering
            </button>
            <button
              onClick={() => setActiveTab('content-based')}
              className={`px-6 py-3 rounded-lg font-semibold transition ${
                activeTab === 'content-based'
                  ? 'bg-pink-600 text-white shadow-lg'
                  : 'bg-white text-gray-600 hover:bg-gray-100'
              }`}
            >
              🔍 Content-Based Filtering
            </button>
          </div>
        </div>

        {/* Ingredient Substitution Tab */}
        {activeTab === 'substitution' && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                🔄 Ingredient Substitution Finder
              </h2>
              <p className="text-gray-600 mb-6">
                Find alternative ingredients using association rule mining. Based on ingredient co-occurrence patterns in recipes.
              </p>

              {/* Input Section */}
              <div className="mb-6">
                <label className="block text-gray-700 font-semibold mb-2">
                  Enter an ingredient:
                </label>
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={substitutionInput}
                    onChange={(e) => setSubstitutionInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && findSubstitutes()}
                    placeholder="e.g., chicken, milk, eggs, pasta..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  />
                  <button
                    onClick={findSubstitutes}
                    disabled={loading}
                    className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition disabled:opacity-50"
                  >
                    {loading ? 'Searching...' : 'Find Substitutes'}
                  </button>
                  {substitutionResults && (
                    <button
                      onClick={() => setSubstitutionResults(null)}
                      className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition"
                    >
                      Hide All
                    </button>
                  )}
                </div>
                
                <div className="mt-3 flex gap-3">
                  <button
                    onClick={loadAvailableIngredients}
                    className="text-sm text-green-600 hover:text-green-700 underline"
                  >
                    View all available ingredients
                  </button>
                  {availableIngredients.length > 0 && (
                    <button
                      onClick={() => setAvailableIngredients([])}
                      className="text-sm text-red-600 hover:text-red-700 underline"
                    >
                      Hide ingredients list
                    </button>
                  )}
                </div>
              </div>

              {/* Available Ingredients */}
              {availableIngredients.length > 0 && (
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-semibold text-gray-700 mb-2">Available Ingredients ({availableIngredients.length}):</h3>
                  <div className="flex flex-wrap gap-2">
                    {availableIngredients.map(ing => (
                      <button
                        key={ing}
                        onClick={() => setSubstitutionInput(ing)}
                        className="px-3 py-1 bg-white border border-gray-300 rounded-full text-sm hover:bg-green-50 hover:border-green-500 transition"
                      >
                        {ing}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Results Section */}
              {substitutionResults && (
                <div className="mt-6">
                  <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg p-6 mb-6">
                    <h3 className="text-xl font-bold text-gray-800 mb-2">
                      Ingredient: {substitutionResults.ingredient}
                    </h3>
                    
                    {substitutionResults.ingredient_info && (
                      <div className="text-sm text-gray-600 space-y-1">
                        <p>Category: <span className="font-semibold">{substitutionResults.ingredient_info.category}</span></p>
                        <p>Appears in: <span className="font-semibold">{substitutionResults.ingredient_info.appears_in}</span> recipes</p>
                        <p>Frequency: <span className="font-semibold">{(substitutionResults.ingredient_info.frequency * 100).toFixed(1)}%</span></p>
                      </div>
                    )}
                  </div>

                  {substitutionResults.substitutes && substitutionResults.substitutes.length > 0 ? (
                    <div>
                      <h3 className="text-lg font-bold text-gray-800 mb-4">
                        🔄 Recommended Substitutes:
                      </h3>
                      <div className="grid md:grid-cols-2 gap-4">
                        {substitutionResults.substitutes.map((sub, idx) => (
                          <div
                            key={idx}
                            className="bg-gradient-to-r from-green-100 to-teal-100 rounded-lg p-4 shadow-md hover:shadow-lg transition"
                          >
                            <div className="flex justify-between items-start mb-2">
                              <h4 className="font-bold text-lg text-gray-800">
                                {idx + 1}. {sub.substitute}
                              </h4>
                              <button
                                onClick={() => findSubstitutesFor(sub.substitute)}
                                className="text-xs bg-white px-3 py-1 rounded hover:bg-green-600 hover:text-white transition"
                              >
                                Find more →
                              </button>
                            </div>
                            <div className="space-y-1 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-600">Confidence:</span>
                                <span className="font-semibold text-green-700">
                                  {(sub.confidence * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Support:</span>
                                <span className="font-semibold text-blue-700">
                                  {(sub.support * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Category:</span>
                                <span className="font-semibold text-purple-700">
                                  {sub.category}
                                </span>
                              </div>
                            </div>
                            
                            {/* Progress bars */}
                            <div className="mt-3 space-y-2">
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-green-600 h-2 rounded-full transition-all"
                                  style={{ width: `${sub.confidence * 100}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      
                      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                        <h4 className="font-semibold text-gray-800 mb-2">📊 Understanding the Metrics:</h4>
                        <ul className="text-sm text-gray-700 space-y-1">
                          <li><strong>Confidence:</strong> How similar the substitute is based on usage context</li>
                          <li><strong>Support:</strong> How frequently this ingredient appears in recipes</li>
                          <li><strong>Category:</strong> The ingredient classification type</li>
                        </ul>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <p className="text-lg">No substitutes found for "{substitutionResults.ingredient}"</p>
                      <p className="text-sm mt-2">Try a different ingredient or check the available ingredients list</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Ingredient Clustering Tab */}
        {activeTab === 'clustering' && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                🔍 Ingredient Clustering
              </h2>
              <p className="text-gray-600 mb-6">
                View ingredient groups or predict which cluster a new ingredient belongs to
              </p>
              
              <button
                onClick={loadIngredientClusters}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 mb-6"
              >
                {loading ? 'Loading...' : showClusters ? 'Refresh Clusters' : 'View All Clusters'}
              </button>

              {showClusters && clusters.length > 0 && (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {clusters.map((cluster) => (
                    <div key={cluster.cluster_id} className="bg-gradient-to-br from-blue-100 to-cyan-100 rounded-lg p-6 shadow-md">
                      <h3 className="text-lg font-bold text-gray-800 mb-2">{cluster.cluster_name}</h3>
                      <p className="text-sm text-gray-600 mb-3">Cluster #{cluster.cluster_id} • {cluster.count} ingredients</p>
                      <ul className="space-y-1">
                        {cluster.ingredients.map((ing, idx) => (
                          <li key={idx} className="text-sm text-gray-700 bg-white px-2 py-1 rounded">
                            {ing}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}

              <div className="border-t pt-8">
                <h3 className="text-xl font-bold text-gray-800 mb-4">🎯 Predict Ingredient Cluster</h3>
                <div className="grid md:grid-cols-2 gap-4 mb-4">
                  <input
                    type="text"
                    placeholder="Ingredient Name"
                    value={newIngredient.name}
                    onChange={(e) => handleIngredientChange('name', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="number"
                    placeholder="Protein (g)"
                    value={newIngredient.protein}
                    onChange={(e) => handleIngredientChange('protein', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="number"
                    placeholder="Carbs (g)"
                    value={newIngredient.carbs}
                    onChange={(e) => handleIngredientChange('carbs', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="number"
                    placeholder="Fat (g)"
                    value={newIngredient.fat}
                    onChange={(e) => handleIngredientChange('fat', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="number"
                    placeholder="Calories"
                    value={newIngredient.calories}
                    onChange={(e) => handleIngredientChange('calories', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                  <input
                    type="number"
                    placeholder="Fiber (g)"
                    value={newIngredient.fiber}
                    onChange={(e) => handleIngredientChange('fiber', e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
                <button
                  onClick={predictIngredientCluster}
                  disabled={loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                >
                  {loading ? 'Predicting...' : 'Predict Cluster'}
                </button>

                {predictionResult && (
                  <div className="mt-6 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg p-6">
                    <h4 className="text-lg font-bold text-gray-800 mb-2">Prediction Result</h4>
                    <p className="text-gray-700 mb-2">
                      <strong>{predictionResult.ingredient}</strong> belongs to:
                    </p>
                    <p className="text-xl font-bold text-blue-700 mb-3">{predictionResult.cluster_name}</p>
                    <p className="text-sm text-gray-600 mb-2">Similar ingredients:</p>
                    <div className="flex flex-wrap gap-2">
                      {predictionResult.similar_ingredients.map((ing, idx) => (
                        <span key={idx} className="bg-white px-3 py-1 rounded text-sm text-gray-700">
                          {ing}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Collaborative Filtering Tab */}
        {activeTab === 'collaborative' && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                👥 Get Personalized Recommendations
              </h2>
              <p className="text-gray-600 mb-6">
                Select a user profile to get recipe recommendations based on similar users' preferences
              </p>
              
              <div className="flex items-center space-x-4 mb-6">
                <label className="text-gray-700 font-semibold">Select User:</label>
                <select
                  value={selectedUser}
                  onChange={(e) => setSelectedUser(Number(e.target.value))}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  <option value={0}>User 1 - Likes healthy food</option>
                  <option value={1}>User 2 - Likes Italian cuisine</option>
                  <option value={2}>User 3 - Prefers light meals</option>
                  <option value={3}>User 4 - Loves spicy food</option>
                  <option value={4}>User 5 - Enjoys complex dishes</option>
                  <option value={5}>User 6 - Quick & healthy</option>
                  <option value={6}>User 7 - Mexican/Asian fan</option>
                  <option value={7}>User 8 - Italian/French lover</option>
                  <option value={8}>User 9 - Salad enthusiast</option>
                  <option value={9}>User 10 - Spicy food lover</option>
                </select>
                <button
                  onClick={getCollaborativeRecommendations}
                  disabled={loading}
                  className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition disabled:opacity-50"
                >
                  {loading ? 'Loading...' : 'Get Recommendations'}
                </button>
              </div>

              {/* Recommendations Display */}
              {userRecommendations.length > 0 && (
                <div className="mt-8">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">
                    🎯 Recommended Recipes for You
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {userRecommendations.map((recipe, idx) => (
                      <div key={idx} className="bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg p-6 shadow-md">
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="text-lg font-bold text-gray-800">{recipe.name}</h4>
                          <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded-full">
                            {recipe.cuisine}
                          </span>
                        </div>
                        <div className="mb-3">
                          <span className="text-sm text-gray-600">Predicted Rating: </span>
                          <span className="font-bold text-purple-700">{recipe.predicted_rating} ⭐</span>
                        </div>
                        <div className="text-sm text-gray-700">
                          <strong>Ingredients:</strong>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {recipe.ingredients.map((ing, i) => (
                              <span key={i} className="bg-white px-2 py-1 rounded text-xs">
                                {ing}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="mt-3 text-xs text-gray-500">
                          Prep: {recipe.features[0]}min • Difficulty: {recipe.features[1]}/5 • Spice: {recipe.features[2]}/5
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Content-Based Filtering Tab */}
        {activeTab === 'content-based' && (
          <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                🔍 Find Similar Recipes
              </h2>
              <p className="text-gray-600 mb-6">
                Click on any recipe to find similar dishes based on ingredients and features
              </p>

              {/* Recipe Grid */}
              <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
                {recipes.map((recipe) => (
                  <button
                    key={recipe.id}
                    onClick={() => getContentBasedRecommendations(recipe.id)}
                    className={`text-left p-4 rounded-lg border-2 transition ${
                      selectedRecipe === recipe.id
                        ? 'border-pink-500 bg-pink-50 shadow-md'
                        : 'border-gray-200 bg-white hover:border-pink-300 hover:shadow-md'
                    }`}
                  >
                    <h4 className="font-bold text-gray-800 mb-1">{recipe.name}</h4>
                    <span className="text-xs bg-pink-100 text-pink-700 px-2 py-1 rounded">
                      {recipe.cuisine}
                    </span>
                  </button>
                ))}
              </div>

              {/* Similar Recipes Display */}
              {similarRecipes.length > 0 && (
                <div className="mt-8 pt-8 border-t border-gray-200">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">
                    ✨ Similar Recipes
                  </h3>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {similarRecipes.map((recipe, idx) => (
                      <div key={idx} className="bg-gradient-to-br from-pink-100 to-orange-100 rounded-lg p-6 shadow-md">
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="text-lg font-bold text-gray-800">{recipe.name}</h4>
                          <span className="bg-pink-600 text-white text-xs px-2 py-1 rounded-full">
                            {recipe.cuisine}
                          </span>
                        </div>
                        <div className="mb-3">
                          <span className="text-sm text-gray-600">Similarity Score: </span>
                          <span className="font-bold text-pink-700">{(recipe.similarity_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="text-sm text-gray-700">
                          <strong>Ingredients:</strong>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {recipe.ingredients.map((ing, i) => (
                              <span key={i} className="bg-white px-2 py-1 rounded text-xs">
                                {ing}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div className="mt-3 text-xs text-gray-500">
                          Prep: {recipe.features[0]}min • Difficulty: {recipe.features[1]}/5 • Spice: {recipe.features[2]}/5
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Footer Info */}
        <div className="max-w-6xl mx-auto mt-12 text-center text-gray-600">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-bold text-gray-800 mb-3">🤖 ML Algorithms Used</h3>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="bg-blue-50 p-4 rounded">
                <strong className="text-blue-700">K-Means Clustering</strong>
                <p className="mt-2 text-gray-600">
                  Groups ingredients into 6 clusters based on nutritional similarity
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded">
                <strong className="text-purple-700">Collaborative Filtering</strong>
                <p className="mt-2 text-gray-600">
                  Recommends recipes based on similar users' ratings using cosine similarity
                </p>
              </div>
              <div className="bg-pink-50 p-4 rounded">
                <strong className="text-pink-700">Content-Based Filtering</strong>
                <p className="mt-2 text-gray-600">
                  Finds similar recipes by analyzing features like prep time, difficulty, and spice level
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
