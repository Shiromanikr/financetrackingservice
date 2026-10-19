from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
#from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from models import User

SECRET_KEY = "YOUR SECRET KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#security = HTTPBasic() #token extract from header
security = HTTPBearer()


def hash_password(password):
    return pwd_context.hash(password)

def verfiy_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE)
    
    data={
        "user_id": user_id,
        "exp": expire
    }
    token = jwt.encode(data, SECRET_KEY, algorithm= ALGORITHM)
    
    return token

# Verify JWT token and get user from database
def verifty_token(token: str, db: Session):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            return None

        user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

        return user

    except JWTError:
        return None
    
###### Get user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = verifty_token(token, db)
    
    

    if not user:
        raise HTTPException(
            
            status_code=401,
            detail="Invalid token, expired token, or user not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user
