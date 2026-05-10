/* ==================== STREAK ==================== */
function getMoscowMidnight() {
  const now = new Date();
  const moscow = new Date(now.toLocaleString('en-US', { timeZone: 'Europe/Moscow' }));
  moscow.setHours(0, 0, 0, 0);
  return moscow.getTime();
}
function loadStreak() {
  try { const s = JSON.parse(localStorage.getItem('hd_streak') || '{}'); return { count: s.count || 0, lastDay: s.lastDay || 0 }; } catch { return { count: 0, lastDay: 0 }; }
}
function updateStreak() {
  const now = getMoscowMidnight();
  const s = loadStreak();
  const diff = now - s.lastDay;
  if (diff === 0) return s.count;
  const dayMs = 86400000;
  let newCount = diff <= dayMs + 5 * 60000 ? s.count + 1 : 1;
  localStorage.setItem('hd_streak', JSON.stringify({ count: newCount, lastDay: now }));
  return newCount;
}
