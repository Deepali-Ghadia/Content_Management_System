from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    mobile_number = Column(String(10), nullable=True)
    email_id = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=True, default="author")
    bio = Column(Text, nullable=True)
    
    profile_photo = Column(Integer, ForeignKey("media_files.id"))
    profile = relationship("Media", foreign_keys=[profile_photo])
    
    posts = relationship("Post", back_populates="user")
    # user_medias = relationship("Media", back_populates="media_user")
    user_comments = relationship("Comment", back_populates="commenter")
    
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    # posted_on = Column(DateTime, default=func.now())
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    
    posted_by = Column(Integer, ForeignKey("users.id"))
    post_category = Column(Integer, ForeignKey("categories.id"))
    media_id = Column(Integer, ForeignKey("media_files.id"))
    
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    medias = relationship("Media", back_populates="posts_medias")
    comments = relationship("Comment", back_populates="post")
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    
    posts = relationship("Post", back_populates="category")
    
    
class Media(Base):
    __tablename__ = "media_files"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    link = Column(String(255), nullable=False)
    
    posts_medias = relationship("Post", back_populates="medias")
    # media_user = relationship("User", back_populates="user_medias")

    owner = relationship("User", foreign_keys=[user], backref="media_files")
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=False)
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    commented_by = Column(Integer, ForeignKey("users.id"))
    
    post = relationship("Post", back_populates="comments")
    commenter = relationship("User", back_populates="user_comments")
    