// app.js — основной клиентский скрипт для Super_WAW_HOBBY

// --- 1. Глобальные утилиты (остаются как есть)
function formatDateRelative(dateStr) {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return "только что";
  if (diffMins < 60) return `${diffMins} мин назад`;
  if (diffHours < 24) return `${diffHours} ч назад`;
  if (diffDays < 7) return `${diffDays} дн назад`;
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
}

function getNickFromEmail(email) {
  if (!email) return 'Гость';
  return email.split('@')[0].replace(/[^a-zA-Zа-яА-Я0-9_]/g, '') || 'Гость';
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.trim());
}

// --- 2. Основное приложение (App)
const App = {
  setup() {
    // --- Состояние приложения
    const page = ref('auth');
    const authMode = ref('register');
    const email = ref('');
    const password = ref('');
    const authError = ref('');
    const emailError = ref(false);
    const pwError = ref(false);
    const toast = ref('');
    let toastTimer = null;

    const navPage = ref('feed');
    const viewingUserId = ref(null);

    // --- Onboarding
    const selectedHobbies = ref([]);
    const hobbyLevels = ref({});
    const goalsText = ref('');
    const addedFriends = ref([]);
    const friendsTab = ref('Все');
    const hobbySearch = ref('');
    const onboardingValidationMsg = ref('');

    // --- Пользователь
    const currentUser = reactive({
      id: null,
      name: 'Гость',
      avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=100',
      streak: 1,
      hobbies: [],
      hobbyLevels: {},
      goals: '',
      friends: [],
      bio: 'Люблю хобби и новых друзей! ⭐',
      isVerified: false,
    });

    const isGuest = ref(true);
    const userStats = reactive({ posts: 0, likesGiven: 0, comments: 0, readingHours: 0, friends: 0 });

    // --- Календарь (упрощённо)
    const calData = ref({
      year: new Date().getFullYear(),
      month: new Date().getMonth() + 1,
      today: new Date().getDate(),
      weekDays: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    });
    const visitedDays = ref([new Date().getDate()]);

    function markTodayVisited() {
      const d = new Date();
      const day = d.getDate();
      if (!visitedDays.value.includes(day)) {
        visitedDays.value.push(day);
        localStorage.setItem(`visited_${d.getFullYear()}_${d.getMonth()+1}`, '1');
      }
    }

    // --- Настройки
    const currentTheme = ref(localStorage.getItem('hd_theme') || 'light');
    const soundsEnabled = ref(localStorage.getItem('hd_sound') !== 'false');
    const currentLang = ref(localStorage.getItem('hd_lang') || 'ru');

    function setLang(code) {
      currentLang.value = code;
      localStorage.setItem('hd_lang', code);
    }

    const settingNewName = ref('');
    const settingNewBio = ref('');

    function applyTheme(t) {
      document.body.classList.toggle('dark', t === 'dark');
      localStorage.setItem('hd_theme', t);
    }

    watch(currentTheme, applyTheme, { immediate: true });
    watch(soundsEnabled, v => localStorage.setItem('hd_sound', v ? 'true' : 'false'));

    function playSoundIfEnabled(type) {
      if (soundsEnabled.value && type === 'success') console.log('🎵 Success sound');
    }

    function showToast(msg) {
      toast.value = msg;
      if (toastTimer) clearTimeout(toastTimer);
      toastTimer = setTimeout(() => { toast.value = ''; }, 3000);
    }

    // --- Feed posts (теперь пусто — данные приходят из API)
    const allPosts = ref([]);
    const myPosts = ref([]);
    const likedPosts = computed(() => allPosts.value.filter(p => p.liked));
    const likedNotifCount = ref(0);
    const openComments = ref({});
    const commentInputs = ref({});
    const showScrollTop = ref(false);
    const loadingMore = ref(false);

    // --- Поиск
    const searchQuery = ref('');
    const searchOpen = ref(false);
    const showSearchResults = ref(false);

    const searchResults = computed(() => {
      const q = searchQuery.value.toLowerCase().trim();
      if (!q) return { posts: [], users: [] };
      return {
        posts: allPosts.value.filter(p =>
          p.title.toLowerCase().includes(q) ||
          p.description?.toLowerCase().includes(q) ||
          p.tags?.some(t => t.toLowerCase().includes(q))
        ),
        users: [] // будет заполнено из API
      };
    });

    const sortedPosts = computed(() => {
      const hobbyNames = currentUser.hobbies.map(h => h.name?.toLowerCase() || '');
      if (!hobbyNames.length) return allPosts.value;
      return [...allPosts.value].sort((a, b) => {
        const aR = a.tags?.some(t => hobbyNames.some(h => t.toLowerCase().includes(h))) ? 1 : 0;
        const bR = b.tags?.some(t => hobbyNames.some(h => t.toLowerCase().includes(h))) ? 1 : 0;
        return bR - aR;
      });
    });

    // --- Чаты
    const chats = ref([]);
    const activeChatId = ref(null);
    const chatInput = ref('');
    const chatSearch = ref('');
    const activeReactionMsgId = ref(null);
    const showTyping = ref(false);
    const REACTIONS = ['❤️','😂','😮','👍','🔥','🎉'];

    const activeChat = computed(() => chats.value.find(c => c.id === activeChatId.value));
    const activeChatUser = computed(() => activeChat.value ?
      chats.value.find(u => u.id === activeChat.value.userId) : null);

    const totalChatUnread = computed(() =>
      chats.value.filter(c => !c.muted).reduce((s, c) => s + (c.unread || 0), 0)
    );

    // --- Создание поста
    const showCreatePost = ref(false);
    const newPostTitle = ref('');
    const newPostText = ref('');
    const newPostTags = ref([]);
    const newPostTagInput = ref('');
    const newPostHobbyDone = ref(false);
    const newPostImage = ref(null);
    const postValidation = ref('');

    // --- Вспомогательные функции
    function getScroller() {
      return document.getElementById('mainScroll') || document.body;
    }

    function scrollToTop() {
      getScroller().scrollTo({ top: 0, behavior: 'smooth' });
    }

    // --- Аутентификация (теперь через api.js)
    async function submitAuth() {
      authError.value = ''; emailError.value = false; pwError.value = false;
      const em = email.value.trim(), pw = password.value;
      if (!em) { authError.value = 'Введите электронную почту'; emailError.value = true; return; }
      if (!isValidEmail(em)) { authError.value = 'Введите корректный email'; emailError.value = true; return; }
      if (!pw) { authError.value = 'Введите пароль'; pwError.value = true; return; }
      if (pw.length < 6) { authError.value = 'Пароль минимум 6 символов'; pwError.value = true; return; }
      if (/\s/.test(pw)) { authError.value = 'Пароль не должен содержать пробелы'; pwError.value = true; return; }

      try {
        if (authMode.value === 'login') {
          // Вызов через api.js
          const userData = await window.api.authAPI.login(em, pw);
          Object.assign(currentUser, userData);
          isGuest.value = false;
          page.value = 'feed';
          navPage.value = 'feed';
          markTodayVisited();
          showToast('🔥 Добро пожаловать обратно!');
        } else {
          // Регистрация — шаг 1: отправка кода (через api.js)
          const userData = await window.api.authAPI.register(login, em, pw);
          currentUser.name = getNickFromEmail(em);
          currentUser.email = em;
          isGuest.value = false;
          page.value = 'onboarding-hobbies';
          showToast('📧 Код подтверждения отправлен на ' + em);
        }
      } catch (err) {
        authError.value = err.message || 'Сервер недоступен';
        playSoundIfEnabled('error');
      }
    }

    function skipToFeed() {
      currentUser.name = 'Гость';
      currentUser.streak = 1;
      isGuest.value = true;
      page.value = 'feed';
      navPage.value = 'feed';
      showToast('👀 Просмотр без авторизации');
    }

    // --- Onboarding (теперь через api.js)
    async function nextOnboarding() {
      onboardingValidationMsg.value = '';
      if (page.value === 'onboarding-hobbies') {
        if (!selectedHobbies.value.length) {
          onboardingValidationMsg.value = 'Выберите хотя бы одно хобби';
          return;
        }
        playSoundIfEnabled('success');
        page.value = 'onboarding-levels';
      } else if (page.value === 'onboarding-levels') {
        const missing = selectedHobbies.value.filter(id => !hobbyLevels.value[id]);
        if (missing.length) {
          onboardingValidationMsg.value = 'Выберите уровень для каждого хобби';
          return;
        }
        playSoundIfEnabled('success');
        page.value = 'onboarding-goals';
      } else if (page.value === 'onboarding-goals') {
        if (!goalsText.value.trim()) {
          onboardingValidationMsg.value = 'Напишите хотя бы одну цель';
          return;
        }
        playSoundIfEnabled('success');
        page.value = 'onboarding-summary';
      } else if (page.value === 'onboarding-summary') {
        playSoundIfEnabled('success');
        page.value = 'onboarding-friends';
      } else if (page.value === 'onboarding-friends') {
        // Шаг 4: сохраняем профиль через API (через api.js)
        try {
          const profileData = {
            hobbies: selectedHobbies.value.map(id => ({
              hobby_id: id,
              experience_level: hobbyLevels.value[id] || 'Новичок',
              frequency_per_week: 2,
              frequency_per_month: 8,
              experience_description: '',
              why_this_hobby: '',
              looking_for_in_partner: '',
              is_public: true
            })),
            goals: goalsText.value.split('\n').filter(g => g.trim()).map(g => ({
              type: 'general',
              title: g,
              description: '',
              target_date: null,
              why_goal: '',
              is_public: true
            })),
            looking_for: 'друзей и вдохновения'
          };

          // Вызов через api.js
          const updatedUser = await window.api.onboardingAPI.complete(profileData);

          // Обновляем локальный профиль
          currentUser.hobbies = selectedHobbies.value.map(id => ({
            id,
            name: `Хобби ${id}`,
            level: hobbyLevels.value[id] || 'Новичок'
          }));
          currentUser.goals = goalsText.value.split('\n').filter(g => g.trim());
          currentUser.friends = [...addedFriends.value];
          userStats.friends = addedFriends.value.length;

          page.value = 'feed';
          navPage.value = 'feed';
          showToast('🎉 Добро пожаловать в ХОББИДРУГ!');
        } catch (err) {
          onboardingValidationMsg.value = 'Ошибка сохранения: ' + err.message;
        }
      }
    }

    function prevOnboarding() {
      const steps = ['onboarding-hobbies','onboarding-levels','onboarding-goals','onboarding-summary','onboarding-friends'];
      const i = steps.indexOf(page.value);
      if (i > 0) page.value = steps[i - 1];
    }

    // --- Feed actions (теперь через api.js)
    async function likePost(post) {
      if (isGuest.value) { showToast('Войдите, чтобы ставить лайки'); return; }
      try {
        // Вызов через api.js
        const response = await window.api.postsAPI.like(post.id);
        // Оптимистичное обновление
        post.liked = !post.liked;
        post.likes += post.liked ? 1 : -1;
        if (post.liked) {
          userStats.likesGiven++;
          likedNotifCount.value++;
          playSoundIfEnabled('like');
        } else {
          userStats.likesGiven = Math.max(0, userStats.likesGiven - 1);
          likedNotifCount.value = Math.max(0, likedNotifCount.value - 1);
        }
      } catch (err) {
        showToast('Ошибка: ' + err.message);
      }
    }

    function toggleComments(postId) {
      openComments.value = { ...openComments.value, [postId]: !openComments.value[postId] };
    }

    async function sendComment(post) {
      if (isGuest.value) { showToast('Войдите, чтобы комментировать'); return; }
      const text = (commentInputs.value[post.id] || '').trim();
      if (!text) return;
      try {
        // Вызов через api.js
        const comment = await window.api.postsAPI.addComment(post.id, text);
        post.comments = [...(post.comments || []), {
          author: currentUser.name,
          text,
          time: 'только что',
          id: Date.now()
        }];
        commentInputs.value = { ...commentInputs.value, [post.id]: '' };
        userStats.comments++;
        playSoundIfEnabled('select');
      } catch (err) {
        showToast('Ошибка: ' + err.message);
      }
    }

    // --- Загрузка постов (теперь через api.js)
    async function loadFeed() {
      try {
        // Вызов через api.js
        const myPostsData = await window.api.postsAPI.my();
        myPosts.value = myPostsData;

        const allPostsData = await window.api.postsAPI.feed();
        allPosts.value = allPostsData.map(p => ({
          ...p,
          time: formatDateRelative(p.created_at),
          liked: false, // будет обновлено позже
          expanded: false
        }));

        // Загружаем лайки
        const likedIds = await window.api.postsAPI.myLiked();
        allPosts.value.forEach(p => {
          p.liked = likedIds.some(id => id === p.id);
        });

        userStats.posts = myPosts.value.length;
        showToast('✨ Лента загружена');
      } catch (err) {
        console.error('Ошибка загрузки ленты:', err);
        showToast('Не удалось загрузить ленту');
      }
    }

    // --- Вспомогательные
    function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;
    }

    // --- Инициализация
    onMounted(() => {
      // Автоматическая загрузка ленты при входе
      if (!isGuest.value) {
        loadFeed();
      }

      // Обработчик прокрутки
      const scroller = getScroller();
      const handleScroll = () => {
        showScrollTop.value = scroller.scrollTop > 400;
      };
      scroller.addEventListener('scroll', handleScroll);

      // Мониторинг активности
      setInterval(() => {
        userStats.readingHours += 1/3600;
      }, 1000);

      // Проверка гостевого режима
      if (window.location.hash === '#guest') {
        skipToFeed();
      }
    });

    // --- Экспорт методов
    return {
      // State
      page, authMode, email, password, authError, emailError, pwError, toast,
      navPage, viewingUserId,
      selectedHobbies, hobbyLevels, goalsText, addedFriends, friendsTab, hobbySearch, onboardingValidationMsg,
      currentUser, isGuest, userStats,
      calData, visitedDays,
      allPosts, myPosts, likedPosts, likedNotifCount, openComments, commentInputs,
      showScrollTop, loadingMore, sortedPosts,
      searchQuery, searchOpen, showSearchResults, searchResults,
      chats, activeChatId, activeChat, activeChatUser, totalChatUnread,
      chatInput, chatSearch, activeReactionMsgId, showTyping, REACTIONS,
      showCreatePost, newPostTitle, newPostText, newPostTags, newPostTagInput,
      newPostHobbyDone, newPostImage, postValidation,

      // Methods
      showToast,
      submitAuth,
      skipToFeed,
      toggleHobby,
      setLevel,
      addGoalHint,
      toggleFriend,
      nextOnboarding,
      prevOnboarding,
      likePost,
      toggleComments,
      sendComment,
      loadFeed,
      scrollToTop,
      getScroller,
      formatDateRelative,
      getCookie,

      // Computed
      onboardingStep: computed(() => {
        const m = { 'onboarding-hobbies':1,'onboarding-levels':2,'onboarding-goals':3,'onboarding-summary':4,'onboarding-friends':5 };
        return m[page.value] || 0;
      }),
      filteredHobbies: computed(() => {
        // Здесь можно подгружать из /hobbies/ при необходимости
        return [];
      }),
      friendsTabs2: computed(() => {
        const tabs = ['Все'];
        selectedHobbies.value.forEach(id => {
          tabs.push(`Хобби ${id}`);
        });
        tabs.push('Новички');
        return tabs;
      }),
      filteredFriends: computed(() => []),
      sidebarSteps: [
        { label: 'Ваши хобби', sub: 'выберите свои хобби' },
        { label: 'Уровень', sub: 'выберите свой уровень' },
        { label: 'Ваши цели', sub: 'напишите, чего хотите достичь' },
        { label: 'Готово!', sub: '' },
        { label: 'Поиск друзей', sub: 'найдите новых друзей' },
      ],
      onboardingBgImages: {
        'onboarding-hobbies': 'https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=1200',
        'onboarding-levels': 'https://images.unsplash.com/photo-1513593771513-7b58b6c4af38?w=1200',
        'onboarding-goals': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200',
        'onboarding-summary': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200',
        'onboarding-friends': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1200',
      },

      // Settings
      currentTheme, soundsEnabled, currentLang, setLang,
      settingNewName, settingNewBio,
      applyTheme,
      saveName() {
        if (!settingNewName.value.trim()) return;
        currentUser.name = settingNewName.value.trim();
        settingNewName.value = '';
        showToast('✅ Имя изменено!');
      },
      saveBio() {
        currentUser.bio = settingNewBio.value || currentUser.bio;
        settingNewBio.value = '';
        showToast('✅ О себе обновлено!');
      },
      handleAvatarChange(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = ev => {
          currentUser.avatar = ev.target.result;
          showToast('📸 Аватар обновлён!');
        };
        reader.readAsDataURL(file);
      },

      // Chat
      openChatWith(userId) {
        if (isGuest.value) { showToast('Войдите, чтобы писать сообщения'); return; }
        let chat = chats.value.find(c => c.userId === userId);
        if (!chat) {
          chat = { id: Date.now(), userId, messages: [], unread: 0, muted: false, pinned: false };
          chats.value.unshift(chat);
        }
        activeChatId.value = chat.id;
        chat.unread = 0;
        navPage.value = 'chats';
        nextTick(() => {
          const el = document.getElementById('chat-msgs');
          if (el) el.scrollTop = el.scrollHeight;
        });
      },
      sendChatMessage() {
        if (!chatInput.value.trim() || !activeChat.value) return;
        const msg = {
          id: Date.now(),
          from: 'me',
          text: chatInput.value.trim(),
          time: new Date().toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }),
          reaction: null
        };
        activeChat.value.messages.push(msg);
        chatInput.value = '';
        nextTick(() => {
          const el = document.getElementById('chat-msgs');
          if (el) el.scrollTop = el.scrollHeight;
        });
        playSoundIfEnabled('msg');
        showTyping.value = true;
        setTimeout(() => {
          showTyping.value = false;
          const replies = ['Интересно! 😊','Расскажи подробнее 🙌','Отлично! 🔥','Согласна!','Да, конечно! ✨','Понял(а) тебя 👍','Здорово!','Продолжай, я слушаю 😄'];
          const reply = {
            id: Date.now() + 1,
            from: activeChat.value.userId,
            text: replies[Math.floor(Math.random() * replies.length)],
            time: new Date().toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }),
            reaction: null
          };
          activeChat.value.messages.push(reply);
          nextTick(() => {
            const el = document.getElementById('chat-msgs');
            if (el) el.scrollTop = el.scrollHeight;
          });
          playSoundIfEnabled('notify');
        }, 1200 + Math.random() * 800);
      },
      setReaction(msgId, emoji) {
        if (!activeChat.value) return;
        const msg = activeChat.value.messages.find(m => m.id === msgId);
        if (msg) msg.reaction = msg.reaction === emoji ? null : emoji;
        activeReactionMsgId.value = null;
        playSoundIfEnabled('select');
      },
      deleteChatItem() {
        chats.value = chats.value.filter(c => c.id !== activeChatId.value);
        activeChatId.value = null;
        showToast('🗑️ Чат удалён');
      },
      toggleMuteChat() {
        if (!activeChat.value) return;
        activeChat.value.muted = !activeChat.value.muted;
        showToast(activeChat.value.muted ? '🔕 Уведомления отключены' : '🔔 Уведомления включены');
      },
      togglePinChat() {
        if (!activeChat.value) return;
        activeChat.value.pinned = !activeChat.value.pinned;
        showToast(activeChat.value.pinned ? '📌 Чат закреплён' : '📌 Чат откреплён');
      },

      // Create post
      addTagFromInput() {
        const t = newPostTagInput.value.trim();
        if (!t) return;
        const tag = t.startsWith('#') ? t : '#' + t;
        if (!newPostTags.value.includes(tag)) newPostTags.value.push(tag);
        newPostTagInput.value = '';
      },
      addSuggestedTag(tag) {
        if (!newPostTags.value.includes(tag)) newPostTags.value.push(tag);
      },
      removeTag(tag) {
        newPostTags.value = newPostTags.value.filter(t => t !== tag);
      },
      handleImageUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = ev => { newPostImage.value = ev.target.result; };
        reader.readAsDataURL(file);
      },
      async submitPost() {
        if (isGuest.value) { showToast('Войдите, чтобы публиковать посты'); return; }
        postValidation.value = '';
        if (!newPostTitle.value.trim()) { postValidation.value = 'Введите заголовок'; return; }
        if (!newPostText.value.trim()) { postValidation.value = 'Напишите текст поста'; return; }

        try {
          // Вызов через api.js
          const newPost = await window.api.postsAPI.create({
            title: newPostTitle.value,
            description: newPostText.value,
            tags: newPostTags.value,
            visibility: 'public',
            activity_status: newPostHobbyDone.value ? 'did_hobby' : 'new',
            file_url: newPostImage.value
          });

          // Добавляем в локальный список
          const post = {
            id: newPost.id,
            authorId: 'me',
            author: currentUser.name,
            avatar: currentUser.avatar,
            time: 'только что',
            badge: newPostHobbyDone.value ? 'Занимался хобби' : 'Новый пост',
            hobbyDone: newPostHobbyDone.value,
            streak: currentUser.streak,
            title: newPost.title,
            description: newPost.description,
            file_url: newPost.file_url,
            tags: newPost.tags || [],
            likes: 0,
            liked: false,
            comments: [],
            shares: 0,
            expanded: false
          };
          allPosts.value.unshift(post);
          myPosts.value.unshift(post);
          userStats.posts++;
          showToast('🎉 Пост опубликован!');
          showCreatePost.value = false;
          newPostTitle.value = '';
          newPostText.value = '';
          newPostTags.value = [];
          newPostTagInput.value = '';
          newPostHobbyDone.value = false;
          newPostImage.value = null;
        } catch (err) {
          postValidation.value = 'Ошибка: ' + err.message;
        }
      },

      // Navigation
      goToUser(id) {
        if (!id || id === 'me') { navPage.value = 'profile'; return; }
        if (isGuest.value) { showToast('Войдите, чтобы просматривать профили'); return; }
        viewingUserId.value = id;
        navPage.value = 'other-user';
      },
      addFriendFromPage(userId) {
        if (isGuest.value) { showToast('Войдите, чтобы добавлять друзей'); return; }
        if (!currentUser.friends.includes(userId)) {
          currentUser.friends.push(userId);
          userStats.friends++;
          showToast('🎉 Друг добавлен!');
        } else {
          showToast('Уже в друзьях!');
        }
      },

      // Helper
      tr: { /* будет заполнено при локализации */ }
    };
  },
  template: `
    <!-- TOAST -->
    <div v-if="toast" class="toast-notification">{{ toast }}</div>

    <!-- ============ AUTH ============ -->
    <div v-if="page==='auth'" style="position:relative;min-height:100vh">
      <div class="bg-watercolor"></div>
      <button class="auth-skip-btn" @click="skipToFeed">👀 Смотреть без входа</button>
      <div class="auth-page">
        <div class="auth-logo-area">
          <div class="logo-icon" style="margin:0 auto"><span style="font-size:36px">⭐</span></div>
          <div class="auth-title">ХОББИ ДРУГ</div>
          <div class="auth-subtitle">сервис для помощи в вашем хобби</div>
        </div>
        <div class="auth-card">
          <div class="auth-card-title">{{ authMode==='login' ? '👋 Добро пожаловать!' : '🌟 Создание аккаунта' }}</div>
          <div class="form-group">
            <label class="form-label">Электронная почта:</label>
            <div class="form-input-wrap" :class="{error:emailError}">
              <span class="icon">✉️</span>
              <input class="form-input" v-model="email" @keyup.enter="submitAuth" @input="emailError=false" type="text" placeholder="email@example.com"/>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Пароль:</label>
            <div class="form-input-wrap" :class="{error:pwError}">
              <span class="icon">🔒</span>
              <input class="form-input" v-model="password" @keyup.enter="submitAuth" @input="pwError=false" type="password" placeholder="Минимум 6 символов, без пробелов"/>
            </div>
            <div v-if="authMode==='register'" style="font-size:12px;color:var(--gray-text);margin-top:5px;padding-left:2px">Минимум 6 символов. Пробелы не допускаются.</div>
          </div>
          <div v-if="authError" class="error-msg">⚠️ {{ authError }}</div>
          <div class="auth-footer">
            <div v-if="authMode==='register'" style="font-size:15px;color:var(--brown-dark);font-weight:500">
              Есть аккаунт? <span class="auth-link" @click="authMode='login'">Войти</span>
            </div>
            <div v-else style="font-size:15px;color:var(--brown-dark);font-weight:500">
              Нет аккаунта? <span class="auth-link" @click="authMode='register'">Регистрация</span>
            </div>
            <button class="btn-primary" @click="submitAuth">{{ authMode==='login' ? 'Войти' : 'Регистрация' }}</button>
          </div>
        </div>
        <div style="margin-top:20px;text-align:center;color:rgba(92,61,30,.6);font-size:13px">Тестовый аккаунт: test@mail.ru / testtest</div>
      </div>
    </div>

    <!-- ============ ONBOARDING ============ -->
    <div v-if="['onboarding-hobbies','onboarding-levels','onboarding-goals','onboarding-summary','onboarding-friends'].includes(page)" class="onboarding-page">
      <div class="onboarding-sidebar">
        <div class="sidebar-welcome-title">Давайте познакомимся!</div>
        <div class="sidebar-welcome-desc">Расскажите немного о своих хобби...</div>
        <div v-for="(step,i) in sidebarSteps" :key="i" class="sidebar-step">
          <div class="step-num" :class="onboardingStep>i+1?'done':onboardingStep===i+1?'active':'pending'">{{ onboardingStep>i+1?'✓':i+1 }}</div>
          <div class="step-info">
            <div class="step-label">{{ step.label }}</div>
            <div class="step-sub">{{ step.sub }}</div>
          </div>
        </div>
      </div>
      <div class="onboarding-main">
        <div class="onboarding-bg" :style="'background-image:url('+onboardingBgImages[page]+')'"></div>
        <div class="onboarding-content">
          <div v-if="page==='onboarding-hobbies'" class="onboarding-card">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:24px">
              <div><div style="font-size:14px;font-weight:600;color:var(--gray-text);margin-bottom:4px">Шаг 1 из 5:</div><div style="font-size:22px;font-weight:800;color:var(--brown-dark)">Выберите ваши хобби</div></div>
              <div class="hobby-search-bar"><span style="color:#bbb">🔍</span><input v-model="hobbySearch" placeholder="поиск хобби"/></div>
            </div>
            <div class="hobby-grid">
              <div v-for="id in [1,2,3,4,5]" :key="id" class="hobby-chip" :class="{selected:selectedHobbies.includes(id)}" @click="toggleHobby(id)">
                <span>🎨</span><span>Хобби {{ id }}</span>
                <span v-if="selectedHobbies.includes(id)" style="position:absolute;top:6px;right:8px;font-size:12px">✓</span>
              </div>
            </div>
            <div style="display:flex;align-items:center;justify-content:space-between">
              <div style="display:flex;align-items:center;gap:8px;font-size:17px;font-weight:700;color:var(--brown-dark)">Выбрано: <span class="count-badge">{{ selectedHobbies.length }}</span></div>
              <button class="btn-primary" @click="nextOnboarding">Далее →</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============ MAIN APP ============ -->
    <div v-if="page==='feed'" class="app-layout">
      <!-- SIDEBAR -->
      <div class="app-sidebar">
        <div class="app-brand">
          <div class="logo-icon-xs"><span style="font-size:18px">⭐</span></div>
          <div><div class="app-brand-name">ХОББИДРУГ</div><div class="app-brand-sub">serivce for hobby</div></div>
        </div>
        <div class="nav-item" :class="{active:navPage==='profile'}" @click="isGuest?showToast('Войдите'):navPage='profile'"><span class="nav-icon">⭐</span> Профиль</div>
        <div class="nav-item" :class="{active:navPage==='feed'}" @click="navPage='feed'"><span class="nav-icon">📋</span> Лента</div>
        <div class="nav-item" :class="{active:navPage==='chats'}" @click="isGuest?showToast('Войдите'):navPage='chats'">
          <span class="nav-icon">💬</span> Чаты
          <span v-if="!isGuest&&totalChatUnread>0" class="nav-badge">{{ totalChatUnread }}</span>
        </div>
        <div class="nav-item" :class="{active:navPage==='friends'}" @click="isGuest?showToast('Войдите'):navPage='friends'"><span class="nav-icon">👥</span> Друзья</div>
        <div class="nav-item" :class="{active:navPage==='settings'}" @click="navPage='settings'"><span class="nav-icon">⚙️</span> Настройки</div>
        <div class="sidebar-footer">
          <div class="nav-item" :class="{active:navPage==='rules'}" @click="navPage='rules'"><span class="nav-icon">📜</span> Правила</div>
          <div v-if="!isGuest" class="btn-logout" @click="page='auth'">Выйти</div>
        </div>
      </div>

      <!-- MAIN -->
      <div class="app-main-scroll" ref="mainScroll" id="mainScroll" style="flex:1;overflow-y:auto">
        <!-- TOPBAR -->
        <div class="app-topbar">
          <div class="topbar-search-wrap">
            <div class="topbar-search">
              <span style="color:#bbb">🔍</span>
              <input v-model="searchQuery" @input="searchOpen=searchQuery.length>0" @blur="setTimeout(()=>searchOpen=false,200)" placeholder="Поиск..."/>
            </div>
          </div>
          <div class="topbar-right">
            <button class="heart-btn" :class="likedPosts.length>0?'active-likes':''" @click="navPage='likes'">
              ❤️<div v-if="likedNotifCount>0" class="likes-count-badge">{{ likedNotifCount }}</div>
            </button>
            <div v-if="!isGuest" class="streak-display"><span>{{ currentUser.streak }} дней подряд 🔥</span></div>
            <button v-if="!isGuest" class="btn-create-post" @click="showCreatePost=true">+ Пост</button>
            <div v-if="!isGuest" class="user-avatar-btn" @click="navPage='profile'"><img :src="currentUser.avatar"/></div>
            <button v-if="isGuest" class="btn-create-post" @click="page='auth'">Войти</button>
          </div>
        </div>

        <!-- GUEST BANNER -->
        <div v-if="isGuest" class="guest-banner">
          <span style="font-size:20px">🌟</span>
          <span>Просмотр без входа</span>
          <div class="guest-banner-btns">
            <button class="gb-btn-outline" @click="page='auth';authMode='login'">Войти</button>
            <button class="gb-btn-solid" @click="page='auth';authMode='register'">Регистрация</button>
          </div>
        </div>

        <!-- FEED -->
        <div v-if="navPage==='feed'" class="feed-page-wrap">
          <div class="feed-main">
            <div v-for="post in sortedPosts" :key="post.id" class="post-card">
              <div class="post-header">
                <div class="post-author">
                  <div class="post-avatar" @click="goToUser(post.authorId)"><img :src="post.avatar"/></div>
                  <div><div class="post-author-name" @click="goToUser(post.authorId)">{{ post.author }}</div><div class="post-time">{{ post.time }}</div></div>
                </div>
                <div class="post-meta">
                  <span class="post-badge" :class="post.hobbyDone?'hobby-done':''">{{ post.badge }}</span>
                  <span class="post-flame">🔥 {{ post.streak }}</span>
                </div>
              </div>
              <div class="post-title">{{ post.title }}</div>
              <div class="post-content-wrap">
                <div class="post-text">
                  <span v-if="!post.expanded && post.description?.length > 220">
                    {{ post.description.slice(0, 220) }}...
                    <button class="read-more-btn" @click="post.expanded=true">Читать далее</button>
                  </span>
                  <span v-else>{{ post.description }}</span>
                </div>
                <div v-if="post.file_url" class="post-img"><img :src="post.file_url"/></div>
              </div>
              <div v-if="post.tags?.length" class="post-tags">
                <span v-for="tag in post.tags" :key="tag" class="post-tag">{{ tag }}</span>
              </div>
              <div class="post-actions">
                <button class="action-btn" :class="{liked:post.liked}" @click="likePost(post)">
                  <span class="heart-icon">{{ post.liked?'❤️':'🤍' }}</span> {{ post.likes }}
                </button>
                <button class="action-btn" @click="toggleComments(post.id)">💬 {{ post.comments?.length || 0 }}</button>
              </div>
              <div v-if="openComments[post.id]" class="comments-section">
                <div v-for="c in post.comments" :key="c.id" class="comment-item">
                  <div class="comment-avatar"><img :src="currentUser.avatar"/></div>
                  <div class="comment-bubble">
                    <div class="comment-author">{{ c.author }}</div>
                    <div class="comment-text">{{ c.text }}</div>
                    <div class="comment-time">{{ c.time }}</div>
                  </div>
                </div>
                <div class="comment-input-wrap">
                  <img :src="currentUser.avatar" style="width:32px;height:32px;border-radius:50%"/>
                  <input class="comment-input" v-model="commentInputs[post.id]" placeholder="Комментарий..." @keyup.enter="sendComment(post)"/>
                  <button class="comment-send" @click="sendComment(post)">↑</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- CREATE POST MODAL -->
        <div v-if="showCreatePost" class="modal-overlay" @click.self="showCreatePost=false">
          <div class="modal-box">
            <div class="modal-title"><span>Создать пост</span><span class="modal-close" @click="showCreatePost=false">✕</span></div>
            <input v-model="newPostTitle" placeholder="Заголовок" />
            <textarea v-model="newPostText" placeholder="Текст поста"></textarea>
            <div>
              <input v-model="newPostTagInput" placeholder="#тег" @keyup.enter="addTagFromInput"/>
              <button @click="addTagFromInput">+</button>
            </div>
            <label>Фото: <input type="file" @change="handleImageUpload"/></label>
            <div>
              <input type="checkbox" v-model="newPostHobbyDone"> Занимался хобби сегодня
            </div>
            <button @click="submitPost">Опубликовать</button>
          </div>
        </div>
      </div>
    </div>

    <!-- SCROLL TOP BUTTON -->
    <button v-if="showScrollTop && navPage==='feed'" class="scroll-top" @click="scrollToTop()">↑</button>
  `
};

// --- Применяем тему
document.addEventListener('DOMContentLoaded', () => {
  const theme = localStorage.getItem('hd_theme') || 'light';
  document.body.classList.toggle('dark', theme === 'dark');
  // app.mount('#app'); // Убираем, т.к. монтируем в main.js
});
