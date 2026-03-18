import random
import string
import httpx

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

BASE_URL = "http://127.0.0.1:8000"

# уникальные данные для пользователя
suffix = random_string()
login = f"testuser_{suffix}"  # поле login
email = f"test_{suffix}@example.com"
password = "123456"

# регистрация
register_data = {
    "login": login,     # теперь поле соответствует ожиданиям FastAPI
    "email": email,
    "password": password
}

with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/auth/register", json=register_data)
    print("Register:")
    print("STATUS:", response.status_code)
    print(response.json())
    print("-" * 50)

# логин
login_data = {
    "login": login,
    "password": password
}

with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/auth/login", json=login_data)
    print("Login:")
    print("STATUS:", response.status_code)
    login_result = response.json()
    print(login_result)
    print("-" * 50)

    token = login_result.get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # создание сообщества
    community_data = {"name": f"Любители рисования {random_string()}"}
    response = client.post(f"{BASE_URL}/communities/", json=community_data, headers=headers)
    print("Create Community:")
    print("STATUS:", response.status_code)
    print(response.json())
    print("-" * 50)

    # получение постов
    response = client.get(f"{BASE_URL}/posts/", headers=headers)
    print("Get Posts:")
    print("STATUS:", response.status_code)
    print(response.json())
    print("-" * 50)

print("START TEST")