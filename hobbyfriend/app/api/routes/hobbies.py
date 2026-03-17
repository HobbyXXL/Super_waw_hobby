# app/api/routes/hobbies.py

from fastapi import APIRouter

# Инициализация APIRouter для маршрутов, связанных с хобби
router = APIRouter()

# Пример маршрута для получения списка хобби
@router.get("/")
async def get_hobbies():
    return {"message": "Список доступных хобби"}

# Пример маршрута для получения конкретного хобби по ID
@router.get("/{hobby_id}")
async def get_hobby(hobby_id: int):
    return {"message": f"Информация о хобби с ID: {hobby_id}"}

# Добавьте другие эндпоинты, связанные с хобби, например:
# @router.post("/")
# async def create_hobby(...):
#     ...
# @router.put("/{hobby_id}")
# async def update_hobby(hobby_id: int, ...):
#     ...
# @router.delete("/{hobby_id}")
# async def delete_hobby(hobby_id: int):
#     ...
