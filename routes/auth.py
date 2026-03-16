from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
import bcrypt
from db import admin_collection
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    admin_user = await admin_collection.find_one({"username": req.username})
    if not admin_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(req.password, admin_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {"message": "Login successful", "token": "mock-jwt-token"}
