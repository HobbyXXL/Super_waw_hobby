import requests

BASE = "http://127.0.0.1:8000"

def test_create_post():
    r = requests.post(BASE + "/posts/", json={"content": "test"})
    assert r.status_code == 200

def test_feed():
    r = requests.get(BASE + "/posts/feed")
    assert r.status_code == 200