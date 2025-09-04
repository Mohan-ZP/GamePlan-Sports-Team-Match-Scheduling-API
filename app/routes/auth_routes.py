from fastapi import APIRouter, Depends
from app.models import UserRegister
from app.database import users_collection
from app.utils.helpers import hash_password
from app.utils.logger import logger
from app.utils.exceptions import UserAlreadyExistsException, RegistrationFailedException


router = APIRouter()


@router.post("/register")
def register_user(user: UserRegister):
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
