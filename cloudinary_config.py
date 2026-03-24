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

def delete_file_from_cloudinary(file_url: str):
    try:
        parts = file_url.split("/upload/")
        if len(parts) == 2:
            resource_type = "raw" if "/raw/" in parts[0] else "image"
            path_after_upload = parts[1]
            path_parts = path_after_upload.split("/")
            
            if path_parts[0].startswith("v") and path_parts[0][1:].isdigit():
                public_id_with_ext = "/".join(path_parts[1:])
            else:
                public_id_with_ext = path_after_upload
            
            if resource_type == "image":
                public_id = public_id_with_ext.rsplit(".", 1)[0]
            else:
                public_id = public_id_with_ext
                
            cloudinary.uploader.destroy(public_id, resource_type=resource_type)
    except Exception as e:
        print(f"Cloudinary deletion error: {e}")
