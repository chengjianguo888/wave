import React, { useState, useEffect } from 'react'
import axios from '../api/axios'
import './DetectionHistory.css'

function DetectionHistory() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    loadHistory()
  }, [page])

  const loadHistory = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`/api/detections/history?page=${page}&per_page=10`)
      setHistory(response.data.detections)
      setTotal(response.data.total)
    } catch (err) {
      console.error('Failed to load history:', err)
      setError(err.message || 'Failed to load detection history')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (detectionId) => {
    try {
      const response = await axios.get(`/api/detections/${detectionId}/export?format=csv`, {
        responseType: 'blob'
      })

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `detection_${detectionId}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (err) {
      console.error('Export failed:', err)
      alert(err.message || 'Failed to export detection')
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
  }

  if (loading) {
    return <div className="loading">Loading history...</div>
  }

  if (error) {
    return (
      <div className="detection-panel">
        <h2>Detection History</h2>
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: '#f44336', marginBottom: '10px' }}>{error}</p>
          <button onClick={loadHistory} className="btn-primary">
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="detection-panel">
      <h2>Detection History</h2>

      {history.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
          No detections yet. Start by uploading an image!
        </p>
      ) : (
        <>
          <table className="history-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Filename</th>
                <th>Algorithm</th>
                <th>Waves</th>
                <th>Amplitude</th>
                <th>Confidence</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {history.map((detection) => (
                <tr key={detection.id}>
                  <td>{formatDate(detection.created_at)}</td>
                  <td>{detection.filename}</td>
                  <td>{detection.algorithm}</td>
                  <td>{detection.wave_count}</td>
                  <td>{detection.avg_amplitude?.toFixed(2) || 0}px</td>
                  <td>{((detection.confidence_score || 0) * 100).toFixed(1)}%</td>
                  <td>
                    <button
                      onClick={() => handleExport(detection.id)}
                      className="btn-secondary"
                    >
                      Export
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pagination">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="btn-secondary"
            >
              Previous
            </button>
            <span>Page {page} of {Math.ceil(total / 10)}</span>
            <button
              onClick={() => setPage(p => p + 1)}
              disabled={page >= Math.ceil(total / 10)}
              className="btn-secondary"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}

export default DetectionHistory
