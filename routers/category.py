from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.authentication import get_current_user


router = APIRouter(prefix="/category", tags=['Category'])


# APIs for Category

# create a category
@router.post('/create_category', response_model=schemas.Category)
def create_category(category: schemas.CreateCategory, random :int = Depends(get_current_user)):
    if random is not None:
        new_category = models.Category(
            name= category.name
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    
    
# # View all categories along with posts
# @router.get('/view_all', response_model=List[schemas.Category])
# def get_categorieswith_posts():
#     categories = db.query(models.Category).all()
#     return categories



# list all categories
@router.get('/list_all', response_model=List[schemas.ListCategory])
def get_list_of_categories(random :int = Depends(get_current_user)):
    if random is not None:
        list_of_categories = db.query(models.Category).all()
        return list_of_categories 



# # delete a category
# @router.delete('/delete/{id}', response_model=schemas.Category)
# def delete_a_category(id: int):
#     category_to_delete = db.query(models.Category).filter(models.Category.id == id).first()
#     if category_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
#     db.delete(category_to_delete)
#     db.commit()
#     db.refresh(category_to_delete)
#     return category_to_delete
    



# API to get all the posts of a particular category
@router.get('/search/{category_id}', response_model=schemas.SearchByCategory)
def search_by_category(category_id : int, random :int = Depends(get_current_user)):
    if random is not None:
        posts_of_a_category  = db.query(models.Category).filter(models.Category.id == category_id).first()
        return posts_of_a_category
