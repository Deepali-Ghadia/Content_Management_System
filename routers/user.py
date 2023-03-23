from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# view all users
@router.get('/users', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    users=db.query(models.User).all()
    return users



# register a user
@router.post('/users/register', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.CreateUser):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User account already exists")
    
    hashed_password = password_context.hash(user.password)
    
    new_user = models.User(
        name= user.name,
        username= user.username,
        mobile_number= user.mobile_number,
        email_id= user.email_id,
        password= hashed_password
        # alternative to this statement
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# view an user by its id
@router.get('/users/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user



# update an user
@router.post('/users/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, user: schemas.UpdateUser):
    
    hashed_password = password_context.hash(user.password)
    
    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    user_to_update.username = user.username,
    user_to_update.mobile_number = user.mobile_number,
    user_to_update.password = hashed_password,
    user_to_update.profile_photo = user.profile_photo,
    user_to_update.bio = user.bio

    db.commit()
    db.refresh(user_to_update)
    return user_to_update



# delete an user
@router.delete('/users/{id}')
def delete_an_user(id: int):
    user_to_delete=db.query(models.User).filter(models.User.id==id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    db.delete(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    return user_to_delete
    
    
    
    
    