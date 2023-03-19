from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ShowUser(BaseModel):
    name: str
    username: str
    email_id: str
    
    class Config:
        orm_mode=True  
        
        
class ShowCategory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode=True  
            
        
        
class ShowPostByUser(BaseModel):
    id: int
    title: str
    description: str
    # posted_on: datetime
    is_featured: bool
    is_published: bool
    user: ShowUser # this is the relationship wala variable
 
    class Config:
        orm_mode = True
        
        
        
class CreateUser(BaseModel):
    name: str
    username: str
    mobile_number: str
    email_id: str
    password: str
    
    class Config:
        orm_mode = True
    
    
    
class ShowPost(BaseModel):
    title: str
    description: str
    
    class Config:
        orm_mode = True
    
    
    
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    mobile_number: str
    email_id: str
    password: str
    role: str
    posts: List
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True
        
        
        
class UpdateUser(BaseModel):
    username: str
    mobile_number: str
    password: str
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True
  
    
# Schemas for post  
class CreatePost(BaseModel):
    title: str
    description: str
    posted_by: int
    post_category: int

    class Config:
        orm_mode = True 
    
        
    
class ShowAllPost(BaseModel):
    id: int
    title: str
    description: str
    # posted_on: datetime
    is_featured: bool
    is_published: bool
    posted_by: int
    user: ShowUser
    category: ShowCategory
    
    class Config:
        orm_mode = True
        

    
class UpdatePost(BaseModel):
    title: str
    description: str
    # posted_on: datetime
    is_published: bool
    
    class Config:
        orm_mode = True
        
        
# Schemas for Category
class CreateCategory(BaseModel):
    name: str
    
    class Config:
        orm_mode=True
        
        
class Category(BaseModel):
    id: int
    name: str
    posts: List
    
    class Config:
        orm_mode=True
        
