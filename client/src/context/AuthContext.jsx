import { createContext, useReducer, useEffect, useCallback } from 'react'
import { api, setTokens, clearTokens, getToken } from '../utils/api'

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext(null)

const initialState = { user: null, isAuthenticated: !!getToken(), loading: true }

function authReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload, isAuthenticated: true, loading: false }
    case 'LOGOUT':
      return { user: null, isAuthenticated: false, loading: false }
    case 'LOADED':
      return { ...state, loading: false }
    default:
      return state
  }
}

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  const fetchUser = useCallback(async () => {
    if (!getToken()) {
      dispatch({ type: 'LOADED' })
      return
    }
    try {
      const user = await api('/auth/me', { auth: true })
      dispatch({ type: 'SET_USER', payload: user })
    } catch {
      clearTokens()
      dispatch({ type: 'LOGOUT' })
    }
  }, [])

  useEffect(() => { fetchUser() }, [fetchUser])

  useEffect(() => {
    const handleLogout = () => dispatch({ type: 'LOGOUT' })
    window.addEventListener('auth:logout', handleLogout)
    return () => window.removeEventListener('auth:logout', handleLogout)
  }, [])

  const login = async (email, password) => {
    const data = await api('/auth/login', {
      method: 'POST',
      body: { email, password },
    })
    setTokens(data.access_token, data.refresh_token)
    dispatch({ type: 'SET_USER', payload: data.user })
    return data.user
  }

  const register = async (fields) => {
    const data = await api('/auth/register', {
      method: 'POST',
      body: fields,
    })
    setTokens(data.access_token, data.refresh_token)
    dispatch({ type: 'SET_USER', payload: data.user })
    return data.user
  }

  const logout = () => {
    clearTokens()
    dispatch({ type: 'LOGOUT' })
  }

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout, fetchUser }}>
      {children}
    </AuthContext.Provider>
  )
}
