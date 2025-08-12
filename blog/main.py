from fastapi import FastAPI
from . import schema

app = FastAPI()


@app.post("/blog")
def create_blog_post(req: schema.BlogPost):
    return "create blog post"