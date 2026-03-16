from fastapi import APIRouter, HTTPException, UploadFile, File
from db import gallery_collection
from cloudinary_config import upload_image
import datetime
import os

router = APIRouter(prefix="/gallery", tags=["Gallery"])

@router.get("/")
async def get_gallery():
    cursor = gallery_collection.find().sort("created_at", -1)
    images = await cursor.to_list(length=100)
    for img in images:
        img["_id"] = str(img["_id"])
    return images

@router.post("/upload")
async def add_image(
    title: str, 
    category: str = "general", 
    file: UploadFile = File(...)
):
    temp_path = f"tmp_img_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        result = upload_image(temp_path)
        img_url = result.get("secure_url")
        
        img_data = {
            "title": title,
            "category": category,
            "url": img_url,
            "created_at": datetime.datetime.now()
        }
        
        await gallery_collection.insert_one(img_data)
        return {"message": "Image added to gallery", "url": img_url}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
