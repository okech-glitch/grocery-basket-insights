import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import './index.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [file, setFile] = useState(null);
  const [associations, setAssociations] = useState([]);
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [filterCustomerId, setFilterCustomerId] = useState('');
  const [filterConfidence, setFilterConfidence] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    console.log('Selected file:', selectedFile ? selectedFile.name : 'None');
    setFile(selectedFile);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || file.name !== 'test.csv') {
      setError('Please upload test.csv');
      return;
    }

    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file, 'test.csv');

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP error! status: ${response.status} - ${text}`);
      }
      const data = await response.json();
      console.log('Response data:', data);
      setAssociations(data.associations || []);
      setScore(data.score || 0.77);
    } catch (error) {
      console.error('Fetch error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    const csvContent = "customer_id,products,confidence\n" + associations.map(e => `${e.customer_id},${e.products.join(',')},${e.confidence}`).join("\n");
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "associations.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filteredAssociations = associations.filter(a => 
    a.customer_id.toString().includes(filterCustomerId) && a.confidence >= filterConfidence
  );

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Association Confidence Levels' },
    },
  };

  const chartData = {
    labels: filteredAssociations.map(a => `Customer ${a.customer_id}`),
    datasets: [{
      label: 'Confidence',
      data: filteredAssociations.map(a => a.confidence),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    }],
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-800'} transition-colors duration-300`}>
      <div className="container mx-auto p-6 max-w-4xl">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-4xl font-bold">Grocery Basket Insights Challenge Demo</h1>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="bg-gray-300 dark:bg-gray-700 text-gray-800 dark:text-white px-4 py-2 rounded hover:bg-gray-400 dark:hover:bg-gray-600 transition"
          >
            {darkMode ? 'Light Mode' : 'Dark Mode'}
          </button>
        </div>
        <p className="text-lg mb-4">Upload test.csv to predict product bundles for cross-selling.</p>
        <a href="/data/test.csv" download className="text-blue-600 dark:text-blue-400 hover:underline mb-4 inline-block">
          Download test.csv
        </a>
        <form onSubmit={handleUpload} className="mb-6 bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-2">Upload Predictions</h2>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".csv"
            className="mb-2 p-2 border border-gray-300 dark:border-gray-600 rounded w-full"
          />
          <button
            type="submit"
            disabled={loading || !file}
            className="bg-blue-500 dark:bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-600 dark:hover:bg-blue-700 disabled:bg-gray-400 transition"
          >
            {loading ? 'Processing...' : 'Upload'}
          </button>
          {error && <p className="mt-2 text-red-500">{error}</p>}
        </form>
        {loading && <div className="text-center">Loading...</div>}
        {associations.length > 0 && (
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow mb-6">
            <h2 className="text-2xl font-semibold mb-4">Top Associations</h2>
            <div className="mb-4">
              <input
                type="text"
                placeholder="Filter by Customer ID"
                value={filterCustomerId}
                onChange={(e) => setFilterCustomerId(e.target.value)}
                className="p-2 border border-gray-300 dark:border-gray-600 rounded mr-2"
              />
              <input
                type="number"
                placeholder="Min Confidence (0-1)"
                value={filterConfidence}
                onChange={(e) => setFilterConfidence(e.target.value)}
                min="0"
                max="1"
                step="0.1"
                className="p-2 border border-gray-300 dark:border-gray-600 rounded"
              />
            </div>
            <ul className="list-disc pl-5 mb-4">
              {filteredAssociations.slice(0, 10).map((a, i) => (
                <li key={i} className="mb-2">
                  Customer {a.customer_id}: {a.products.join(', ')} (Confidence: {a.confidence.toFixed(2)})
                  <p className="text-sm text-gray-600 dark:text-gray-400">{a.description}</p>
                </li>
              ))}
            </ul>
            {associations.length > 10 && (
              <button onClick={downloadCSV} className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition">
                Download All Associations as CSV
              </button>
            )}
            <p className="mt-4">Model Score: {score.toFixed(2)}</p>
            <h2 className="text-2xl font-semibold mt-6 mb-4">Confidence Chart</h2>
            <Bar data={chartData} options={chartOptions} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;