import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(file_path, folder="holy_kingdom"):
    return cloudinary.uploader.upload(file_path, folder=folder)

def upload_pdf(file_path, folder="holy_kingdom/docs"):
    return cloudinary.uploader.upload(file_path, folder=folder, resource_type="raw")
