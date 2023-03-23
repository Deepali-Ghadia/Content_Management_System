import os, shutil
from fastapi import APIRouter, UploadFile, File
from database import db
from passlib.context import CryptContext
from typing import List
import schemas, models


router = APIRouter()


# APIs for Media Library

# View all uploaded files
@router.get('/media_files', response_model=List[schemas.ShowMediaFile])
def show_all_media_files():
    files = db.query(models.Media).all()
    return files



# upload a file and add it to local directory
@router.post('/media_library', response_model=schemas.ShowMediaFile)
def upload_file(file: UploadFile = File(...)):  
    
    upload_dir = r"E:\Shubhchintak Technology Pvt. Ltd. (Internship)\Project\Content Management System\Coding Workspace\Content Management System\uploaded_files"
    
    # get the destination path
    destination_path = os.path.join(upload_dir, file.filename)
    print(destination_path)
    
    # copying file contents
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # wb means write and binary
    
    # # adding the locally stored file to the database
    # db_file = db.query(models.Media).filter(models.Media.link == file.filename).first()
    # if db_file is not None:
    #     raise HTTPException(status_code=400, detail="Media File already exists")
    
    # print(file.filename)
    # new_media = models.Media(
    #     link = file.filename
    # )

    # db.add(new_media)
    # db.commit()
    # db.refresh(new_media)
    
    return {"Result": "OK"}
