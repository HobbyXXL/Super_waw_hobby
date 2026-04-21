from repositories import UserRepository
from schemas.users import (
    UserRegisterRequest,
    UserLogin,
    UserInfo,
    AccessToken,
    UserProfileExtended,
    ProfileCompleteRequest
)
from core.security import verify_password, create_access_token
from core.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from models import UserHobby, Goal, UserActivity, PortfolioWork as PortfolioWorkModel, User as UserModel
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from services.portfolio import PortfolioService


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    def create_user(self, user: UserRegisterRequest) -> UserInfo:
        """
        Шаг 1: Создание пользователя (до подтверждения email)
        
        ⚠️ Теперь используется в api/auth.py напрямую
        """
        if self.repo.get_by_login(user.login):
            raise UserAlreadyExistsException("login", user.login)
        if self.repo.get_by_email(user.email):
            raise UserAlreadyExistsException("email", user.email)
        
        db_user = self.repo.create(user)
        return UserInfo.model_validate(db_user)

    def authenticate_user(self, credentials: UserLogin) -> AccessToken:
        """
        Вход в систему
        
        - Проверяет login и пароль
        - Проверяет что email подтверждён
        """
        user = self.repo.get_by_login(credentials.login)
        if not user:
            raise InvalidCredentialsException()
        
        if not verify_password(credentials.password, user.password_hash):
            raise InvalidCredentialsException()
        
        # Проверяем что email подтверждён
        if not user.is_verified:
            raise Exception("Email не подтверждён. Пожалуйста, подтвердите код из письма.")
        
        token = create_access_token({"sub": user.login})
        return AccessToken(access_token=token, token_type="bearer")

    def complete_profile(self, user_id: str, profile: ProfileCompleteRequest, db: Session):
        """
        Шаг 3: Заполнение профиля после верификации
        
        - Добавляет хобби (1-5)
        - Добавляет цели (1-4)
        """
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("Пользователь не найден")
        
        if not user.is_verified:
            raise Exception("Email не подтверждён")
        
        # Добавляем хобби (максимум 5)
        for hobby_data in profile.hobbies:
            user_hobby = UserHobby(
                user_id=user_id,
                hobby_id=hobby_data.hobby_id,
                experience_level=hobby_data.experience_level,
                frequency_per_week=hobby_data.frequency_per_week,
                frequency_per_month=hobby_data.frequency_per_month,
                experience_description=hobby_data.experience_description,
                why_this_hobby=hobby_data.why_this_hobby,
                looking_for_in_partner=hobby_data.looking_for_in_partner,
                is_public=hobby_data.is_public
            )
            db.add(user_hobby)
        
        # Добавляем цели (максимум 4)
        for goal_data in profile.goals:
            goal = Goal(
                user_id=user_id,
                type=goal_data.type,
                title=goal_data.title,
                description=goal_data.description,
                target_date=goal_data.target_date,
                why_goal=goal_data.why_goal,
                is_public=goal_data.is_public
            )
            db.add(goal)
        
        db.commit()
        return True

    def get_extended_profile(self, user_id: str) -> UserProfileExtended | None:
        """Получить расширенный профиль с постами и активностью"""
        user = self.repo.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return None
        
        portfolio_service = PortfolioService(self.repo.db)
        posts = portfolio_service.get_user_portfolio(user_id)
        streak = self.calculate_activity_streak(user_id)
        
        return UserProfileExtended(
            id=user.id,
            login=user.login,
            email=user.email,
            role=user.role,
            is_verified=user.is_verified,
            created_at=user.created_at,
            last_seen=user.last_seen,
            posts=posts,
            activity_streak=streak
        )

    def calculate_activity_streak(self, user_id: str) -> int:
        """Считаем количество дней активности подряд"""
        activities = self.repo.db.query(UserActivity).filter(
            UserActivity.user_id == user_id
        ).order_by(UserActivity.activity_date.desc()).all()
        
        if not activities:
            return 0
        
        streak = 0
        today = date.today()
        expected_date = today
        
        for activity in activities:
            if activity.activity_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            elif activity.activity_date < expected_date:
                break
        
        return streak

    def verify_email(self, email: str, code: str, db: Session) -> bool:
        """
        Шаг 2: Подтверждение email кодом
        
        Returns:
            bool: True если код верный
        """
        from services.email import EmailService
        email_service = EmailService(db)
        
        if not email_service.verify_code(email, code):
            return False
        
        # Помечаем пользователя как подтверждённого
        user = self.repo.get_by_email(email)
        if user:
            self.repo.mark_as_verified(user.id)
        
        return True