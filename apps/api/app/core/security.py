from pwdlib import PasswordHash
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
import jwt
from jwt.exceptions import InvalidTokenError

load_dotenv()

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password:str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }
    return jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM", "HS256"))

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM", "HS256")])
        user_id = payload.get("sub")

        if not user_id:
            raise InvalidTokenError("Token is missing sub")
        return user_id
    except InvalidTokenError:
        raise


