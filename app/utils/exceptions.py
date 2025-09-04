from fastapi import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"User with email {email} already exists")


class RegistrationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="User registration failed")
