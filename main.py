from fastapi import FastAPI, status, HTTPException
from typing import List
from database import SessionLocal
import schemas 
import models

app = FastAPI()

db=SessionLocal() 

# view all users
@app.get('/users', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_users():
    users=db.query(models.User).all()
    return users

# register a user
@app.post('/users/register', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.CreateUser):
    # db_user = db.query(models.User).filter(models.User.id == user.id).first()
    # if db_user is not None:
    #     raise HTTPException(status_code=400, detail="User account already exists")
    
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