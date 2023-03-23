from fastapi import APIRouter, status, HTTPException
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


#  APIs for Adding Comments
# add comment to a particular post
@router.post('/comments/{id}', response_model=schemas.ShowComment)
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
@router.delete('/delete_comments/{id}')
def delete_comment_by_id(id: int):
    comment_to_delete = db.query(models.Comment).filter(models.Comment.id == id).first()
    if comment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")
    db.delete(comment_to_delete)
    db.commit()
    db.refresh(comment_to_delete)
    return comment_to_delete