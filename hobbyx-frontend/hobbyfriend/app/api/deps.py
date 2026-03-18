from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
# откуда брать токен — fastapi.security, jwt decode и т.д.

def get_db_dep():
    yield from get_db()

# Заглушка get_current_user (замени на реальную авторизацию)
def get_current_user():
    class User:
        id = "u1"
    return User()