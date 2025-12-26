# db.py
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 sec timeout
    client.server_info()  # forces a connection to test it
    print("✅ MongoDB connected successfully")
except errors.ServerSelectionTimeoutError as err:
    print("❌ Could not connect to MongoDB:", err)
    client = None

if client:
    db = client["bluestudy"]
    tasks_collection = db["tasks"]
    users_collection = db["users"]
    flashcards_collection = db["flashcards"]
else:
    db = None
    tasks_collection = None
    users_collection = None
    flashcards_collection = None
    print("⚠️ Database collections are not initialized due to connection failure.")
