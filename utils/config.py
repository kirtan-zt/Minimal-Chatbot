import os
import time
from dotenv import load_dotenv
from google import genai
from loguru import logger

# Load environment variables once when this module is imported
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DEFAULT_MODEL = 'gemini-2.5-flash'