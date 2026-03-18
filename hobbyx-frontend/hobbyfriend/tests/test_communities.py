import requests

BASE = "http://127.0.0.1:8000"

def test_create_community():
    r = requests.post(BASE + "/communities/", json={"name": "test"})
    assert r.status_code == 200

def test_join():
    r = requests.post(BASE + "/communities/1/join")
    assert r.status_code == 200