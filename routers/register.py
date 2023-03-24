from fastapi import APIRouter, status, HTTPException, Depends
from database import db
from passlib.context import CryptContext
import schemas, models

router = APIRouter(prefix="/register")


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# register a user
@router.post('/register', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Register"])

def register_user(user: schemas.CreateUser):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User account already exists")
    
    hashed_password = password_context.hash(user.password)
    
    new_user = models.User(
        name= user.name,
        username= user.username,
        mobile_number= user.mobile_number,
        email_id= user.email_id,
        password= hashed_password
        # alternative to this statement
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
