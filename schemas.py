from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    name: str
    username: str
    mobile_number: int
    email_id: str
    password: str
    
    class Config:
        orm_mode = True
    
    
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    mobile_number: int
    email_id: str
    password: str
    role: str
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True
        
        
class UpdateUser(BaseModel):
    username: str
    mobile_number: int
    password: str
    profile_photo: Optional[int] = None
    bio: Optional[str] = None