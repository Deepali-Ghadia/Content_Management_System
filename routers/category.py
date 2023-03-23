from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


# APIs for Category

# create a category
@router.post('/category', response_model=schemas.Category)
def create_category(category: schemas.CreateCategory):
    new_category = models.Category(
        name= category.name
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
    
    
# View all categories along with posts
@router.get('/categories', response_model=List[schemas.Category])
def get_categorieswith_posts():
    categories = db.query(models.Category).all()
    return categories



# list all categories
@router.get('/categories_list/', response_model=List[schemas.ListCategory])
def get_list_of_categories():
    list_of_categories = db.query(models.Category).all()
    return list_of_categories 



# delete a category
@router.delete('/categories/{id}', response_model=schemas.Category)
def delete_a_category(id: int):
    category_to_delete = db.query(models.Category).filter(models.Category.id == id).first()
    if category_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
    db.delete(category_to_delete)
    db.commit()
    db.refresh(category_to_delete)
    return category_to_delete
    

# API to get all the posts of a particular category
@router.get('/posts/search/{category_id}', response_model=schemas.SearchByCategory)
def search_by_category(category_id : int):
    posts_of_a_category  = db.query(models.Category).filter(models.Category.id == category_id).first()
    return posts_of_a_category
