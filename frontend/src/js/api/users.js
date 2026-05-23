const usersApi = {
  me() {
    return apiClient.get('/users/me');
  },
  meExtended() {
    return apiClient.get('/users/me/extended');
  },
};
