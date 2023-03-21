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
@app.post('/posts/user/{id}', response_model=schemas.ShowAllPost, status_code=status.HTTP_201_CREATED)
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
@app.get('/user/posts/{id}', response_model=schemas.ShowPostByUser)
def get_all_posts_by_user(id: int):
    posts = db.query(models.Post).filter(models.Post.posted_by == id).all()
    return posts



# show post by a particular ID
@app.get('/posts/{id}', response_model=schemas.ShowPost)
def view_post_by_id(id: int):
    post_by_id = db.query(models.Post).filter(models.Post.id == id).first()
    return post_by_id



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
def upload_file(file: UploadFile = File(...)):  
    
    upload_dir = r"E:\Shubhchintak Technology Pvt. Ltd. (Internship)\Project\Content Management System\Coding Workspace\Content Management System\uploaded_files"
    
    # get the destination path
    destination_path = os.path.join(upload_dir, file.filename)
    print(destination_path)
    
    # copying file contents
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # wb means write and binary
    
    # adding the locally stored file to the database
    db_file = db.query(models.Media).filter(models.Media.link == file.filename).first()
    if db_file is not None:
        raise HTTPException(status_code=400, detail="Media File already exists")
    
    print(file.filename)
    new_media = models.Media(
        link = file.filename
    )

    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    
    return {"Result": "OK"}

 
#  APIs for Adding Comments
# add comment to a particular post
@app.post('/comments/{id}', response_model=schemas.ShowComment)
def add_comment(id: int, comment: schemas.AddComment):
    validate = db.query(models.Post).filter(models.Post.id == id).first()
    if validate is not None: 
        new_comment = models.Comment(
            post_id = validate.id,
            description =  comment.description,
            commented_by = comment.commented_by
        )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# delete a comment by id
@app.delete('/delete_comments/{id}')
def delete_comment_by_id(id: int):
    comment_to_delete = db.query(models.Comment).filter(models.Comment.id == id).first()
    if comment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")
    db.delete(comment_to_delete)
    db.commit()
    db.refresh(comment_to_delete)
    return comment_to_delete
    


# API to mark a post as featured post
@app.post('/admin/posts/{id}', response_model=schemas.ShowAllPost)
def mark_featured(id: int):
    to_mark = db.query(models.Post).filter(models.Post.id == id).first()
    if to_mark.is_featured == False:
        to_mark.is_featured = True

    db.commit()
    db.refresh(to_mark)
    return to_mark



# show all featured posts
@app.get('/posts/is_featured/{value}', response_model=List[schemas.ShowFeaturedPosts])
def list_all_featured_posts(value: bool):
    featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
    return featured_posts



# Implementing Search Functionality
# get all posts of a particular category
@app.get('/posts/{category}', response_model=List[])