import React from 'react'

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-md">
      <div className="container mx-auto px-4 py-6">
        <h1 className="text-3xl font-bold">NL to SQL Converter</h1>
        <p className="text-blue-100 mt-2">
          Convert natural language queries to SQL using AI
        </p>
      </div>
    </header>
  )
}

export default Header 