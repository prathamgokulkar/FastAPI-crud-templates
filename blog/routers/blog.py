from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema, models
from typing import List
from sqlalchemy.orm import Session
from ..initDB import get_db
from .token import get_current_user

router = APIRouter()

# Get all blog posts
@router.get("/blog", response_model=List[schema.ShowBlog], tags=['Blog'])
def get_blog_post(db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    blog_posts = db.query(models.BlogPost).filter(models.BlogPost.user_id == current_user.id).all()
    return blog_posts


# Create a blog post
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'], response_model=schema.ShowBlog)
def create_blog_post(req: schema.BlogPost, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)
):
    # Validate user exists
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    new_blog = models.BlogPost(
        title=req.title,
        content=req.content,
        user_id=current_user.id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get a blog post by ID
@router.get("/blog/{blog_id}", response_model=schema.ShowBlog, tags=['Blog'])
def get_blog_post_by_id(blog_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):

    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).first()

    if not blog_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    return blog_post

#Update a blog post
@router.put("/blog/{blog_id}", status_code=status.HTTP_200_OK, tags = ['Blog'])
def update_blog_post(blog_id: int, req: schema.BlogPost, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    
    updated_blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id, models.BlogPost.user_id == current_user.id)

    if not updated_blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    
    updated_blog.update({"title": req.title, "content": req.content}, synchronize_session = False)
    db.commit()

#Delete a blog post
@router.delete("/blog/{blog_id}", status_code = status.HTTP_204_NO_CONTENT, tags = ['Blog'])
def delete_blog_post(blog_id: int, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):

    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id, models.BlogPost.user_id == current_user.id).delete(synchronize_session=False)

    if not blog_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    db.commit()
    return {"detail": "Blog post deleted successfully"}