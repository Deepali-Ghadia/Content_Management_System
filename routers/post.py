from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.authentication import get_current_user


router = APIRouter(prefix="/posts")


# APIs for Post

# view all posts
@router.get('/all', response_model=List[schemas.ShowAllPost], status_code=status.HTTP_200_OK, tags=['Posts'])
def get_all_posts(random: int = Depends(get_current_user) ):
    if random is not None:
        posts = db.query(models.Post).filter(models.Post.is_published==True).all()
        return posts



# create a post 
@router.post('/create/', response_model=schemas.ShowAllPost, status_code=status.HTTP_201_CREATED,tags=['Posts'])
# the ID returned by get_current_user is mapped with the id in the argument
def create_post( post: schemas.CreatePost, id:int = Depends(get_current_user) ):
    
    # media_owner = db.query(models.Media).filter(models.Media.user == id).first()
    # if media_owner is None:
    #     return {"message": "This media file does not belong to you ❌❌"}
        
    # else:  
    new_post = models.Post(
        title = post.title,
        description = post.description,
        posted_by = id,
        post_category = post.post_category,
        media_id = post.media_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# update a post
@router.post('/update/{id}', response_model=schemas.ShowPostByUser, tags=['Posts'])
def update_an_post(post:schemas.UpdatePost, id: int, user_id:int = Depends(get_current_user)):
    
    post_to_update = db.query(models.Post).filter((models.Post.posted_by == user_id) & (models.Post.id == id)).first()
    
    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to edit someone else's post")
    post_to_update.title = post.title
    post_to_update.description = post.description
    post_to_update.is_published = post.is_published
    post_to_update.post_category = post.category
    post_to_update.media_id = post.media_id
    
    db.commit()
    db.refresh(post_to_update)
    return post_to_update



# delete a post
@router.delete('/delete/{id}', response_model=schemas.ShowPostByUser, tags=['Posts'])
def delete_an_post(id: int, user_id:int = Depends(get_current_user)):
    post_to_delete=db.query(models.Post).filter((models.Post.id==id) & (models.Post.posted_by == user_id)).first()
    
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Either the post does not exist or you are not the owner of this post")
    
    db.delete(post_to_delete)
    db.commit()
    db.refresh(post_to_delete)
    return post_to_delete



# show all my posts
@router.get('/user', response_model=List[schemas.ShowPostByUser], tags=['Posts'])
def get_all_my_posts(id:int = Depends(get_current_user) ):
    posts = db.query(models.Post).filter(models.Post.posted_by == id).all()
    return posts


# get list of posts of a particular user
@router.get('/user/{id}', response_model=List[schemas.ShowPostByUser], tags=['Posts'])
def get_all_posts_of_a_user(id: int, random :int = Depends(get_current_user) ):
    if random is not None:
        posts = db.query(models.Post).filter((models.Post.posted_by == id) & (models.Post.is_published==True)).all()
        return posts



# show post by a particular ID
@router.get('/view_post/{id}', response_model=schemas.ShowPost, tags=['Posts'])
def view_post_by_id(id: int, random: int = Depends(get_current_user) ):
    if random is not None:
        post_by_id = db.query(models.Post).filter(models.Post.id == id).first()
        return post_by_id


