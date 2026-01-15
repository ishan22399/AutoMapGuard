import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000, // 30 seconds
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Don't redirect on auth errors - let components handle it
    if (error.response?.status === 401) {
      console.warn('Authentication required');
    }
    return Promise.reject(error);
  }
);

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('token', token);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  }
};

export const apiService = {
  // Change Detection
  detectChanges: (simulate = true) => api.post('/changes/detect', { simulate }),
  listChanges: (status = null) => api.get('/changes/list', { params: { status } }),
  
  // Geometry Validation
  validateGeometry: (geometry) => api.post('/geometry/validate', { geometry }),
  
  // Review Queue
  getReviewQueue: (status = 'pending') => api.get('/review-queue', { params: { status } }),
  submitReview: (review_id, decision, notes = null) => api.post('/review-queue/decide', { review_id, decision, notes }),
  
  // Building Footprints
  listFootprints: (limit = 100) => api.get('/footprints/list', { params: { limit } }),
  commitFootprint: (footprint) => api.post('/footprints/commit', footprint),
  
  // Dashboard
  getDashboardStats: () => api.get('/dashboard/stats'),
};
