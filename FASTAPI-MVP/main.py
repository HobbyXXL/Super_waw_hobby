from fastapi import FastAPI
from api.router import common_router

app = FastAPI(title="HobbyX API", version="0.1.0")
app.include_router(common_router)
