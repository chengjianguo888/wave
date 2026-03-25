import React, { useState, useEffect, useRef } from 'react'
import axios from '../api/axios'
import WaveVisualizer from './WaveVisualizer'
import DetectionHistory from './DetectionHistory'
import './Dashboard.css'

const DEMO_IMAGE_DATA_URL = 'data:image/png;base64,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'

function Dashboard({ user, onLogout }) {
  const [stats, setStats] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [algorithm, setAlgorithm] = useState('edge_detection')
  const [sensitivity, setSensitivity] = useState(0.5)
  const [detectionResult, setDetectionResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [initialLoading, setInitialLoading] = useState(true)
  const [algorithms, setAlgorithms] = useState([])
  const [activeTab, setActiveTab] = useState('detect')
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    setInitialLoading(true)
    setError(null)
    try {
      await Promise.all([loadStats(), loadAlgorithms()])
    } catch (err) {
      console.error('Failed to load initial data:', err)
      setError(err.message || 'Failed to load initial data')
    } finally {
      setInitialLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const response = await axios.get('/api/stats/summary')
      setStats(response.data)
    } catch (err) {
      console.error('Failed to load stats:', err)
      // Don't throw, let component load anyway
    }
  }

  const loadAlgorithms = async () => {
    try {
      const response = await axios.get('/api/algorithms')
      setAlgorithms(response.data.algorithms)
    } catch (err) {
      console.error('Failed to load algorithms:', err)
      // Set default algorithms as fallback
      setAlgorithms([{
        id: 'edge_detection',
        name: 'Edge Detection',
        description: 'Classical edge detection using Canny algorithm'
      }])
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
          'Content-Type': 'multipart/form-data'
        },
        timeout: 30000 // 30 seconds for file upload
      })

      setDetectionResult(response.data.result)
      loadStats() // Refresh stats
    } catch (err) {
      console.error('Detection failed:', err)
      alert(err.message || 'Detection failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDemoDetect = async () => {
    setPreviewUrl(DEMO_IMAGE_DATA_URL)
    setSelectedFile(null)
    setDetectionResult(null)
    setLoading(true)

    try {
      const response = await axios.post('/api/detect/realtime', {
        image_data: DEMO_IMAGE_DATA_URL,
        algorithm,
        sensitivity
      }, getAuthHeaders())

      setDetectionResult(response.data.result)
      loadStats()
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

      {initialLoading && (
        <div className="loading" style={{ textAlign: 'center', padding: '40px' }}>
          Loading dashboard...
        </div>
      )}

      {error && !initialLoading && (
        <div style={{ textAlign: 'center', padding: '20px' }}>
          <p style={{ color: '#f44336', marginBottom: '10px' }}>{error}</p>
          <button onClick={loadInitialData} className="btn-primary">
            Retry
          </button>
        </div>
      )}

      {!initialLoading && !error && (
        <>
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

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', margin: '12px 0' }}>
            <button
              type="button"
              className="btn-secondary"
              onClick={handleDemoDetect}
              disabled={loading}
            >
              {loading ? 'Running demo...' : 'Try demo image'}
            </button>
            <button
              onClick={handleDetect}
              className="btn-primary"
              disabled={!selectedFile || loading}
            >
              {loading ? 'Detecting Waves...' : 'Start Detection'}
            </button>
          </div>

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
        </>
      )}
    </div>
  )
}

export default Dashboard
