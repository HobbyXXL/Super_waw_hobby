/* ==================== CHAT DATA ==================== */
const initialChats = [
  { id: 1, userId: 1, messages: [
    { id: 1, from: 1, text: 'Привет! Как твои дела? 😊', time: '12:40', reaction: null },
    { id: 2, from: 'me', text: 'Отлично! Сегодня занимался хобби', time: '12:42', reaction: null },
    { id: 3, from: 1, text: 'Супер! Я тоже! Вязала весь вечер 🧶', time: '12:44', reaction: null },
    { id: 4, from: 'me', text: 'Как продвигается проект?', time: '12:45', reaction: null },
    { id: 5, from: 1, text: 'Хорошо! Уже на половине 🎉', time: '12:47', reaction: null },
  ], unread: 2, muted: false, pinned: false },
  { id: 2, userId: 3, messages: [
    { id: 1, from: 3, text: 'Запишись на мой мастер-класс!', time: 'вчера', reaction: null },
    { id: 2, from: 'me', text: 'Обязательно! Когда ближайший?', time: 'вчера', reaction: null },
  ], unread: 0, muted: false, pinned: true },
  { id: 3, userId: 5, messages: [
    { id: 1, from: 5, text: 'Видела новый ролик про хастл? Огонь!', time: 'пн', reaction: null },
  ], unread: 1, muted: true, pinned: false },
];
