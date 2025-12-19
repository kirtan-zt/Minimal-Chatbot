import os
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import Config

# Initialize the client
client = AsyncIOMotorClient(Config.MONGO_URL)

# Access the specific database
db = client.chatbot_db 

# Access the collections
# We define them here so they can be imported directly into service.py
messages_collection = db.get_collection("messages")
sessions_collection = db.get_collection("sessions")

async def test_mongodb_connection():
    """Utility function to verify the connection on startup"""
    try:
        # The 'ping' command is cheap and confirms the server is reachable
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")