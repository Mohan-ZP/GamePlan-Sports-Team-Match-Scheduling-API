from fastapi import HTTPException


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(status_code=400, detail=f"User with email {email} already exists")


class RegistrationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="User registration failed")


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid email or password")


class TeamAlreadyExistsException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=400, detail=f"Team '{name}' already exists")


class TeamCreationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Failed to create team")
