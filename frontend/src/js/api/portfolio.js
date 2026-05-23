const portfolioApi = {
  feed(params = {}) {
    return apiClient.get('/portfolio/feed', params);
  },
  create(formData) {
    return apiClient.post('/portfolio/', formData);
  },
  my() {
    return apiClient.get('/portfolio/my');
  },
  toggleLike(postId) {
    return apiClient.post(`/likes/${postId}`, {});
  },
};
