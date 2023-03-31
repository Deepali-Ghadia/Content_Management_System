import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models
from routers.authentication import get_current_user
import sqlalchemy

router = APIRouter()


# APIs for Media Library

# View all uploaded files
@router.get('/media_files', response_model=List[schemas.ShowMediaFile], tags=["Media Library"])
def show_all_media_files(id: int = Depends(get_current_user)):
    
    user_media_files = db.query(models.Media).filter(models.Media.user == id).all()
    
    return user_media_files



# upload a file, add it to local directory and add the file's metadata to the database 
@router.post('/media_library', response_model=schemas.ShowMediaFile, tags=["Media Library"])
def upload_file(file: UploadFile = File(...), id:int = Depends(get_current_user)):  
    
    upload_dir = r'E:/Shubhchintak Technology Pvt. Ltd. (Internship)/Project/Content Management System/Coding Workspace/Content Management System/upload_files/'
    
    # get the destination path
    destination_path = os.path.join(upload_dir, file.filename)
    print(file.filename)
    print(destination_path)
    
    # copying file contents
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # wb means write and binary
    
    
    # # adding the locally stored file to the database

    db_file = db.query(models.Media).filter((models.Media.link == destination_path) & (models.Media.user == id)).first()
    if db_file is not None:
        raise HTTPException(status_code=400, detail="Media File already exists")
    

    new_media = models.Media(
        link = destination_path ,
        user = id
    )

    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    
    return new_media



# delete media
@router.delete("/media_library/delete/{id}", tags=["Media Library"])
def delete_media_file(id: int, user_id:int = Depends(get_current_user)):
    media_to_delete=db.query(models.Media).filter((models.Media.id==id) & (models.Media.user == user_id)).first()
    
    if media_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Either the media file does not exist or you are not the owner of this media file")
    
    try:
        # before deleting media file, make the media attributes of all the posts containing that media file as null
        post_containing_media = db.query(models.Post).filter(models.Post.media_id == id).all()
        
        for i in range(len(post_containing_media)):
            post_containing_media[i].media_id == None
            
        db.delete(media_to_delete)
        db.commit()
        db.refresh(media_to_delete)
        
    except sqlalchemy.exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Media File deleted successfully")
    
    
    
    
