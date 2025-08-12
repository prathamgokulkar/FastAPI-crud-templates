from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/about")
def about():
    return {"About": "This is a sample FastAPI application."}

@app.get("/items/{id}")
def read_item(id: int):
    return {"item_id": id, "description": "This is an item."}


@app.get("/items/{id}/comments")
def read_item(id: int):
    return {"item_id": id, "comment": "This is a comment."}

class Item(BaseModel):
    name:str
    description: str = None


@app.post("/items/")
def create_item(item: Item):
    return {"item_name":item.name, "item_description": item.description}