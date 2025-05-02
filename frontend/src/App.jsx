import React, { useState, useEffect } from 'react'
import axios from 'axios'
import QueryForm from './components/QueryForm'
import ResultsDisplay from './components/ResultsDisplay'
import DatabaseInfo from './components/DatabaseInfo'
import Header from './components/Header'
import Footer from './components/Footer'

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [schema, setSchema] = useState(null)
  const [sampleData, setSampleData] = useState(null)
  const [exampleQueries, setExampleQueries] = useState([])

  // Fetch database schema and sample data on component mount
  useEffect(() => {
    const fetchDatabaseInfo = async () => {
      try {
        // Fetch schema
        const schemaResponse = await axios.get('/api/tables')
        setSchema(schemaResponse.data)
        
        // Fetch sample data
        const sampleDataResponse = await axios.get('/api/sample-data')
        setSampleData(sampleDataResponse.data)
        
        // Fetch example queries
        const exampleQueriesResponse = await axios.get('/api/example-queries')
        setExampleQueries(exampleQueriesResponse.data.examples)
      } catch (err) {
        console.error('Error fetching database info:', err)
        setError('Could not load database information. Please try again later.')
      }
    }
    
    fetchDatabaseInfo()
  }, [])

  const processQuery = async (query) => {
    setLoading(true)
    setError(null)
    setResults(null)
    
    try {
      const response = await axios.post('/api/query', { query })
      setResults(response.data)
    } catch (err) {
      console.error('Error processing query:', err)
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error)
      } else {
        setError('An error occurred while processing your query. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header />
      
      <main className="flex-grow container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <DatabaseInfo 
              schema={schema} 
              sampleData={sampleData} 
            />
          </div>
          
          <div className="lg:col-span-2">
            <div className="card mb-6">
              <QueryForm 
                onSubmit={processQuery} 
                loading={loading} 
                exampleQueries={exampleQueries}
              />
            </div>
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-6">
                <strong className="font-bold">Error: </strong>
                <span className="block sm:inline">{error}</span>
              </div>
            )}
            
            {results && (
              <div className="card">
                <ResultsDisplay results={results} />
              </div>
            )}
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

export default App 