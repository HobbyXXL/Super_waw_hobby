const BASE_URL = 'http://127.0.0.1:8000';

function authHeaders() {
  const token = localStorage.getItem('hd_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
}

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

export const authAPI = {
  async register(loginValue, emailValue, passwordValue) {
    const bodyData = {
      login: loginValue,
      email: emailValue,
      password: passwordValue
    };
    console.log("🚀 ОТПРАВКА РЕГИСТРАЦИИ:", bodyData);
    const data = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(bodyData)
    });
    if (data && data.access_token) localStorage.setItem('hd_token', data.access_token);
    return data;
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
    return data;
  },
  logout() { localStorage.removeItem('hd_token'); },
  async checkSession() {
    try { return await request('/users/me'); }
    catch { localStorage.removeItem('hd_token'); return null; }
  }
};

export const usersAPI = {
  me() { return request('/users/me'); },
  updateMe(payload) { return request('/users/me/profile', { method: 'PUT', body: JSON.stringify(payload) }); }
};

export const postsAPI = {
  feed(skip = 0, limit = 20) { return request(`/portfolio/?skip=${skip}&limit=${limit}`); },
  create(payload) { return request('/portfolio/', { method: 'POST', body: JSON.stringify(payload) }); },
  like(postId) { return request(`/likes/${postId}`, { method: 'POST' }); },
  unlike(postId) { return request(`/likes/${postId}`, { method: 'DELETE' }); }
};

export const chatsAPI = {
  list() { return request('/chats/'); },
  messages(chatId) { return request(`/chats/${chatId}/messages`); },
  sendMessage(chatId, text) { return request(`/chats/${chatId}/messages`, { method: 'POST', body: JSON.stringify({ text }) }); }
};