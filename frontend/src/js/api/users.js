const usersApi = {
  me() {
    return apiClient.get('/users/me');
  },
  meExtended() {
    return apiClient.get('/users/me/extended');
  },
  updateProfile(data) {
    return apiClient.put('/users/me/profile', data);
  },
};
