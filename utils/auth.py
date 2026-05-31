from datetime import datetime, timezone, timedelta
from jose import jwt,JWTError
from config import *
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.users import User

 
def create_access_token(data: dict):
    # Copy data to avoid modifying original input
    to_encode = data.copy()

    # Set token expiry time (e.g., 30 minutes from now)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry to payload
    to_encode.update({"exp": expire})

    # Encode JWT using secret key + algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str):
    try:
        # Decode token → validates signature + expiry automatically
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except JWTError:
        # Token invalid / expired
        raise ValueError("Invalid or Expired token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# This tells FastAPI:
# "Get token from Authorization header (Bearer <token>)"

def get_current_user(
    token: str = Depends(oauth2_scheme),   # Extract token from request header
    db: Session = Depends(get_db)          # DB session
):
    try:
        # Step 1: Decode token
        payload = verify_access_token(token)

        # Step 2: Extract user identity
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception:
        # Any decoding error → unauthorized
        raise HTTPException(status_code=401, detail="Invalid token")

    # Step 3: Fetch user from DB
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        # Token valid but user no longer exists
        raise HTTPException(status_code=401, detail="User not found")

    # Step 4: Return user object → used in routes
    return user
    