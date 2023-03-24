from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.authentication import get_current_user


router = APIRouter(prefix="/admin", tags=["Admin"])  
    
        

# API to mark a post as featured post
@router.post('/posts/mark_featured/{id}', response_model=schemas.ShowAllPost)
def mark_featured(id: int, current: int = Depends(get_current_user)):
    current_user = db.query(models.User).filter(models.User.id == current).first()
    print(current_user.role)
    
    to_mark = db.query(models.Post).filter((models.Post.id == id) & (current_user.role=="admin")).first()
    if to_mark is not None:
        if to_mark.is_featured == False:
            to_mark.is_featured = True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have authority to update role of any user")

    db.commit()
    db.refresh(to_mark)
    return to_mark



# show all featured posts
@router.get('/posts/show_featured/{value}', response_model=List[schemas.ShowFeaturedPosts])
def list_all_featured_posts(value: bool):
    featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
    return featured_posts


# API to change user roles and permissions
@router.post('/update_user_role/{id}', response_model=schemas.UserResponse)
def change_user_role(id: int, user: schemas.ChangeRole):
    user_details = db.query(models.User).filter(models.User.id == id).first()
    user_details.role = user.role
    
    db.commit()
    db.refresh(user_details)
    return user_details
