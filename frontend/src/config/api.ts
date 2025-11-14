/**
 * API Configuration
 * Centralized configuration for all API calls
 *
 * Environment Variables:
 * - VITE_API_URL: Backend API base URL (set in .env or Vercel env vars)
 *
 * Default behavior:
 * - Development: Uses VITE_API_URL or falls back to http://localhost:8000
 * - Production: MUST set VITE_API_URL in deployment platform (Vercel/Netlify)
 */

// Get API URL from environment variable or default to localhost
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// API endpoints base path
export const API_PATH = '/api';

// Full API URL (base + path)
export const API_URL = `${API_BASE_URL}${API_PATH}`;

// Debug logging - helps diagnose connection issues
console.log('🌐 API Configuration Loaded:', {
  VITE_API_URL: import.meta.env.VITE_API_URL,
  API_BASE_URL,
  API_URL,
  MODE: import.meta.env.MODE,
  DEV: import.meta.env.DEV,
  PROD: import.meta.env.PROD
});

// Helper to check if API is configured correctly
export const isApiConfigured = (): boolean => {
  const configured = !!import.meta.env.VITE_API_URL;
  if (!configured && import.meta.env.PROD) {
    console.warn('⚠️ WARNING: VITE_API_URL not set in production! Using default localhost.');
  }
  return configured;
};

// Log warning if in production without explicit API URL
if (import.meta.env.PROD && !import.meta.env.VITE_API_URL) {
  console.error('❌ PRODUCTION ERROR: VITE_API_URL environment variable is not set!');
  console.error('Set this in your deployment platform (Vercel/Netlify) environment variables.');
}

export default {
  API_BASE_URL,
  API_PATH,
  API_URL,
  isApiConfigured
};
