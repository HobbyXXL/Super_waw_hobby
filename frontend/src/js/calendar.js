/* ==================== CALENDAR ==================== */
function getCalendarData() {
  const now = new Date();
  const year = now.getFullYear(), month = now.getMonth(), today = now.getDate();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const dayOfWeek = now.getDay();
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  const weekDays = [];
  for (let i = 0; i < 7; i++) {
    const d = today + mondayOffset + i;
    weekDays.push(d >= 1 && d <= daysInMonth ? d : null);
  }
  return { today, month, year, weekDays, daysInMonth };
}
function loadVisitedDays(year, month) {
  try { return JSON.parse(localStorage.getItem('hd_visited_'+year+'_'+month) || '[]'); } catch { return []; }
}
function saveVisitedDay(year, month, day) {
  try {
    const key = 'hd_visited_'+year+'_'+month;
    const arr = JSON.parse(localStorage.getItem(key) || '[]');
    if (!arr.includes(day)) { arr.push(day); localStorage.setItem(key, JSON.stringify(arr)); }
  } catch {}
}
