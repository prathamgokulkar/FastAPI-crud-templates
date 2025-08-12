from fastapi import FastAPI,Depends
from . import schema, models
from .initDB import engine
from sqlalchemy.orm import Session
from .initDB import get_db


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/blog")
def create_blog_post(req: schema.BlogPost, db: Session = Depends(get_db)):
    new_blog = models.BlogPost(title=req.title, content=req.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def get_blog_post(db:Session = Depends(get_db)):
    blog_post = db.query(models.BlogPost).all()
    return blog_post
