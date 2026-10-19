
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from security import hash_password, verfiy_password, create_access_token , get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        hash_password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "user_id": new_user.id
    }
@router.post("/login")
def login(user:UserLogin, db:Session=Depends(get_db)):
    #email check
    db_user=db.execute(select(User).where(User.email == user.email)).scalar_one_or_none()
    
    if not db_user:
        return{
            "error":"User Invalid Email"
        }
     #password check   
    if not verfiy_password(user.password, db_user.hash_password):
        return{
            "error":"User Invalid Password"
        }
    #Token generate
    token = create_access_token(db_user.id)
    
    return{
        "messsage": "Login Successfull",
        "access_token": token
    }
@router.get("/me")
def profile(current_user:User = Depends(get_current_user)):
    return{
        "id": current_user.id,
        "email":current_user.email,
        "name":current_user.name
    }
     
