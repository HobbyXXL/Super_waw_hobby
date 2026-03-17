import httpx
import asyncio
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

# --- глобальные переменные ---
results = {}
tokens = {}
post_ids = []
community_ids = []


def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {}


def print_step(title: str):
    print(f"\n{'='*20}")
    print(f"{title}")
    print(f"{'='*20}")


async def register_user(client: httpx.AsyncClient):
    res = await client.post("/auth/register", json={
        "login": "test_user",
        "email": "test@example.com",
        "password": "password123"
    })
    return {"status": res.status_code, "data": safe_json(res)}


async def login_user(client: httpx.AsyncClient):
    res = await client.post("/auth/login", json={
        "login": "test_user",
        "password": "password123"
    })

    data = safe_json(res)

    if res.is_success and "access_token" in data:
        tokens["main"] = data["access_token"]

    return {"status": res.status_code, "data": data}


def get_auth_headers():
    token = tokens.get("main")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


async def create_post(client: httpx.AsyncClient):
    res = await client.post(
        "/posts/",
        json={"title": "Тестовый пост", "content": "Контент поста"},
        headers=get_auth_headers()
    )

    data = safe_json(res)

    if res.is_success and "id" in data:
        post_ids.append(data["id"])

    return {"status": res.status_code, "data": data}


async def get_feed(client: httpx.AsyncClient):
    res = await client.get("/posts/feed", headers=get_auth_headers())
    return {"status": res.status_code, "data": safe_json(res)}


async def like_post(client: httpx.AsyncClient):
    if not post_ids:
        return {"status": 0, "data": "нет поста"}

    res = await client.post(
        f"/posts/{post_ids[0]}/like",
        headers=get_auth_headers()
    )
    return {"status": res.status_code, "data": safe_json(res)}


async def add_comment(client: httpx.AsyncClient):
    if not post_ids:
        return {"status": 0, "data": "нет поста"}

    res = await client.post(
        f"/posts/{post_ids[0]}/comments",
        json={"content": "Тестовый комментарий"},
        headers=get_auth_headers()
    )
    return {"status": res.status_code, "data": safe_json(res)}


async def create_community(client: httpx.AsyncClient):
    res = await client.post(
        "/communities/",
        json={
            "name": "Тест сообщество",
            "description": "Описание",
            "is_private": False
        },
        headers=get_auth_headers()
    )

    data = safe_json(res)

    if res.is_success and "id" in data:
        community_ids.append(data["id"])

    return {"status": res.status_code, "data": data}


async def join_community(client: httpx.AsyncClient):
    if not community_ids:
        return {"status": 0, "data": "нет сообщества"}

    res = await client.post(
        f"/communities/{community_ids[0]}/join",
        headers=get_auth_headers()
    )
    return {"status": res.status_code, "data": safe_json(res)}


async def get_members(client: httpx.AsyncClient):
    if not community_ids:
        return {"status": 0, "data": "нет сообщества"}

    res = await client.get(
        f"/communities/{community_ids[0]}/members",
        headers=get_auth_headers()
    )
    return {"status": res.status_code, "data": safe_json(res)}


async def run_tests():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:

        tests = [
            ("Регистрация", register_user),
            ("Логин", login_user),
            ("Создание поста", create_post),
            ("Лента", get_feed),
            ("Лайк", like_post),
            ("Комментарий", add_comment),
            ("Создание сообщества", create_community),
            ("Вступление", join_community),
            ("Участники", get_members),
        ]

        for name, func in tests:
            print_step(name)

            try:
                result = await func(client)
                results[name] = result

                print(f"Статус: {result['status']}")
                print(f"Ответ: {result['data']}")

            except Exception as e:
                results[name] = {"status": -1, "data": str(e)}
                print(f"❌ Ошибка: {e}")


def print_summary():
    print("\n" + "="*50)
    print("ИТОГИ ТЕСТА")
    print("="*50)

    success = 0
    fail = 0

    for name, result in results.items():
        status = result["status"]

        if 200 <= status < 300:
            print(f"✅ {name:<25} | {status}")
            success += 1
        else:
            print(f"❌ {name:<25} | {status}")
            fail += 1

    print("="*50)
    print(f"Успешно: {success}")
    print(f"Ошибки: {fail}")
    print("="*50)


async def main():
    print("🚀 Запуск полного теста API...\n")

    await run_tests()
    print_summary()


if __name__ == "__main__":
    asyncio.run(main())