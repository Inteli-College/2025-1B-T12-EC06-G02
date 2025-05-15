export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  SIGNUP: '/signup',
  FORGOT_PASSWORD: '/forgot-password',
  DASHBOARD: '/dashboard',
  PROJECTS: '/projects',
  IMAGES: '/images',
  RESULTS: '/results',
  REPORTS: '/reports',
  PROFILE: '/profile'
}

export const API_ROUTES = {
  PROJECTS: '/api/projects',
  IMAGES: '/api/images',
  RESULTS: '/api/results',
  REPORTS: '/api/reports',
  USERS: '/api/users'
}

export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  USER_DATA: 'user_data',
  THEME: 'theme_preference'
}

export const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
export const ALLOWED_REPORT_TYPES = ['application/pdf']
