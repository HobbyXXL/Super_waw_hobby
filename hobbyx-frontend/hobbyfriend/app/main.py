from fastapi import FastAPI
from app.api.routes import auth, users, posts, communities, hobbies
from app.core.database import Base, engine

app = FastAPI()

# 🔥 СОЗДАНИЕ ТАБЛИЦ
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(communities.router)
app.include_router(hobbies.router)











#cd C:\Users\Камила\Desktop\studies\school_x\hobbyfriend
#.venv\Scripts\activate
#uvicorn app.main:app --reload
#http://127.0.0.1:8000/docs
