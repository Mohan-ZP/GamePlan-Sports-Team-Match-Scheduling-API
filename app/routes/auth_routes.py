from fastapi import APIRouter, HTTPException
from app.models import LoginRequest, UserRegister
from app.database import users_collection
from app.utils.decorators import response_timer
from app.utils.helpers import hash_password, verify_password, create_access_token
from app.utils.logger import logger
from app.utils.exceptions import UserAlreadyExistsException, RegistrationFailedException, InvalidCredentialsException


router = APIRouter()


@router.post("/register")
@response_timer
async def register_user(user: UserRegister):
    try:
        # Check if user already exists
        if users_collection.find_one({"email": user.email}):
            logger.warning(f"Registration failed: User already exists - {user.email}")
            raise UserAlreadyExistsException(user.email)

        # Hash password
        hashed_password = hash_password(user.password)

        # Create user document
        user_doc = {
            "username": user.username,
            "email": user.email,
            "password": hashed_password,
            "role": user.role
        }

        result = users_collection.insert_one(user_doc)

        if not result.inserted_id:
            logger.error(f"Registration failed for {user.email}")
            raise RegistrationFailedException()

        logger.info(f"User registered successfully: {user.email}")
        return {"message": f"User registered successfully: {user.email}", "user_id": str(result.inserted_id)}

    except UserAlreadyExistsException as e:
        raise e  # re-raise to FastAPI
    except Exception as e:
        logger.exception(f"Unexpected error during registration: {str(e)}")
        raise RegistrationFailedException()


@router.post("/login")
@response_timer
async def login_user(credentials: LoginRequest):
    try:
        # Check if user exists
        user = users_collection.find_one({"email": credentials.email})
        if not user:
            logger.warning(f"Login failed: Email not found - {credentials.email}")
            raise InvalidCredentialsException()

        # Verify password
        if not verify_password(credentials.password, user["password"]):
            logger.warning(f"Login failed: Incorrect password - {credentials.email}")
            raise InvalidCredentialsException()

        # Create JWT token
        token_data = {"user_id": str(user["_id"]), "role": user["role"]}
        token = create_access_token(token_data)

        logger.info(f"User logged in successfully: {credentials.email}")
        return {"access_token": token, "token_type": "bearer"}

    except InvalidCredentialsException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed due to server error")
