from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserInfo, UserProfileExtended, ProfileCompleteRequest
from models import User as UserModel
from models.user_hobbies import UserHobby
from models.goals import Goal
from models.user_profiles import UserProfile
from dependency import get_current_user
from database import get_db
from services.users import UserService
from repositories import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserInfo)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Получить базовую информацию о текущем пользователе"""
    return UserInfo.model_validate(current_user)


@router.get("/me/extended", response_model=UserProfileExtended)
def get_extended_profile_endpoint(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить расширенный профиль с постами и активностью"""
    repo = UserRepository(db)
    service = UserService(repo)
    return service.get_extended_profile(current_user.id)


@router.put("/me/profile", response_model=UserProfileExtended)
def update_profile(
    profile_data: ProfileCompleteRequest,  # ✅ Исправлено: profile_ → profile_data
    current_user: UserModel = Depends(get_current_user),  # ✅ Исправлено: User → UserModel
    db: Session = Depends(get_db)
):
    """
    Обновление профиля пользователя (хобби, цели, looking_for)
    
    - Работает как для создания нового профиля
    - Так и для обновления существующего
    """
    # ✅ Обновляем или создаём основной профиль
    user_profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()
    
    if user_profile:
        # Обновляем существующий
        user_profile.looking_for = profile_data.looking_for
    else:
        # Создаём новый
        user_profile = UserProfile(
            user_id=current_user.id,
            looking_for=profile_data.looking_for
        )
        db.add(user_profile)
    
    # ✅ Обновляем хобби (удаляем старые, добавляем новые)
    db.query(UserHobby).filter(UserHobby.user_id == current_user.id).delete()
    
    for hobby_data in profile_data.hobbies:
        user_hobby = UserHobby(
            user_id=current_user.id,
            hobby_id=hobby_data.hobby_id,
            experience_level=hobby_data.experience_level,
            frequency_per_week=hobby_data.frequency_per_week,
            experience_description=hobby_data.experience_description,
            why_this_hobby=hobby_data.why_this_hobby,
            looking_for_in_partner=hobby_data.looking_for_in_partner,
            is_public=hobby_data.is_public
        )
        db.add(user_hobby)
    
    # ✅ Обновляем цели (удаляем старые, добавляем новые)
    db.query(Goal).filter(Goal.user_id == current_user.id).delete()
    
    for goal_data in profile_data.goals:
        goal = Goal(
            user_id=current_user.id,
            type=goal_data.type,
            title=goal_data.title,
            description=goal_data.description,
            why_goal=goal_data.why_goal,
            is_public=goal_data.is_public
        )
        db.add(goal)
    
    db.commit()
    
    # ✅ Возвращаем обновлённый профиль через сервис
    repo = UserRepository(db)
    service = UserService(repo)
    return service.get_extended_profile(current_user.id)