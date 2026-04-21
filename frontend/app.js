// ============================================
// КОНФИГУРАЦИЯ
// ============================================
const API_URL = 'http://127.0.0.1:8000';
let accessToken = localStorage.getItem('access_token');
let currentUser = null;

// ============================================
// ИНИЦИАЛИЗАЦИЯ
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    loadHobbies();
    showPage('home');
});

// ============================================
// НАВИГАЦИЯ
// ============================================
function showPage(pageId) {
    // Скрываем все страницы
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Показываем нужную
    const targetPage = document.getElementById(pageId + '-page');
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    // Загружаем данные для профиля
    if (pageId === 'profile' && currentUser) {
        loadProfile();
    }
}

// ============================================
// АВТОРИЗАЦИЯ
// ============================================
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        accessToken = token;
        currentUser = JSON.parse(user);
        updateNav(true);
    } else {
        updateNav(false);
    }
}

function updateNav(isLoggedIn) {
    document.getElementById('nav-register').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('nav-login').style.display = isLoggedIn ? 'none' : 'block';
    document.getElementById('nav-logout').style.display = isLoggedIn ? 'block' : 'none';
    document.getElementById('user-info').style.display = isLoggedIn ? 'block' : 'none';
    
    if (isLoggedIn && currentUser) {
        document.getElementById('username-display').textContent = currentUser.login;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    accessToken = null;
    currentUser = null;
    updateNav(false);
    showPage('home');
    showMessage('Вы успешно вышли', 'success');
}

// ============================================
// РЕГИСТРАЦИЯ (ШАГ 1)
// ============================================
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const login = document.getElementById('reg-login').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login, email, password, role: 'user' })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(data.message, 'success');
            document.getElementById('verify-email').value = email;
            showPage('verify');
        } else {
            showMessage(data.detail || 'Ошибка регистрации', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
});

// ============================================
// ПОДТВЕРЖДЕНИЕ КОДА (ШАГ 2)
// ============================================
document.getElementById('verify-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('verify-email').value;
    const code = document.getElementById('verify-code').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/verify-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, code })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // ✅ НОВОЕ: Не сохраняем токен, перенаправляем на вход
            localStorage.removeItem('access_token');
            accessToken = null;
            
            showMessage('Email подтверждён! Теперь войдите в систему', 'success');
            
            // ✅ Перенаправляем на страницу входа через 1.5 секунды
            setTimeout(() => {
                showPage('login');
                // Авто-заполняем логин для удобства
                document.getElementById('login-login').value = data.login || '';
            }, 1500);
        } else {
            showMessage(data.detail || 'Неверный код', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
});

// ============================================
// ЗАПОЛНЕНИЕ ПРОФИЛЯ (ШАГ 3)
// ============================================
document.getElementById('profile-complete-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!accessToken) {
        showMessage('Сначала войдите в систему', 'error');
        showPage('login');
        return;
    }
    
    // Собираем данные из формы
    const selectedHobbies = Array.from(document.querySelectorAll('input[name="hobby"]:checked'))
        .map(input => ({
            hobby_id: parseInt(input.value),
            experience_level: document.getElementById(`exp-${input.value}`).value,
            frequency_per_week: parseInt(document.getElementById(`freq-${input.value}`).value) || 1,
            experience_description: document.getElementById(`exp-desc-${input.value}`).value,
            why_this_hobby: document.getElementById(`why-${input.value}`).value,
            looking_for_in_partner: document.getElementById(`partner-${input.value}`).value,
            is_public: true
        }));
    
    const goals = [];
    const goalTypes = ['learn', 'achieve', 'share', 'other'];
    goalTypes.forEach(type => {
        const title = document.getElementById(`goal-title-${type}`).value;
        if (title.trim()) {
            goals.push({
                type,
                title,
                description: document.getElementById(`goal-desc-${type}`).value,
                why_goal: document.getElementById(`goal-why-${type}`).value,
                is_public: true
            });
        }
    });
    
    const lookingFor = document.getElementById('looking-for').value;
    
    try {
        // ✅ НОВОЕ: Пробуем обновить профиль, если не получится — создаём
        const response = await fetch(`${API_URL}/users/me/profile`, {
            method: 'PUT',  // ✅ PUT для обновления
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                hobbies: selectedHobbies,
                goals,
                looking_for: lookingFor
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Профиль успешно сохранён!', 'success');
            showPage('profile');
            loadProfile();
        } else {
            // Если PUT не сработал, пробуем POST (для старых аккаунтов)
            showMessage(data.detail || 'Ошибка сохранения', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
});
// ============================================
// ВХОД
// ============================================
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const login = document.getElementById('login-login').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            accessToken = data.access_token;
            currentUser = { login };
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateNav(true);
            showMessage('Вы успешно вошли!', 'success');
            
            // ✅ НОВОЕ: Проверяем заполнен ли профиль, если нет — на заполнение
            setTimeout(() => {
                checkProfileComplete();
            }, 500);
        } else {
            showMessage(data.detail || 'Неверный логин или пароль', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
});

// ============================================
// ЗАГРУЗКА ХОББИ
// ============================================
async function loadHobbies() {
    try {
        const response = await fetch(`${API_URL}/hobbies/`);
        const hobbies = await response.json();
        
        const hobbySelect = document.getElementById('hobby-select');
        const searchHobby = document.getElementById('search-hobby');
        
        if (hobbySelect) {
            hobbySelect.innerHTML = hobbies.map(h => 
                `<option value="${h.id}">${h.name}</option>`
            ).join('');
        }
        
        if (searchHobby) {
            searchHobby.innerHTML = '<option value="">Любое хобби</option>' + 
                hobbies.map(h => `<option value="${h.id}">${h.name}</option>`).join('');
        }
    } catch (error) {
        console.error('Ошибка загрузки хобби:', error);
    }
}

// ============================================
// ЗАГРУЗКА ПРОФИЛЯ
// ============================================
async function loadProfile() {
    if (!accessToken) return;
    
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        
        if (response.ok) {
            const user = await response.json();
            document.getElementById('profile-login').textContent = user.login || 'N/A';
            document.getElementById('profile-email').textContent = user.email || 'N/A';
            document.getElementById('profile-verified').textContent = user.is_verified ? '✅ Подтверждён' : '❌ Не подтверждён';
        }
    } catch (error) {
        console.error('Ошибка загрузки профиля:', error);
    }
}

