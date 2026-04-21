from fastapi import HTTPException
from enum import Enum
from typing import Optional, Dict, Any

class ErrorCode(Enum):
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "code": error_code.value,
                "message": message,
                "field": field,
                "details": details or {}
            }
        )

class UserAlreadyExistsException(AppException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=400,
            error_code=ErrorCode.USER_ALREADY_EXISTS,
            message=f"Пользователь с {field} '{value}' уже существует",
            field=field,
            details={field: value}
        )

class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(
            status_code=401,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            message="Неверные учётные данные"
        )
