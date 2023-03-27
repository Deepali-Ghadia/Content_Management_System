from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from typing import List
import schemas, models
from routers.authentication import get_current_user


router = APIRouter(prefix="/user", tags=["User"])


# view all users
@router.get('/list_all', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(random: int = Depends(get_current_user)):
    if random is not None:
        users=db.query(models.User).all()
        return users



# view an user by its id along with posts
@router.get('/view/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, random: int = Depends(get_current_user)):
    if random is not None:
        user = db.query(models.User).filter(models.User.id == id).first()
        return user



# update an user
@router.post('/update/', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_user(user: schemas.UpdateUser, user_id: int = Depends(get_current_user)):


    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
    user_to_update.username = user.username,
    user_to_update.mobile_number = user.mobile_number,
    user_to_update.profile_photo = user.profile_photo,
    user_to_update.bio = user.bio

    db.commit()
    db.refresh(user_to_update)
    return user_to_update



# delete an user
@router.delete('/delete/')
def delete_an_user(id: int = Depends(get_current_user)):
    user_to_delete=db.query(models.User).filter(models.User.id==id).first()
    
    # if user_to_delete is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    db.delete(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    return user_to_delete
    
    
    
    
    