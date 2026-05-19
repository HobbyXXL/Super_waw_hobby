// api.js — централизованный API-клиент для ХОББИДРУГ
const BASE_URL = 'http://localhost:8000';

// Вспомогательная функция: добавляет токен к заголовкам
function authHeaders() {
  const token = localStorage.getItem('hd_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
}

// Базовый запрос
async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: authHeaders(),
    ...options
  });

  let data;
  try { data = await res.json(); } catch { data = {}; }

  if (!res.ok) {
    const err = new Error(data.detail || `HTTP ${res.status}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

// === AUTH ===
export const authAPI = {
  async register(email, password) {
    const data = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    localStorage.setItem('hd_token', data.access_token);
    return data.user;
  },
  async login(email, password) {
    const form = new URLSearchParams({ username: email, password });
    const res = await fetch(`${BASE_URL}/auth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Ошибка входа');
    localStorage.setItem('hd_token', data.access_token);
    return usersAPI.me();
  },
  logout() {
    localStorage.removeItem('hd_token');
  },
  async checkSession() {
    try {
      return await usersAPI.me();
    } catch {
      localStorage.removeItem('hd_token');
      return null;
    }
  }
};

// === USERS ===
export const usersAPI = {
  me() { return request('/users/me'); },
  updateMe(payload) {
    return request('/users/me', {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
  },
  async uploadAvatar(file) {
    const token = localStorage.getItem('hd_token');
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${BASE_URL}/users/me/avatar`, {
      method: 'POST',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      body: formData
    });
    if (!res.ok) throw new Error('Ошибка загрузки аватара');
    return res.json();
  }
};

// === POSTS ===
export const postsAPI = {
  feed(skip = 0, limit = 20) {
    return request(`/portfolio/?skip=${skip}&limit=${limit}`);
  },
  create(payload) {
    return request('/portfolio/', {
      method: 'POST',
      body: JSON.stringify(payload)
    });
  },
  like(postId) {
    return request(`/likes/${postId}`, { method: 'POST' });
  },
  unlike(postId) {
    return request(`/likes/${postId}`, { method: 'DELETE' });
  },
  addComment(postId, text) {
    return request(`/portfolio/${postId}/comments`, {
      method: 'POST',
      body: JSON.stringify({ text })
    });
  }
};

// === CHATS ===
export const chatsAPI = {
  list() { return request('/chats/'); },
  messages(chatId) { return request(`/chats/${chatId}/messages`); },
  sendMessage(chatId, text) {
    return request(`/chats/${chatId}/messages`, {
      method: 'POST',
      body: JSON.stringify({ text })
    });
  }
};

// === ONBOARDING ===
export const onboardingAPI = {
  complete(payload) {
    return request('/users/me/profile', {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
  }
};