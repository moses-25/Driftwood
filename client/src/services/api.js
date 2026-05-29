// API Base URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

// Helper function to handle API responses
const handleResponse = async (response) => {
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.error || data.message || 'Something went wrong');
  }
  
  return data;
};

// Helper function to make API requests
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };
  
  try {
    const response = await fetch(url, config);
    return await handleResponse(response);
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
};

// ============================================================================
// PRODUCTS API
// ============================================================================

export const getProducts = async (params = {}) => {
  const queryParams = new URLSearchParams();
  
  if (params.page) queryParams.append('page', params.page);
  if (params.per_page) queryParams.append('per_page', params.per_page);
  if (params.category_id) queryParams.append('category_id', params.category_id);
  if (params.search) queryParams.append('search', params.search);
  if (params.is_available !== undefined) queryParams.append('is_available', params.is_available);
  
  const query = queryParams.toString();
  const endpoint = `/api/products${query ? `?${query}` : ''}`;
  
  return apiRequest(endpoint);
};

export const getProductById = async (id) => {
  return apiRequest(`/api/products/${id}`);
};

export const searchProducts = async (query) => {
  return apiRequest(`/api/products/search?q=${encodeURIComponent(query)}`);
};

// ============================================================================
// CATEGORIES API
// ============================================================================

export const getCategories = async () => {
  return apiRequest('/api/categories');
};

export const getCategoryById = async (id) => {
  return apiRequest(`/api/categories/${id}`);
};

export const getProductsByCategory = async (categoryId) => {
  return apiRequest(`/api/categories/${categoryId}/products`);
};

// ============================================================================
// ORDERS API
// ============================================================================

export const createOrder = async (orderData) => {
  return apiRequest('/api/orders', {
    method: 'POST',
    body: JSON.stringify(orderData),
  });
};

export const getOrderById = async (id) => {
  return apiRequest(`/api/orders/${id}`);
};

export const trackOrder = async (orderNumber) => {
  return apiRequest(`/api/orders/${orderNumber}/track`);
};

export const getOrderTimeline = async (id) => {
  return apiRequest(`/api/orders/${id}/timeline`);
};

// ============================================================================
// PAYMENTS API
// ============================================================================

export const initiateMpesaPayment = async (paymentData) => {
  return apiRequest('/api/payments/mpesa/initiate', {
    method: 'POST',
    body: JSON.stringify(paymentData),
  });
};

export const getPaymentStatus = async (paymentId) => {
  return apiRequest(`/api/payments/${paymentId}`);
};

export const queryPaymentStatus = async (checkoutRequestId) => {
  return apiRequest(`/api/payments/query/${checkoutRequestId}`);
};

// ============================================================================
// AUTH API
// ============================================================================

export const register = async (userData) => {
  return apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};

export const login = async (credentials) => {
  return apiRequest('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  });
};

export const getCurrentUser = async (token) => {
  return apiRequest('/api/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const refreshToken = async (refreshToken) => {
  return apiRequest('/api/auth/refresh', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${refreshToken}`,
    },
  });
};

// ============================================================================
// CONTACT & NEWSLETTER API (if backend has these endpoints)
// ============================================================================

export const submitContactForm = async (formData) => {
  return apiRequest('/api/contact', {
    method: 'POST',
    body: JSON.stringify(formData),
  });
};

export const subscribeNewsletter = async (email) => {
  return apiRequest('/api/newsletter', {
    method: 'POST',
    body: JSON.stringify({ email }),
  });
};

// ============================================================================
// HEALTH CHECK
// ============================================================================

export const checkHealth = async () => {
  return apiRequest('/api/health');
};

export default {
  // Products
  getProducts,
  getProductById,
  searchProducts,
  
  // Categories
  getCategories,
  getCategoryById,
  getProductsByCategory,
  
  // Orders
  createOrder,
  getOrderById,
  trackOrder,
  getOrderTimeline,
  
  // Payments
  initiateMpesaPayment,
  getPaymentStatus,
  queryPaymentStatus,
  
  // Auth
  register,
  login,
  getCurrentUser,
  refreshToken,
  
  // Other
  submitContactForm,
  subscribeNewsletter,
  checkHealth,
};
