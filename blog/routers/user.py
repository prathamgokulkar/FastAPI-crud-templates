from fastapi import APIRouter, Depends, status, HTTPException
from .. import schema, models
from typing import List
from sqlalchemy.orm import Session
from ..initDB import get_db
from ..hashing import Hash


router = APIRouter()

# Create new User
@router.post("/user", status_code=status.HTTP_201_CREATED, tags=['User'], response_model=schema.ShowUser)
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
@router.get("/user", response_model=List[schema.ShowUser], tags=['User'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
