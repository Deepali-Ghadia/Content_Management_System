from pydantic import BaseModel
from typing import Optional, List, BinaryIO
from datetime import datetime

class ShowCategory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode=True  
    
    
    
class ShowUser(BaseModel):
    name: str
    username: str
    email_id: str
    
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
    role: str
    posts: List
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    password: str
    
    class Config:
        orm_mode = True
        
        
        
class UpdateUser(BaseModel):
    username: str
    mobile_number: str
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True
  
    
# Schemas for post  
class CreatePost(BaseModel):
    title: str
    description: str
    post_category: int
    media_id: Optional[int]= None

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
    media_id: Optional[int]= None
    
    class Config:
        orm_mode = True
        

    
class UpdatePost(BaseModel):
    title: str
    description: str
    # posted_on: datetime
    is_published: bool
    category: int
    media_id: Optional[int]= None
    
    class Config:
        orm_mode = True
 
 
class ShowPost(BaseModel):
    id: int
    title: str
    description: str
    # posted_on: datetime
    is_featured: bool
    is_published: bool
    posted_by: int
    user: ShowUser
    category: ShowCategory
    comments: List
    media_id: Optional[int]= None
    
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
   
   
     
# Upload File
class UploadMediaFile(BaseModel):
    link: str
    

    
class ShowMediaFile(BaseModel):
    id: int
    link: str
    
    class Config:
        orm_mode=True
        


# Schema for adding comments
class AddComment(BaseModel):
    description: str

    
    class Config:
        orm_mode=True
        
        
class ShowComment(BaseModel):
    id: int
    post_id : int
    description: str
    commenter: ShowUser
    is_approved: bool
    
    class Config:
        orm_mode=True
        
        
        
class ShowFeaturedPosts(BaseModel):
    id: int
    title: str
    description: str
    # posted_on: datetime
    is_featured: bool
    # is_published: bool
    # posted_by: int
    user: ShowUser
    category: ShowCategory
    # media_id: Optional[int]= None
    # comments: List
    
    class Config:
        orm_mode = True 
        
        
        
class ListCategory(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        
        
        
class SearchByCategory(BaseModel):
    id: int
    name: str
    posts: List
    
    class Config:
        orm_mode = True
        
        
class ChangeRole(BaseModel):
    role: str
    
    class Config:
        orm_mode = True
    
    
class Login(BaseModel):
    username: str
    password: str
    
    class Config:
        orm_mode = True
        
        
class TokenData(BaseModel):
    username: Optional[str]= None
    
    class Config:
        orm_mode = True