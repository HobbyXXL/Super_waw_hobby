/* Centralized HTTP client: Bearer token, 401 logout, error parsing */

function getToken() {
  try { return localStorage.getItem(TOKEN_KEY) || ''; } catch { return ''; }
}

function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

function getStoredLogin() {
  try { return localStorage.getItem(LOGIN_KEY) || ''; } catch { return ''; }
}

function setStoredLogin(login) {
  if (login) localStorage.setItem(LOGIN_KEY, login);
  else localStorage.removeItem(LOGIN_KEY);
}

function clearSession() {
  setToken('');
  setStoredLogin('');
}

function parseErrorDetail(data) {
  if (!data) return 'Ошибка запроса';
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail.map((e) => e.msg || e.message || JSON.stringify(e)).join('; ');
  }
  if (data.message) return data.message;
  return 'Ошибка запроса';
}

async function apiRequest(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }
  if (!(options.body instanceof FormData) && !headers['Content-Type'] && options.body) {
    headers['Content-Type'] = 'application/json';
  }
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    credentials: 'include',
  });
  if (res.status === 401) {
    clearSession();
    if (typeof window !== 'undefined' && window.__hobbyOnUnauthorized) {
      window.__hobbyOnUnauthorized();
    }
  }
  const text = await res.text();
  let data = null;
  if (text) {
    try { data = JSON.parse(text); } catch { data = { detail: text }; }
  }
  if (!res.ok) {
    const err = new Error(parseErrorDetail(data));
    err.status = res.status;
    err.data = data;
    throw err;
  }
  if (res.status === 204) return null;
  return data;
}

const apiClient = {
  get: (path, params) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : '';
    return apiRequest(path + qs, { method: 'GET' });
  },
  post: (path, body) => apiRequest(path, {
    method: 'POST',
    body: body instanceof FormData ? body : JSON.stringify(body ?? {}),
  }),
  put: (path, body) => apiRequest(path, { method: 'PUT', body: JSON.stringify(body ?? {}) }),
  patch: (path, body) => apiRequest(path, { method: 'PATCH', body: JSON.stringify(body ?? {}) }),
  delete: (path) => apiRequest(path, { method: 'DELETE' }),
  getToken,
  setToken,
  getStoredLogin,
  setStoredLogin,
  clearSession,
  getBaseUrl: () => API_BASE_URL,
};
