const API = "http://127.0.0.1:8000";

// регистрация
async function register() {
    const data = {
        login: document.getElementById("reg_login").value,
        email: document.getElementById("reg_email").value,
        password: document.getElementById("reg_password").value
    };

    const res = await fetch(API + "/auth/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const text = await res.text();

    if (res.status === 200) {
        document.getElementById("reg_result").innerText = "✅ пользователь создан";
    } else {
        document.getElementById("reg_result").innerText = "❌ ошибка: " + text;
    }
}

// логин
async function login() {
    const data = {
        login: document.getElementById("login_login").value,
        password: document.getElementById("login_password").value
    };

    const res = await fetch(API + "/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const text = await res.text();

    if (res.status === 200) {
        document.getElementById("login_result").innerText = "✅ вход выполнен";
    } else {
        document.getElementById("login_result").innerText = "❌ ошибка входа";
    }
}

// создать пост
async function createPost() {
    const data = {
        content: document.getElementById("post_content").value,
        author_id: "test"
    };

    const res = await fetch(API + "/posts/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.status === 200) {
        document.getElementById("post_result").innerText = "✅ пост создан";
        loadFeed();
    } else {
        document.getElementById("post_result").innerText = "❌ ошибка";
    }
}

// загрузка ленты
async function loadFeed() {
    const res = await fetch(API + "/posts/feed");
    const data = await res.json();

    const feed = document.getElementById("feed");
    feed.innerHTML = "";

    data.forEach(post => {
        const li = document.createElement("li");
        li.innerText = post.content;
        feed.appendChild(li);
    });
}