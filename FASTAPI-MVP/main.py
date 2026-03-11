from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import common_router

app = FastAPI(title="HobbyX API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common_router)
