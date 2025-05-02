import React, { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

const ResultsDisplay = ({ results }) => {
  const [activeTab, setActiveTab] = useState('results')
  
  if (!results) return null
  
  const { natural_language_query, sql_query, explanation, results: queryResults, parameters } = results
  
  // Function to determine if results is an array
  const isResultsArray = Array.isArray(queryResults)
  
  // Function to render table for array results
  const renderTable = () => {
    if (!isResultsArray || queryResults.length === 0) return null
    
    // Get all unique keys from all objects
    const allKeys = [...new Set(queryResults.flatMap(obj => Object.keys(obj)))]
    
    return (
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              {allKeys.map((key, index) => (
                <th key={index} className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">
                  {key}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {queryResults.map((row, rowIndex) => (
              <tr key={rowIndex} className={rowIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                {allKeys.map((key, cellIndex) => (
                  <td key={cellIndex} className="py-2 px-4 border-b text-sm text-gray-900">
                    {row[key] !== undefined && row[key] !== null 
                      ? String(row[key]) 
                      : <span className="text-gray-400">NULL</span>}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }
  
  // Function to render non-array results
  const renderNonArrayResults = () => {
    if (isResultsArray) return null
    
    return (
      <div className="bg-gray-100 p-4 rounded-md">
        <pre className="whitespace-pre-wrap text-sm">
          {JSON.stringify(queryResults, null, 2)}
        </pre>
      </div>
    )
  }
  
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Query Results</h2>
      
      <div className="mb-4 border-b border-gray-200">
        <nav className="flex">
          <button
            className={`py-2 px-4 font-medium text-sm focus:outline-none ${
              activeTab === 'results' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('results')}
          >
            Results
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm focus:outline-none ${
              activeTab === 'query' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('query')}
          >
            SQL Query
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm focus:outline-none ${
              activeTab === 'details' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('details')}
          >
            Details
          </button>
        </nav>
      </div>
      
      <div className="mt-4">
        {activeTab === 'results' && (
          <div>
            <div className="mb-4">
              <h3 className="text-md font-medium text-gray-700 mb-1">Natural Language Query:</h3>
              <p className="text-gray-900">{natural_language_query}</p>
            </div>
            
            <div className="mb-4">
              <h3 className="text-md font-medium text-gray-700 mb-1">Results:</h3>
              {isResultsArray ? (
                queryResults.length > 0 ? (
                  <div>
                    <p className="text-sm text-gray-500 mb-2">Found {queryResults.length} results</p>
                    {renderTable()}
                  </div>
                ) : (
                  <p className="text-gray-500">No results found</p>
                )
              ) : (
                renderNonArrayResults()
              )}
            </div>
          </div>
        )}
        
        {activeTab === 'query' && (
          <div>
            <div className="mb-4">
              <h3 className="text-md font-medium text-gray-700 mb-1">SQL Query:</h3>
              <SyntaxHighlighter language="sql" style={atomDark} wrapLongLines={true}>
                {sql_query}
              </SyntaxHighlighter>
            </div>
            
            <div className="mb-4">
              <h3 className="text-md font-medium text-gray-700 mb-1">Explanation:</h3>
              <p className="text-gray-900">{explanation}</p>
            </div>
          </div>
        )}
        
        {activeTab === 'details' && (
          <div>
            <div className="mb-4">
              <h3 className="text-md font-medium text-gray-700 mb-1">Extracted Parameters:</h3>
              <SyntaxHighlighter language="json" style={atomDark} wrapLongLines={true}>
                {JSON.stringify(parameters, null, 2)}
              </SyntaxHighlighter>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ResultsDisplay 