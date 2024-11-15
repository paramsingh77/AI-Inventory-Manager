import React, { useState, useEffect } from 'react';
import './App.css';
import Upload from './Component/Upload';
import Inventory from './Component/Inventory';
import Alerts from './Component/Alerts';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [inventory, setInventory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch Inventory Data
  const fetchInventory = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/api/inventory");
      setInventory(response.data);
    } catch (error) {
      setError('Error fetching inventory');
    } finally {
      setLoading(false);
    }
  };

  // Fetch Alerts Data
  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:5000/api/alerts");
      setAlerts(response.data);
    } catch (error) {
      setError('Error fetching alerts');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
    fetchAlerts();
  }, []);

  // Handle File Upload
  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await fetch("http://127.0.0.1:5000/api/upload", {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      // Check if response is JSON
      const contentType = response.headers.get("Content-Type");
      if (contentType && contentType.includes("application/json")) {
        const data = await response.json();
        alert("File uploaded successfully: " + data.message);
      } else {
        throw new Error("Unexpected response format");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file: " + error.message);
    }
  };

  return (
    <div className="App">
      <h1>Inventory Management System</h1>
      
      {/* Upload Component */}
      <Upload 
        file={file} 
        onFileChange={handleFileChange} 
        onUpload={handleUpload}
        error={error}
      />
      
      {/* Inventory Component */}
      {loading ? <div>Loading Inventory...</div> : <Inventory inventory={inventory} />}
      
      {/* Alerts Component */}
      {loading ? <div>Loading Alerts...</div> : <Alerts alerts={alerts} />}
    </div>
  );
}

export default App;
