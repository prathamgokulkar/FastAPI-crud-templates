from fastapi import FastAPI,Depends, status, HTTPException
from . import schema, models
from .initDB import engine
from sqlalchemy.orm import Session
from .initDB import get_db


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

#Create a blog post
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog_post(req: schema.BlogPost, db: Session = Depends(get_db)):
    new_blog = models.BlogPost(title=req.title, content=req.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#Get all blog posts
@app.get("/blog")
def get_blog_post(db:Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).all()
    return blog_post

#Get a blog post by ID
@app.get("/blog/{blog_id}")
def get_blog_post_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).first()

    if not blog_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    
    return blog_post

#Update a blog post
@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def update_blog_post(blog_id: int, req: schema.BlogPost, db: Session = Depends(get_db)):
    updated_blog = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id)
    if not updated_blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    updated_blog.update({"title": req.title, "content": req.content}, synchronize_session = False)
    db.commit()

#Delete a blog post
@app.delete("/blog/{blog_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_blog_post(blog_id: int, db: Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == blog_id).delete(synchronize_session=False)
    if not blog_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Blog post with id {blog_id} is not available")
    db.commit()
    return {"detail": "Blog post deleted successfully"}
