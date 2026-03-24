from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from db import tc_collection
from cloudinary_config import upload_pdf, delete_file_from_cloudinary
import datetime
from pydantic import BaseModel
from typing import Optional, List
import os
from bson import ObjectId

router = APIRouter(prefix="/tc", tags=["Transfer Certificate"])

class TCRecord(BaseModel):
    id: str
    admission_no: str
    student_name: str
    issue_date: str
    document_url: str

@router.get("", response_model=List[dict])
async def list_tcs():
    tcs = []
    cursor = tc_collection.find({})
    async for tc in cursor:
        tc["_id"] = str(tc["_id"])
        tcs.append(tc)
    return tcs

@router.get("/{admission_no}")
async def get_tc(admission_no: str):
    tc = await tc_collection.find_one({"admission_no": admission_no})
    if not tc:
        raise HTTPException(status_code=404, detail="Transfer Certificate not found for this Admission No.")
    # Convert MongoDB _id to string
    tc["_id"] = str(tc["_id"])
    return tc

@router.delete("/{tc_id}")
@router.delete("/{tc_id}/")
async def delete_tc(tc_id: str):
    try:
        obj_id = ObjectId(tc_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid TC ID format")
    
    tc_record = await tc_collection.find_one({"_id": obj_id})
    if not tc_record:
        raise HTTPException(status_code=404, detail="TC record not found")
        
    document_url = tc_record.get("document_url")
    if document_url:
        delete_file_from_cloudinary(document_url)
        
    result = await tc_collection.delete_one({"_id": obj_id})
    return {"message": "TC deleted successfully"}

@router.post("/upload")
async def upload_tc(
    admission_no: str, 
    student_name: str, 
    file: UploadFile = File(...)
):
    # Upload to Cloudinary
    # In a real app, you'd save the file locally first or use a buffer
    # Since we can't easily handle multi-part file buffers without writing to disk here:
    temp_path = f"tmp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        result = upload_pdf(temp_path)
        doc_url = result.get("secure_url")
        
        tc_data = {
            "admission_no": admission_no,
            "student_name": student_name,
            "document_url": doc_url,
            "issue_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.datetime.now()
        }
        
        await tc_collection.update_one(
            {"admission_no": admission_no},
            {"$set": tc_data},
            upsert=True
        )
        return {"message": "TC uploaded successfully", "url": doc_url}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
