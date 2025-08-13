from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .initDB import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship to User
    creator = relationship("User", back_populates="blog_posts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to BlogPost
    blog_posts = relationship("BlogPost", back_populates="creator")
