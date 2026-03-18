import requests

BASE = "http://127.0.0.1:8000"

def test_register():
    r = requests.post(BASE + "/auth/register", json={
        "login": "test",
        "email": "t@test.com",
        "password": "123"
    })
    assert r.status_code == 200

def test_login():
    r = requests.post(BASE + "/auth/login", json={
        "login": "test",
        "password": "123"
    })
    assert r.status_code == 200