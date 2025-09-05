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


class PlayerAlreadyExistsException(HTTPException):
    def __init__(self, name: str):
        super().__init__(status_code=400, detail=f"Player '{name}' already exists")

class PlayerCreationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Failed to create player")

class PlayerNotFoundException(HTTPException):
    def __init__(self, player_id: str):
        super().__init__(status_code=404, detail=f"Player with id {player_id} not found")

class MatchCreationFailedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Failed to create match")

class InvalidMatchSetupException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)