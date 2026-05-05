from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from db import blog_collection
from cloudinary_config import upload_image
import datetime
import os
from bson import ObjectId
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/blogs", tags=["Blogs"])

class BlogBase(BaseModel):
    title: str
    excerpt: str
    content: str
    author: str
    category: str
    readTime: str

@router.get("/")
async def get_blogs():
    cursor = blog_collection.find().sort("created_at", -1)
    blogs = await cursor.to_list(length=100)
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
    return blogs

@router.get("/{blog_id}")
async def get_blog(blog_id: str):
    try:
        obj_id = ObjectId(blog_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Blog ID")
    
    blog = await blog_collection.find_one({"_id": obj_id})
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    blog["_id"] = str(blog["_id"])
    return blog

@router.post("/")
async def create_blog(
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    category: str = Form(...),
    readTime: str = Form(...),
    file: UploadFile = File(...)
):
    temp_path = f"tmp_blog_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        result = upload_image(temp_path)
        img_url = result.get("secure_url")
        
        blog_data = {
            "title": title,
            "excerpt": excerpt,
            "content": content,
            "author": author,
            "category": category,
            "readTime": readTime,
            "image": img_url,
            "date": datetime.datetime.now().strftime("%B %d, %Y"),
            "created_at": datetime.datetime.now()
        }
        
        result = await blog_collection.insert_one(blog_data)
        return {"message": "Blog created successfully", "id": str(result.inserted_id)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.delete("/{blog_id}")
async def delete_blog(blog_id: str):
    try:
        obj_id = ObjectId(blog_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Blog ID")
    
    result = await blog_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return {"message": "Blog deleted successfully"}

@router.put("/{blog_id}")
async def update_blog(
    blog_id: str,
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    category: str = Form(...),
    readTime: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        obj_id = ObjectId(blog_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Blog ID")
    
    update_data = {
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "author": author,
        "category": category,
        "readTime": readTime,
    }
    
    if file:
        temp_path = f"tmp_update_{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        try:
            result = upload_image(temp_path)
            update_data["image"] = result.get("secure_url")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    result = await blog_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return {"message": "Blog updated successfully"}
