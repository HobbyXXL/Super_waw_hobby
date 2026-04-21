from sqlalchemy.orm import Session
from models.email_verification import EmailVerification
from models.users import User
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        
        # Настройки SMTP (из переменных окружения)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_email = os.getenv("SMTP_EMAIL", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.debug_mode = os.getenv("DEBUG_MODE", "true").lower() == "true"

    def generate_verification_code(self) -> str:
        """Генерирует 6-значный код подтверждения"""
        import random
        return str(random.randint(100000, 999999))

    def create_verification_record(self, email: str, user_id: str = None, 
                                    temp_login: str = None, 
                                    temp_password_hash: str = None,
                                    temp_role: str = None) -> str:
        """
        Создаёт запись с кодом подтверждения в БД
        
        Args:
            email: Email пользователя
            user_id: ID пользователя (если уже создан)
            temp_login: Временный логин (до подтверждения)
            temp_password_hash: Временный хеш пароля (до подтверждения)
            temp_role: Временная роль (до подтверждения)
        
        Returns:
            str: Сгенерированный код (в debug режиме)
        """
        # Генерируем код
        code = self.generate_verification_code()
        
        # Деактивируем все предыдущие коды для этого email
        old_codes = self.db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.is_used == False
        ).all()
        
        for old_code in old_codes:
            old_code.is_used = True
        
        # Создаём новую запись с временными данными
        verification = EmailVerification(
            email=email,
            user_id=user_id,
            code=code,
            expires_at=EmailVerification.generate_expires_at(minutes=15),
            temp_login=temp_login,
            temp_password_hash=temp_password_hash,
            temp_role=temp_role
        )
        
        self.db.add(verification)
        self.db.commit()
        
        # В debug режиме возвращаем код (для тестирования)
        if self.debug_mode:
            print(f"\n{'='*50}")
            print(f"📧 EMAIL VERIFICATION CODE (DEBUG MODE)")
            print(f"{'='*50}")
            print(f"Email: {email}")
            print(f"Code: {code}")
            print(f"Login: {temp_login}")
            print(f"Expires: {verification.expires_at}")
            print(f"{'='*50}\n")
        
        return code

    def send_verification_email(self, email: str, code: str):
        """
        Отправляет email с кодом подтверждения
        
        В debug режиме просто выводит код в консоль
        """
        if self.debug_mode:
            # В режиме разработки код уже выведен в create_verification_record
            return
        
        # В production режиме отправляем реальное письмо
        if not self.smtp_email or not self.smtp_password:
            raise Exception("SMTP credentials not configured")
        
        # Создаём письмо
        msg = MIMEMultipart()
        msg['From'] = self.smtp_email
        msg['To'] = email
        msg['Subject'] = "🔐 Код подтверждения HobbyX"
        
        # Тело письма
        body = f"""
        Здравствуйте!
        
        Ваш код подтверждения для HobbyX: {code}
        
        Код действителен в течение 15 минут.
        
        Если вы не регистрировались в HobbyX, проигнорируйте это письмо.
        
        С уважением,
        Команда HobbyX
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Отправляем
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_email, self.smtp_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            raise

    def verify_code(self, email: str, code: str) -> bool:
        """
        Проверяет код подтверждения
        
        Returns:
            bool: True если код верный и не истёк
        """
        verification = self.db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.code == code,
            EmailVerification.is_used == False
        ).first()
        
        if not verification:
            return False
        
        # Проверяем не истёк ли код
        if datetime.utcnow() > verification.expires_at:
            return False
        
        # Помечаем код как использованный
        verification.is_used = True
        verification.used_at = datetime.utcnow()
        self.db.commit()
        
        return True

    def resend_code(self, email: str, user_id: str = None) -> str:
        """
        Повторная отправка кода
        
        Returns:
            str: Новый код
        """
        # Проверяем есть ли пользователь с таким email
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user and not user_id:
            raise Exception("User not found")
        
        # Создаём новый код
        return self.create_verification_record(email, user_id or user.id)