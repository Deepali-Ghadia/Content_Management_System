from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


# APIs for Post

# view all posts
@router.get('/posts', response_model=List[schemas.ShowAllPost], status_code=status.HTTP_200_OK)
def get_all_posts():
    posts = db.query(models.Post).all()
    return posts


# create a post 
@router.post('/posts/user/{id}', response_model=schemas.ShowAllPost, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost, id:int):
    new_post = models.Post(
        title = post.title,
        description = post.description,
        posted_by = id,
        post_category = post.post_category
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# update a post
@router.post('/posts/update/{id}', response_model=schemas.ShowPostByUser)
def update_an_post(id: int, post:schemas.UpdatePost):
    post_to_update = db.query(models.Post).filter(models.Post.id == id).first()
    post_to_update.title = post.title
    post_to_update.description = post.description
    post_to_update.is_published = post.is_published
    post_to_update.post_category = post.category
    
    db.commit()
    db.refresh(post_to_update)
    return post_to_update


# delete a post
@router.delete('/posts/delete/{id}', response_model=schemas.ShowPostByUser)
def delete_an_post(id: int):
    post_to_delete=db.query(models.Post).filter(models.Post.id==id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    db.delete(post_to_delete)
    db.commit()
    db.refresh(post_to_delete)
    return post_to_delete


# show posts of a particular user
@router.get('/user/posts/{id}', response_model=List[schemas.ShowPostByUser])
def get_all_posts_by_user(id: int):
    posts = db.query(models.Post).filter(models.Post.posted_by == id).all()
    return posts



# show post by a particular ID
@router.get('/posts/{id}', response_model=schemas.ShowPost)
def view_post_by_id(id: int):
    post_by_id = db.query(models.Post).filter(models.Post.id == id).first()
    return post_by_id


