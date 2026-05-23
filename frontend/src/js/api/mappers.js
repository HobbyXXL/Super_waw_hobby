/* Map backend DTOs to UI post/user shapes */

const LEVEL_TO_API = {
  'Новичок': 'beginner',
  'Любитель': 'intermediate',
  'Профи': 'advanced',
  'Продолжительный': 'advanced',
};

const API_TO_LEVEL = {
  beginner: 'Новичок',
  intermediate: 'Любитель',
  advanced: 'Профи',
};

function formatRelativeTime(isoDate) {
  if (!isoDate) return '';
  const d = new Date(isoDate);
  const diff = Date.now() - d.getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'только что';
  if (mins < 60) return `${mins} минут назад`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs} час${hrs > 1 && hrs < 5 ? 'а' : hrs >= 5 ? 'ов' : ''} назад`;
  const days = Math.floor(hrs / 24);
  if (days === 1) return 'вчера';
  return `${days} дней назад`;
}

function imageUrl(path) {
  if (!path) return null;
  if (path.startsWith('http') || path.startsWith('data:')) return path;
  return apiClient.getBaseUrl() + path;
}

function mapFeedPost(item, fallbackAvatar) {
  const authorLogin = item.author?.login || 'Пользователь';
  return {
    id: item.id,
    authorId: item.author?.id,
    author: authorLogin,
    avatar: fallbackAvatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(authorLogin)}&background=FFD166&color=3B2510`,
    time: formatRelativeTime(item.created_at),
    badge: item.activity_status === 'did_hobby' ? 'Занимался хобби' : 'Новый пост',
    hobbyDone: item.activity_status === 'did_hobby',
    streak: 0,
    title: item.title,
    text: item.description || '',
    img: imageUrl(item.file_url),
    tags: item.hobby_id ? [`#hobby${item.hobby_id}`] : [],
    likes: item.likes_count || 0,
    liked: !!item.liked,
    comments: [],
    shares: 0,
    expanded: false,
    _fromApi: true,
  };
}

const UI_TO_API_HOBBY = {
  drawing: 'рисование',
  knitting: 'вязание',
  running: 'бег',
  gardening: 'садоводство',
  dancing: 'танцы',
  cooking: 'кулинария',
  sculpting: 'лепка',
  photography: 'фотография',
  music: 'музыка',
  instruments: 'гитара',
  reading: 'чтение',
  sport: 'спорт',
};

function findHobbyIdByUiId(uiHobbyId, apiHobbies, uiHobbies) {
  if (!apiHobbies?.length) return null;
  if (typeof uiHobbyId === 'number') return uiHobbyId;
  const ui = uiHobbies.find((h) => h.id === uiHobbyId);
  const key = (UI_TO_API_HOBBY[uiHobbyId] || ui?.name || '').toLowerCase();
  const match = apiHobbies.find((h) => {
    const n = h.name.toLowerCase();
    return n.includes(key) || key.includes(n.slice(0, 5));
  });
  return match?.id ?? apiHobbies[0]?.id;
}

function buildProfilePayload(selectedUiIds, hobbyLevelsMap, goalsText, apiHobbies, uiHobbies) {
  const hobbies = selectedUiIds.slice(0, 5).map((uiId) => {
    const hobbyId = findHobbyIdByUiId(uiId, apiHobbies, uiHobbies);
    const levelLabel = hobbyLevelsMap[uiId] || 'Новичок';
    return {
      hobby_id: hobbyId,
      experience_level: LEVEL_TO_API[levelLabel] || 'beginner',
      frequency_per_week: 2,
      is_public: true,
    };
  }).filter((h) => h.hobby_id);
  const goalLines = (goalsText || '').split('\n').map((s) => s.trim()).filter(Boolean).slice(0, 4);
  const goals = goalLines.map((line, i) => ({
    type: ['learn', 'create', 'relax'][i % 3],
    title: line.length >= 10 ? line.slice(0, 200) : `${line} — моя цель в Hobby Friend`,
    description: line.length >= 20 ? line : `${line}. Хочу достичь этого через регулярную практику и поддержку сообщества.`,
    is_public: true,
  }));
  if (!goals.length) {
    goals.push({
      type: 'learn',
      title: 'Развивать своё хобби каждый день',
      description: 'Регулярно заниматься выбранным хобби и отслеживать прогресс в приложении.',
      is_public: true,
    });
  }
  return { hobbies, goals, looking_for: 'Единомышленников и поддержку' };
}
