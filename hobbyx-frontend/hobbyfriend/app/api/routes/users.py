# app/api/routes/users.py

from fastapi import APIRouter

# Создаем экземпляр APIRouter для маршрутов, связанных с пользователями
router = APIRouter()

@router.get("/")
async def read_users():
    return {"message": "Список пользователей"}

@router.get("/{user_id}")
async def read_user(user_id: int):
    return {"message": f"Информация о пользователе {user_id}"}

# Добавьте другие маршруты для пользователей здесь, например:
# @router.post("/")
# async def create_user(...):
#     ...
# @router.put("/{user_id}")
# async def update_user(user_id: int, ...):
#     ...
# @router.delete("/{user_id}")
# async def delete_user(user_id: int):
#     ...
