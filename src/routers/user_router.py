from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import user_schema
from src.models import user_model
from src.utils import utils
from src import database
from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
def register(user: user_schema.UserCreate, db: Session = Depends(database.get_db)):
    typed_user = db.query(user_model.User).filter(user_model.User.username == user.username).first()
    if typed_user:
        raise HTTPException(status_code=400, detail="The user cannot be used")

    hashed_pw = utils.hash_password(user.password)

    new_user = user_model.User(
        username=user.username,
        password_hash=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(database.get_db)):
    typed_user = db.query(user_model.User).filter(user_model .User.username == user.username).first()
    if not typed_user or not utils.verify_password(user.password, typed_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not typed_user.is_enabled:
        raise HTTPException(status_code=403, detail="User is disabled")

    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = utils.create_access_token(
        data={"sub":  user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
