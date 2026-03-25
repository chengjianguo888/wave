import React, { useState } from 'react'
import axios from 'axios'
import './Login.css'

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false)
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const endpoint = isRegister ? '/api/auth/register' : '/api/auth/login'
      const payload = isRegister
        ? formData
        : { username: formData.username, password: formData.password }

      const response = await axios.post(endpoint, payload)

      if (isRegister) {
        // After registration, automatically log in
        setError('')
        alert('Registration successful! Please log in.')
        setIsRegister(false)
      } else {
        // Handle login success
        const { access_token, user } = response.data
        onLogin(access_token, user)
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const toggleMode = () => {
    setIsRegister(!isRegister)
    setError('')
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Visual Wave Detection System</h1>
          <p>{isRegister ? 'Create your account' : 'Sign in to continue'}</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Enter your username"
            />
          </div>

          {isRegister && (
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder="Enter your email"
              />
            </div>
          )}

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Please wait...' : isRegister ? 'Register' : 'Login'}
          </button>
        </form>

        <div className="toggle-form">
          {isRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button type="button" onClick={toggleMode}>
            {isRegister ? 'Login' : 'Register'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Login
