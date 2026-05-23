const activitiesApi = {
  checkIn(hobbyId, date) {
    const body = { hobby_id: hobbyId };
    if (date) body.date = date;
    return apiClient.post('/activities/check-in', body);
  },
  stats(params = {}) {
    return apiClient.get('/activities/stats', params);
  },
};
