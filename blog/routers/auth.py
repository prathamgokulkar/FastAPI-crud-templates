from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schema, models, initDB
from ..hashing import Hash
from ..initDB import get_db
from datetime import timedelta
from .token import create_access_token

router = APIRouter(tags=['Auth'])

@router.post("/login")
def login( req: schema.Login, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not Hash.verify(user.password, req.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
 # Generate JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}