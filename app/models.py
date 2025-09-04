from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(..., example="coach_john")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., min_length=6, example="securePass123")
    role: str = Field(..., example="coach")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Team(BaseModel):
    name: str = Field(..., example="Warriors")
    coach: str = Field(..., example="John Doe")
    city: str = Field(..., example="New York")

class Player(BaseModel):
    name: str = Field(..., example="Stephen Curry")
    age: int = Field(..., example=30, gt=0)
    position: str = Field(..., example="Point Guard")
    team_id: str = Field(..., example="64f123abc456")  # Reference to Team
