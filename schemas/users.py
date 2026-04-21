from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from typing import Optional, List
from .portfolio import PortfolioWork

# ============================================
# БАЗОВЫЕ СХЕМЫ
# ============================================

class UserBase(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=100)
    role: str = Field(default="user", max_length=20)

# ============================================
# РЕГИСТРАЦИЯ (ШАГ 1)
# ============================================

class UserRegisterRequest(UserBase):
    """Запрос на регистрацию (шаг 1)"""
    password: str = Field(min_length=6, max_length=100)

class UserRegisterResponse(BaseModel):
    """Ответ после регистрации (ждем код)"""
    message: str = "На вашу почту отправлен код подтверждения"
    email: EmailStr
    expires_in_minutes: int = 15

# ============================================
# ПОДТВЕРЖДЕНИЕ КОДА (ШАГ 2)
# ============================================

class VerificationCodeInput(BaseModel):
    """Ввод кода подтверждения"""
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class VerificationResponse(BaseModel):
    """Ответ после подтверждения кода"""
    message: str = "Email подтвержден"
    is_verified: bool = True
    access_token: Optional[str] = None
    token_type: str = "bearer"

class VerificationSuccessResponse(BaseModel):
    message: str
    is_verified: bool
    login: str
    
# ============================================
# ЗАПОЛНЕНИЕ ПРОФИЛЯ (ШАГ 3)
# ============================================

class ExperienceLevelEnum(str):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class UserHobbyInput(BaseModel):
    """Информация о хобби пользователя"""
    hobby_id: int
    experience_level: str = Field(pattern=r"^(beginner|intermediate|advanced)$")
    frequency_per_week: Optional[int] = Field(None, ge=1, le=7)
    frequency_per_month: Optional[int] = Field(None, ge=1, le=31)
    experience_description: Optional[str] = Field(None, max_length=500)
    why_this_hobby: Optional[str] = Field(None, max_length=1000)
    looking_for_in_partner: Optional[str] = Field(None, max_length=500)
    is_public: bool = True

class GoalCreate(BaseModel):
    type: str = Field(pattern=r"^(learn|create|relax)$")
    title: str = Field(min_length=10, max_length=200)
    description: str = Field(min_length=20, max_length=1000)
    target_date: Optional[date] = None
    why_goal: Optional[str] = Field(None, max_length=1000)
    is_public: bool = True

class ProfileCompleteRequest(BaseModel):
    """Запрос на завершение профиля (после верификации)"""
    # ✅ Максимум 5 хобби
    hobbies: List[UserHobbyInput] = Field(..., min_length=1, max_length=5)
    
    # ✅ Минимум 1 цель, максимум 4
    goals: List[GoalCreate] = Field(..., min_length=1, max_length=4)
    
    # ✅ Дополнительно о себе
    looking_for: Optional[str] = Field(None, max_length=500)

class ProfileCompleteResponse(BaseModel):
    """Ответ после завершения профиля"""
    message: str = "Профиль успешно заполнен"
    user_id: str
    hobbies_count: int
    goals_count: int

# ============================================
# АВТОРИЗАЦИЯ
# ============================================

class UserLogin(BaseModel):
    login: str
    password: str

class AccessToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ============================================
# ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ
# ============================================

class User(UserBase):
    id: str
    is_verified: bool = False
    created_at: datetime
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInfo(UserBase):
    id: str
    is_verified: bool = False
    created_at: datetime
    last_seen: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserProfileExtended(UserInfo):
    """Расширенный профиль с постами и активностью"""
    posts: List[PortfolioWork] = []
    activity_streak: int = 0
    hobbies: Optional[List[dict]] = []
    goals: Optional[List[dict]] = []

# ============================================
# ПОВТОРНАЯ ОТПРАВКА КОДА
# ============================================

class ResendCodeRequest(BaseModel):
    email: EmailStr

class ResendCodeResponse(BaseModel):
    message: str = "Код отправлен повторно"
    expires_in_minutes: int = 15