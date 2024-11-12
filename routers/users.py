from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import user_collection
import logging
from typing import List
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class User(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    points: int = 0
    
@router.get("/{telegram_id}")
async def get_user(telegram_id: int):
    user = await user_collection.find_one({"telegram_id": telegram_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # PARSE OBJECTID to STRING
    user['_id'] = str(user['_id'])
    
    return user

@router.post("/register")
async def create_user(user: User):
    # CHECK IS USER EXISTS
    existing_user = await user_collection.find_one({"telegram_id": user.telegram_id})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_data = user.dict()
    result = await user_collection.insert_one(user_data)
    if result.inserted_id:
        return {"message": "User successfully created"}
    raise HTTPException(status_code=400, detail="User could not be created")
