import React from 'react'

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-300 text-sm">
              &copy; {new Date().getFullYear()} NL to SQL Converter
            </p>
          </div>
          <div>
            <p className="text-gray-300 text-sm">
              A demo project for natural language to SQL conversion
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer 