/* API base URL — override via window.HOBBY_API_URL before scripts load */
const API_BASE_URL = (typeof window !== 'undefined' && window.HOBBY_API_URL)
  || 'http://localhost:8000';

const TOKEN_KEY = 'hd_access_token';
const LOGIN_KEY = 'hd_login';
