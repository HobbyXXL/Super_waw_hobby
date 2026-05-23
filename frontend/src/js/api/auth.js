const authApi = {
  register(email, login, password) {
    return apiClient.post('/auth/register', { email, login, password, role: 'user' });
  },
  verifyCode(email, code) {
    return apiClient.post('/auth/verify-code', { email, code });
  },
  login(login, password) {
    return apiClient.post('/auth/login', { login, password });
  },
  logout() {
    return apiClient.post('/auth/logout', {}).catch(() => null).finally(() => apiClient.clearSession());
  },
  completeProfile(profile) {
    return apiClient.post('/auth/complete-profile', profile);
  },
};
