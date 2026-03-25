import React, { useEffect, useRef } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

function WaveVisualizer({ detectionResult, imageUrl }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (imageUrl && detectionResult?.waves && canvasRef.current) {
      drawWavesOnImage()
    }
  }, [imageUrl, detectionResult])

  const drawWavesOnImage = () => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const img = new Image()

    img.onload = () => {
      // Set canvas size
      canvas.width = img.width
      canvas.height = img.height

      // Draw original image
      ctx.drawImage(img, 0, 0)

      // Draw wave detections
      ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)'
      ctx.lineWidth = 2

      detectionResult.waves.forEach((wave, idx) => {
        const { x, y } = wave.position
        const width = wave.wavelength || 50
        const height = wave.amplitude || 30

        // Draw bounding box
        ctx.strokeRect(x, y, width, height)

        // Draw label
        ctx.fillStyle = 'rgba(255, 0, 0, 0.8)'
        ctx.font = '12px Arial'
        ctx.fillText(`Wave ${idx + 1}`, x, y - 5)
      })
    }

    img.src = imageUrl
  }

  // Prepare chart data for amplitude distribution
  const getAmplitudeChartData = () => {
    if (!detectionResult?.waves) return null

    const amplitudes = detectionResult.waves.map(w => w.amplitude)

    return {
      labels: detectionResult.waves.map((_, idx) => `Wave ${idx + 1}`),
      datasets: [
        {
          label: 'Wave Amplitude (pixels)',
          data: amplitudes,
          borderColor: 'rgb(102, 126, 234)',
          backgroundColor: 'rgba(102, 126, 234, 0.1)',
          tension: 0.4
        }
      ]
    }
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: 'Wave Amplitude Distribution'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }

  const amplitudeData = getAmplitudeChartData()

  return (
    <div className="wave-visualizer">
      <h3>Visual Analysis</h3>

      {imageUrl && (
        <div className="visualization-container">
          <canvas ref={canvasRef} className="wave-canvas" />
        </div>
      )}

      {amplitudeData && (
        <div className="chart-container">
          <Line data={amplitudeData} options={chartOptions} />
        </div>
      )}

      {detectionResult?.waves && detectionResult.waves.length > 0 && (
        <div className="wave-details">
          <h4>Detected Waves (Top 10)</h4>
          <table className="wave-table">
            <thead>
              <tr>
                <th>Wave ID</th>
                <th>Position</th>
                <th>Amplitude</th>
                <th>Wavelength</th>
                <th>Area</th>
              </tr>
            </thead>
            <tbody>
              {detectionResult.waves.slice(0, 10).map((wave, idx) => (
                <tr key={idx}>
                  <td>{idx + 1}</td>
                  <td>({wave.position.x}, {wave.position.y})</td>
                  <td>{wave.amplitude.toFixed(2)}px</td>
                  <td>{wave.wavelength.toFixed(2)}px</td>
                  <td>{wave.area.toFixed(2)}px²</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default WaveVisualizer
