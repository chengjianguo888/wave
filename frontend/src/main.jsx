import React from 'react'
import ReactDOM from 'react-dom/client'
import axios from 'axios'
import App from './App'
import './index.css'

// Configure axios to avoid hanging requests and allow configurable API base URL
axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL || ''
axios.defaults.timeout = 10000

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
