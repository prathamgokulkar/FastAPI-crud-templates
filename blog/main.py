from fastapi import FastAPI, Depends, status, HTTPException
from . import schema, models
from .initDB import engine, get_db
from sqlalchemy.orm import Session, joinedload
from typing import List
from .hashing import Hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create a blog post
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'], response_model=schema.ShowBlog)
def create_blog_post(req: schema.BlogPost, db: Session = Depends(get_db)):
    # Validate user exists
    user = db.query(models.User).filter(models.User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    new_blog = models.BlogPost(
        title=req.title,
        content=req.content,
        user_id=req.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blog posts
@app.get("/blog", response_model=List[schema.ShowBlog], tags=['Blog'])
def get_blog_post(db: Session = Depends(get_db)):
    blog_posts = db.query(models.BlogPost).options(joinedload(models.BlogPost.creator)).all()
    return blog_posts


# Get a blog post by ID
@app.get("/blog/{blog_id}", response_model=schema.ShowBlog, tags=['Blog'])
def get_blog_post_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).options(joinedload(models.BlogPost.creator)) \
        .filter(models.BlogPost.id == blog_id).first()

    if not blog_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    return blog_post

#Update a blog post
@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK, tags = ['Blog'])
def update_blog_post(blog_id: int, req: schema.BlogPost, db: Session = Depends(get_db)):
    updated_blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id)
    if not updated_blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    updated_blog.update({"title": req.title, "content": req.content}, synchronize_session = False)
    db.commit()

#Delete a blog post
@app.delete("/blog/{blog_id}", status_code = status.HTTP_204_NO_CONTENT, tags = ['Blog'])
def delete_blog_post(blog_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).delete(synchronize_session=False)
    if not blog_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    db.commit()
    return {"detail": "Blog post deleted successfully"}

# Create new User
@app.post("/user", status_code=status.HTTP_201_CREATED, tags=['User'], response_model=schema.ShowUser)
def create_user(req: schema.User, db: Session = Depends(get_db)):
    new_user = models.User(
        username=req.username,
        email=req.email,
        password=Hash.bcrypt(req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Show all users
@app.get("/user", response_model=List[schema.ShowUser], tags=['User'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
