from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from api.router import common_router
from core.handlers import register_exception_handlers
from database import engine, Base
from services.seed_hobbies import seed_hobbies
from sqlalchemy.orm import Session

security = HTTPBearer()

app = FastAPI(
    title="HobbyX API",
    version="0.2.0",
    description="API for HobbyX platform — с верификацией по коду и расширенными профилями",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(common_router)

# Раздача статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

register_exception_handlers(app)

@app.on_event("startup")
def startup_event():
    """
    Выполняется при запуске приложения:
    1. Создаёт таблицы БД (если не существуют)
    2. Заполняет 20 базовых хобби
    """
    # Создаём таблицы (если не существуют)
    Base.metadata.create_all(bind=engine)
    
    # Заполняем хобби
    from database import SessionLocal
    db = SessionLocal()
    try:
        seed_hobbies(db)
    finally:
        db.close()
    
    print("HobbyX API запущен!")

def custom_openapi():
    from fastapi.openapi.utils import get_openapi
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="HobbyX API",
        version="0.2.0",
        description="API for HobbyX platform — с верификацией по коду и расширенными профилями",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token (get it from POST /auth/login)"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def root():
    return {
        "message": "HobbyX API — ready",
        "version": "0.2.0",
        "docs": "/docs",
        "features": [
            "Регистрация с подтверждением по коду",
            "20 базовых хобби с описаниями уровней",
            "Профиль с до 5 хобби и до 4 целей",
            "Календарь активности",
            "Лента постов/отчетов",
            "Поиск пользователей по хобби"
        ]
    }