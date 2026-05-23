const commentsApi = {
  getComments(postId) {
    return apiClient.get(`/posts/${postId}/comments`);
  },
  addComment(postId, body) {
    return apiClient.post(`/posts/${postId}/comments`, { body });
  },
};
