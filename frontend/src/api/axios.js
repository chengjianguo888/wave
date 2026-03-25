import axios from 'axios'

// Create axios instance with default timeout configuration
const axiosInstance = axios.create({
  timeout: 10000, // 10 second timeout for all requests
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for better error handling
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      console.error('Request timeout:', error.message)
      error.message = 'Request timed out. Please check your connection and try again.'
    } else if (!error.response) {
      console.error('Network error:', error.message)
      error.message = 'Network error. Please check if the backend server is running.'
    }
    return Promise.reject(error)
  }
)

export default axiosInstance
