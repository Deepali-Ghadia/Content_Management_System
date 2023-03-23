from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


# API to mark a post as featured post
@router.post('/admin/posts/{id}', response_model=schemas.ShowAllPost)
def mark_featured(id: int):
    to_mark = db.query(models.Post).filter(models.Post.id == id).first()
    if to_mark.is_featured == False:
        to_mark.is_featured = True

    db.commit()
    db.refresh(to_mark)
    return to_mark



# show all featured posts
@router.get('/posts/is_featured/{value}', response_model=List[schemas.ShowFeaturedPosts])
def list_all_featured_posts(value: bool):
    featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
    return featured_posts


# API to change user roles and permissions
@router.post('/admin/user_roles/{id}', response_model=schemas.UserResponse)
def change_user_role(id: int, user: schemas.ChangeRole):
    user_details = db.query(models.User).filter(models.User.id == id).first()
    user_details.role = user.role
    
    db.commit()
    db.refresh(user_details)
    return user_details
