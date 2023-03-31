from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.authentication import get_current_user
import sqlalchemy


router = APIRouter(prefix="/comments",
                   tags=["Comment"])


#  APIs for Adding Comments
# add comment to a particular post
@router.post('/add_comment/{id}', response_model=schemas.ShowComment)
def add_comment(id: int, comment: schemas.AddComment, user_id: int = Depends(get_current_user)):

    validate = db.query(models.Post).filter((models.Post.id == id)).first()
    if validate is not None: 
        new_comment = models.Comment(
            post_id = validate.id,
            description =  comment.description,
            commented_by = user_id
        )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment




# delete a comment by id
@router.delete('/delete_comment/{id}')
def delete_comment_by_id(id: int, user_id:int = Depends(get_current_user)):
    comment_to_delete = db.query(models.Comment).filter((models.Comment.id == id) & (models.User.id == user_id)).first()
    
    if comment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Either the comment does not exist or you are not allowed to delete this comment")
    
    
    try:
        db.delete(comment_to_delete)
        db.commit()
        db.refresh(comment_to_delete)
        
    except sqlalchemy.exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Comment is deleted successfully")
    