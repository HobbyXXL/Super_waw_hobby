from fastapi import FastAPI
from core.database import Base, engine

from routers import posts, likes, comments

app = FastAPI(
    title="HobbyFriend API 💙",
    description="API для социальной сети по интересам (посты, лайки, комментарии)",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(likes.router)
app.include_router(comments.router)


@app.get(
    "/",
    summary="🏠 Проверка сервера",
    description="Проверяет, что API работает"
)
def root():
    return {"message": "API работает 🚀"}