// ============================================
// ОТМЕТКА АКТИВНОСТИ
// ============================================
async function markActivity() {
    if (!accessToken) {
        showMessage('Сначала войдите в систему', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/activity/mark`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                activity_type: 'did_hobby',
                activity_date: new Date().toISOString().split('T')[0]
            })
        });
        
        if (response.ok) {
            showMessage('Активность отмечена!', 'success');
            loadActivityCalendar();
        } else {
            showMessage('Ошибка отметки активности', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
}

// ============================================
// КАЛЕНДАРЬ АКТИВНОСТИ
// ============================================
async function loadActivityCalendar() {
    const calendar = document.getElementById('activity-calendar');
    if (!calendar) return;
    
    // Простая демонстрация (30 дней)
    calendar.innerHTML = '';
    const today = new Date();
    
    for (let i = 0; i < 30; i++) {
        const day = document.createElement('div');
        day.className = 'calendar-day';
        day.textContent = i + 1;
        
        // Случайная активность для демонстрации
        if (Math.random() > 0.5) {
            day.classList.add('active');
        }
        
        calendar.appendChild(day);
    }
}

// ============================================
// СОЗДАНИЕ ПОСТА
// ============================================
document.getElementById('create-post-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const postData = {
        title: document.getElementById('post-title').value,
        description: document.getElementById('post-description').value,
        is_public: document.getElementById('post-public').value === 'true'
    };
    
    try {
        const response = await fetch(`${API_URL}/posts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(postData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('Пост опубликован!', 'success');
            showPage('profile');
        } else {
            showMessage(data.detail || 'Ошибка создания поста', 'error');
        }
    } catch (error) {
        showMessage('Ошибка соединения с сервером', 'error');
        console.error(error);
    }
});

// ============================================
// ПОИСК ПОЛЬЗОВАТЕЛЕЙ
// ============================================
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const hobbyId = document.getElementById('search-hobby').value;
    const level = document.getElementById('search-level').value;
    
    try {
        let url = `${API_URL}/users/search?`;
        if (hobbyId) url += `hobby_id=${hobbyId}&`;
        if (level) url += `level=${level}&`;
        
        const response = await fetch(url);
        const users = await response.json();
        
        const resultsDiv = document.getElementById('search-results');
        if (users.length === 0) {
            resultsDiv.innerHTML = '<p>Ничего не найдено</p>';
        } else {
            resultsDiv.innerHTML = users.map(u => `
                <div class="search-result-item">
                    <h4>${u.login}</h4>
                    <p>Хобби: ${u.hobbies?.map(h => h.name).join(', ') || 'Не указано'}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        showMessage('Ошибка поиска', 'error');
        console.error(error);
    }
});

// ============================================
// СООБЩЕНИЯ
// ============================================
function showMessage(text, type = 'success') {
    const container = document.getElementById('message-container');
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    container.appendChild(message);
    
    setTimeout(() => {
        message.remove();
    }, 3000);
}

// ============================================
// ПРОВЕРКА ЗАПОЛНЕННОСТИ ПРОФИЛЯ
// ============================================
async function checkProfileComplete() {
    if (!accessToken) {
        showPage('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        
        if (response.ok) {
            const user = await response.json();
            
            // ✅ Проверяем есть ли хобби у пользователя
            if (user.hobbies && user.hobbies.length > 0) {
                // Профиль заполнен — идём на главную профиля
                showPage('profile');
                loadProfile();
            } else {
                // Профиль не заполнен — идём на заполнение
                showPage('profile-complete');
                loadHobbies();
            }
        } else {
            showPage('login');
        }
    } catch (error) {
        console.error('Ошибка проверки профиля:', error);
        showPage('login');
    }
}