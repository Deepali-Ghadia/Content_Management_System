from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from typing import List
import schemas, models
from routers.authentication import get_current_user


router = APIRouter(prefix="/admin")  
    
def validate_admin(current: int = Depends(get_current_user)):
    current_user = db.query(models.User).filter(models.User.id == current).first()    
    return current_user.role


# API to mark a post as featured post
@router.post('/posts/mark_featured/{id}', response_model=schemas.ShowAllPost, tags=["Admin"])
def mark_featured(id: int, is_admin: str = Depends(validate_admin)):
    
    to_mark = db.query(models.Post).filter((models.Post.id == id) & (is_admin=="admin")).first()
    if to_mark is not None:
        if to_mark.is_featured == False:
            to_mark.is_featured = True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have authority to mark a post as a featured post")

    db.commit()
    db.refresh(to_mark)
    return to_mark




# show all featured posts
@router.get('/posts/show_featured/{value}', response_model=List[schemas.ShowFeaturedPosts], tags=["Posts"])
def list_all_featured_posts(value: bool, random: int = Depends(get_current_user)):
    if random is not None:
        featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
        return featured_posts




# API to change user roles and permissions
@router.post('/update_user_role/{id}', response_model=schemas.UserResponse, tags=["Admin"])
def change_user_role(id: int, user: schemas.ChangeRole, is_admin: str = Depends(validate_admin)):
    user_details = db.query(models.User).filter((models.User.id == id) & (is_admin=="admin")).first()
    
    if user_details is not None:
        user_details.role = user.role
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have authority to update role of any user")
    
    db.commit()
    db.refresh(user_details)
    return user_details
