from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from typing import List
import schemas, models
from routers.authentication import get_current_user
import sqlalchemy


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

    # profile_photo is 0\
    if user.profile_photo == 0:
        user.profile_photo = None
        
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
def delete_an_user(user_id: int = Depends(get_current_user)):
    
    # delete all my posts and comments made by all the users on my post
    posts_of_a_user = db.query(models.Post).filter(models.Post.posted_by == user_id).all()
    # print(posts_of_a_user) # prints a list of all the posts made by a user
    # print(posts_of_a_user[0]) #prints the first post from the list
    # print(posts_of_a_user[0].id) #prints the id of first post
    # print("comments are ........\n")
    # print(posts_of_a_user[0].comments) # prints list of comments
 
        
    try:
        for i in range(len(posts_of_a_user)):
            for j in range(len(posts_of_a_user[i].comments)):
                db.delete(posts_of_a_user[i].comments[j])
        db.delete(posts_of_a_user[i])

        print("Deleted all the posts along with comments")
    
        
        # delete all the comments made by me
        db.query(models.Comment).filter(models.Comment.commented_by == user_id).delete()
        print("deleted all the comments made by me")
        

        # delete the user
        user_to_delete=db.query(models.User).filter(models.User.id==user_id).first()

    
        db.delete(user_to_delete)
        print(6)
        db.commit()
        db.refresh(user_to_delete)
        
    except sqlalchemy.exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="User deleted successfully")
