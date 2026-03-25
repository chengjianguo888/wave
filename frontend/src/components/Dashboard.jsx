import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import WaveVisualizer from './WaveVisualizer'
import DetectionHistory from './DetectionHistory'
import './Dashboard.css'

function Dashboard({ user, onLogout }) {
  const [stats, setStats] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [algorithm, setAlgorithm] = useState('edge_detection')
  const [sensitivity, setSensitivity] = useState(0.5)
  const [detectionResult, setDetectionResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [algorithms, setAlgorithms] = useState([])
  const [activeTab, setActiveTab] = useState('detect')
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadStats()
    loadAlgorithms()
  }, [])

  const getAuthHeaders = () => ({
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`
    }
  })

  const loadStats = async () => {
    try {
      const response = await axios.get('/api/stats/summary', getAuthHeaders())
      setStats(response.data)
    } catch (err) {
      console.error('Failed to load stats:', err)
    }
  }

  const loadAlgorithms = async () => {
    try {
      const response = await axios.get('/api/algorithms', getAuthHeaders())
      setAlgorithms(response.data.algorithms)
    } catch (err) {
      console.error('Failed to load algorithms:', err)
    }
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setDetectionResult(null)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.currentTarget.classList.add('dragover')
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.currentTarget.classList.remove('dragover')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.currentTarget.classList.remove('dragover')

    const file = e.dataTransfer.files[0]
    if (file) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setDetectionResult(null)
    }
  }

  const handleDetect = async () => {
    if (!selectedFile) {
      alert('Please select an image first')
      return
    }

    setLoading(true)
    setDetectionResult(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('algorithm', algorithm)
      formData.append('sensitivity', sensitivity)

      const response = await axios.post('/api/detect/upload', formData, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'multipart/form-data'
        }
      })

      setDetectionResult(response.data.result)
      loadStats() // Refresh stats
    } catch (err) {
      alert(err.response?.data?.error || 'Detection failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Wave Detection System</h1>
        <div className="user-info">
          <span>Welcome, {user?.username}</span>
          <button onClick={onLogout} className="btn-logout">Logout</button>
        </div>
      </div>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Detections</h3>
            <div className="stat-value">{stats.total_detections || 0}</div>
          </div>
          <div className="stat-card">
            <h3>Total Waves Detected</h3>
            <div className="stat-value">{stats.total_waves || 0}</div>
          </div>
          <div className="stat-card">
            <h3>Average Confidence</h3>
            <div className="stat-value">
              {stats.avg_confidence ? (stats.avg_confidence * 100).toFixed(1) : 0}%
            </div>
          </div>
        </div>
      )}

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'detect' ? 'active' : ''}`}
          onClick={() => setActiveTab('detect')}
        >
          Wave Detection
        </button>
        <button
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Detection History
        </button>
      </div>

      {activeTab === 'detect' && (
        <div className="detection-panel">
          <h2>Upload Image for Wave Detection</h2>

          <div
            className="upload-area"
            onClick={() => fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            {previewUrl ? (
              <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', maxHeight: '300px' }} />
            ) : (
              <div>
                <p style={{ fontSize: '48px', marginBottom: '10px' }}>📷</p>
                <p>Click to upload or drag and drop</p>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
                  Supported formats: JPG, PNG, GIF, BMP
                </p>
              </div>
            )}
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />

          <div className="algorithm-selector">
            <label>Detection Algorithm</label>
            <select value={algorithm} onChange={(e) => setAlgorithm(e.target.value)}>
              {algorithms.map(alg => (
                <option key={alg.id} value={alg.id}>
                  {alg.name} - {alg.description}
                </option>
              ))}
            </select>
          </div>

          <div className="sensitivity-slider">
            <label>Sensitivity: {(sensitivity * 100).toFixed(0)}%</label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={sensitivity}
              onChange={(e) => setSensitivity(parseFloat(e.target.value))}
            />
          </div>

          <button
            onClick={handleDetect}
            className="btn-primary"
            disabled={!selectedFile || loading}
          >
            {loading ? 'Detecting Waves...' : 'Start Detection'}
          </button>

          {detectionResult && (
            <div className="detection-result">
              <h3>Detection Results</h3>

              <div className="result-grid">
                <div className="result-item">
                  <label>Wave Count</label>
                  <div className="value">{detectionResult.wave_count}</div>
                </div>
                <div className="result-item">
                  <label>Avg Amplitude</label>
                  <div className="value">{detectionResult.avg_amplitude.toFixed(2)}px</div>
                </div>
                <div className="result-item">
                  <label>Avg Frequency</label>
                  <div className="value">{detectionResult.avg_frequency.toFixed(4)}</div>
                </div>
                <div className="result-item">
                  <label>Confidence</label>
                  <div className="value">{(detectionResult.confidence_score * 100).toFixed(1)}%</div>
                </div>
              </div>

              <WaveVisualizer detectionResult={detectionResult} imageUrl={previewUrl} />
            </div>
          )}
        </div>
      )}

      {activeTab === 'history' && (
        <DetectionHistory />
      )}
    </div>
  )
}

export default Dashboard
