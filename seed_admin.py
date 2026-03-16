import asyncio
import os
from dotenv import load_dotenv
from db import admin_collection
from routes.auth import get_password_hash

load_dotenv()

async def fetch_or_create_admin():
    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "holykingdom123")
    
    hashed_pw = get_password_hash(ADMIN_PASSWORD)

    existing_admin = await admin_collection.find_one({"username": ADMIN_USER})
    if existing_admin:
        print(f"Admin user '{ADMIN_USER}' already exists in database.")
        await admin_collection.update_one(
            {"username": ADMIN_USER},
            {"$set": {"password": hashed_pw}}
        )
        print(f"Updated password for '{ADMIN_USER}'.")
    else:
        new_admin = {
            "username": ADMIN_USER,
            "password": hashed_pw
        }
        await admin_collection.insert_one(new_admin)
        print(f"Successfully created admin user '{ADMIN_USER}' in database.")

if __name__ == "__main__":
    asyncio.run(fetch_or_create_admin())
