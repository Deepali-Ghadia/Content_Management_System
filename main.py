from fastapi import FastAPI, status, HTTPException, File, UploadFile
import os
import shutil
from typing import List, Annotated
from database import SessionLocal
import schemas 
import models

app = FastAPI()

db=SessionLocal() 

# APIS for User

# view all users
@app.get('/users', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    users=db.query(models.User).all()
    return users

# register a user
@app.post('/users/register', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.CreateUser):
    db_user = db.query(models.User).filter(models.User.name == user.name).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User account already exists")
    
    new_user = models.User(
        name= user.name,
        username= user.username,
        mobile_number= user.mobile_number,
        email_id= user.email_id,
        password= user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# view an user by its id
@app.get('/users/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


# update an user
@app.post('/users/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, user: schemas.UpdateUser):
    user_to_update = db.query(models.User).filter(models.User.id == id).first()
    user_to_update.username = user.username,
    user_to_update.mobile_number = user.mobile_number,
    user_to_update.password = user.password,
    user_to_update.profile_photo = user.profile_photo,
    user_to_update.bio = user.bio

    db.commit()
    db.refresh(user_to_update)
    return user_to_update


# delete an user
@app.delete('/users/{id}')
def delete_an_user(id: int):
    user_to_delete=db.query(models.User).filter(models.User.id==id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    db.delete(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    return user_to_delete
    
    
    
    
    
# APIs for Post

# view all posts
@app.get('/posts', response_model=List[schemas.ShowAllPost], status_code=status.HTTP_200_OK)
def get_all_posts():
    posts = db.query(models.Post).all()
    return posts


# create a post 
@app.post('/posts', response_model=schemas.ShowAllPost, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost):
    new_post = models.Post(
        title = post.title,
        description = post.description,
        posted_by = post.posted_by,
        post_category = post.post_category
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# update a post
@app.post('/posts/update/{id}', response_model=schemas.ShowPostByUser)
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
@app.delete('/posts/delete/{id}', response_model=schemas.ShowPostByUser)
def delete_an_post(id: int):
    post_to_delete=db.query(models.Post).filter(models.Post.id==id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    db.delete(post_to_delete)
    db.commit()
    db.refresh(post_to_delete)
    return post_to_delete

# show posts of a particular user
@app.get('/posts/{id}', response_model=schemas.ShowPostByUser)
def get_all_posts_by_user(id: int):
    posts = db.query(models.Post).filter(models.Post.posted_by == id).first()
    return posts



# APIs for Category

# create a category
@app.post('/category', response_model=schemas.Category)
def create_category(category: schemas.CreateCategory):
    new_category = models.Category(
        name= category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
    
    
# View all categories
@app.get('/categories', response_model=List[schemas.Category])
def get_all_categories():
    categories = db.query(models.Category).all()
    return categories

# delete a category
@app.delete('/categories/{id}', response_model=schemas.Category)
def delete_a_category(id: int):
    category_to_delete = db.query(models.Category).filter(models.Category.id == id).first()
    if category_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
    db.delete(category_to_delete)
    db.commit()
    db.refresh(category_to_delete)
    return category_to_delete
    

# APIs for Media Library

# View all uploaded files
@app.get('/media_files', response_model=List[schemas.ShowMediaFile])
def show_all_media_files():
    files = db.query(models.Media).all()
    return files

# upload a file and add it to local directory
@app.post('/media_library', response_model=schemas.ShowMediaFile)
def upload_file(media: schemas.UploadMediaFile, file: UploadFile = File(...)):  
    
    upload_dir = r"E:\Shubhchintak Technology Pvt. Ltd. (Internship)\Project\Content Management System\Coding Workspace\Content Management System\uploaded_files"
    
    # get the destination path
    destination_path = os.path.join(upload_dir, file.filename)
    print(destination_path)
    
    # copying file contents
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # wb means write and binary
    
    
    return {"Result": "OK"}

 