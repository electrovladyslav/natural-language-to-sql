import React, { useState } from 'react'

const DatabaseInfo = ({ schema, sampleData }) => {
  const [activeTab, setActiveTab] = useState('schema')
  
  if (!schema || !sampleData) {
    return (
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Database Information</h2>
        <p className="text-gray-500">Loading database information...</p>
      </div>
    )
  }
  
  // Function to render the schema
  const renderSchema = () => {
    return (
      <div>
        <h3 className="text-md font-medium text-gray-700 mb-2">Customers Table</h3>
        <div className="overflow-x-auto mb-6">
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Column</th>
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Type</th>
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Primary Key</th>
              </tr>
            </thead>
            <tbody>
              {schema.customers.map((col, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">{col.name}</td>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">{col.type}</td>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">
                    {col.pk === 1 ? 'Yes' : 'No'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <h3 className="text-md font-medium text-gray-700 mb-2">Orders Table</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Column</th>
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Type</th>
                <th className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">Primary Key</th>
              </tr>
            </thead>
            <tbody>
              {schema.orders.map((col, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">{col.name}</td>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">{col.type}</td>
                  <td className="py-2 px-4 border-b text-sm text-gray-900">
                    {col.pk === 1 ? 'Yes' : 'No'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <div className="mt-4 p-3 bg-blue-50 border border-blue-100 rounded text-sm text-gray-700">
          <p><strong>Relationship:</strong> One customer can have many orders (1:N relationship)</p>
        </div>
      </div>
    )
  }
  
  // Function to render sample data
  const renderSampleData = () => {
    return (
      <div>
        <h3 className="text-md font-medium text-gray-700 mb-2">Customers Sample Data</h3>
        <div className="overflow-x-auto mb-6">
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                {Object.keys(sampleData.customers[0] || {}).map((key, index) => (
                  <th key={index} className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sampleData.customers.map((customer, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  {Object.values(customer).map((value, valueIndex) => (
                    <td key={valueIndex} className="py-2 px-4 border-b text-sm text-gray-900">
                      {value !== null ? String(value) : <span className="text-gray-400">NULL</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        <h3 className="text-md font-medium text-gray-700 mb-2">Orders Sample Data</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                {Object.keys(sampleData.orders[0] || {}).map((key, index) => (
                  <th key={index} className="py-2 px-4 border-b text-left text-sm font-medium text-gray-700">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sampleData.orders.map((order, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  {Object.values(order).map((value, valueIndex) => (
                    <td key={valueIndex} className="py-2 px-4 border-b text-sm text-gray-900">
                      {value !== null ? String(value) : <span className="text-gray-400">NULL</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
  
  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-4">Database Information</h2>
      
      <div className="mb-4 border-b border-gray-200">
        <nav className="flex">
          <button
            className={`py-2 px-4 font-medium text-sm focus:outline-none ${
              activeTab === 'schema' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('schema')}
          >
            Schema
          </button>
          <button
            className={`py-2 px-4 font-medium text-sm focus:outline-none ${
              activeTab === 'sample' 
                ? 'border-b-2 border-blue-500 text-blue-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('sample')}
          >
            Sample Data
          </button>
        </nav>
      </div>
      
      <div className="mt-4">
        {activeTab === 'schema' && renderSchema()}
        {activeTab === 'sample' && renderSampleData()}
      </div>
    </div>
  )
}

export default DatabaseInfo 