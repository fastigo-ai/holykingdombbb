from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://holykingdom:holykingdom123@holykingdom.hdhgjxk.mongodb.net/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "holykingdom")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

async def get_database():
    return db

# Collections
tc_collection = db["transfer_certificates"]
gallery_collection = db["gallery"]
admin_collection = db["admins"]
