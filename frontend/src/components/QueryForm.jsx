import React, { useState } from 'react'

const QueryForm = ({ onSubmit, loading, exampleQueries = [] }) => {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSubmit(query.trim())
    }
  }

  const handleExampleClick = (example) => {
    setQuery(example)
    onSubmit(example)
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Ask about the data</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="query" className="block text-gray-700 text-sm font-medium mb-2">
            Enter your question in natural language
          </label>
          <textarea
            id="query"
            rows="3"
            className="input-field"
            placeholder="e.g., Show me all customers who are older than 30"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={loading}
          />
        </div>
        
        <div className="flex justify-end">
          <button
            type="submit"
            className="btn-primary"
            disabled={loading || !query.trim()}
          >
            {loading ? 'Processing...' : 'Run Query'}
          </button>
        </div>
      </form>
      
      {exampleQueries.length > 0 && (
        <div className="mt-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Or try one of these examples:</h3>
          <div className="flex flex-wrap gap-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1 rounded-full transition-colors"
                disabled={loading}
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default QueryForm 