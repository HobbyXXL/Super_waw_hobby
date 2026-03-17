from fastapi import FastAPI
from app.api.routes import posts, communities, hobbies

app = FastAPI(title="HobbyFriend API")

app.include_router(posts.router)
app.include_router(communities.router)
app.include_router(hobbies.router)











#cd C:\Users\Камила\Desktop\studies\school_x\hobbyfriend
#.venv\Scripts\activate
#uvicorn app.main:app --reload


#http://127.0.0.1:8000/docs
#pytest
#python -m http.server 5500 or http://127.0.0.1:5500