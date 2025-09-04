# app/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
from app.utils.helpers import SECRET_KEY, ALGORITHM
from app.utils.logger import logger
from app.database import users_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            logger.warning("Invalid token")
            raise HTTPException(status_code=401, detail="Invalid token")

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.warning("User not found")
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except JWTError:
        logger.exception("Invalid or expired token")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
