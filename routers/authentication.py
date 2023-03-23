from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.user import password_context
from datetime import datetime, timedelta
from jose import jwt
router = APIRouter()


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def check_password(hashed_password, plain_password):
    return password_context.verify(plain_password, hashed_password)
    


@router.post('/login')
def login(login: schemas.Login):
    user = db.query(models.User).filter(models.User.username == login.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username does not exist")
    
    
    if not check_password(user.password, login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
    
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}