from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    mobile_number = Column(Integer, nullable=True)
    email_id = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(String(10), nullable=True, default="author")
    profile_photo = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)
    
    posts = relationship("Post", back_populates="user")
    user_medias = relationship("Media", back_populates="media_user")
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    # posted_on = Column(datetime, nullable=True, default=datetime)
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    
    posted_by = Column(Integer, ForeignKey("users.id"))
    post_category = Column(Integer, ForeignKey("categories.id"))
    media_id = Column(Integer, ForeignKey("media_files.id"))
    
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="post")
    medias = relationship("Media", back_populates="posts_medias")
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    
    post = relationship("Post", back_populates="category")
    
    
class Media(Base):
    __tablename__ = "media_files"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    link = Column(String(255), nullable=False)
    
    posts_medias = relationship("Post", back_populates="medias")
    media_user = relationship("User", back_populates="user_medias")