from fastapi import FastAPI
from routes import router
from utils.database import test_mongodb_connection

app = FastAPI(title="Gemini 2.5 Flash Chatbot")

# Include the routes you defined in routes.py
app.include_router(router)

@app.on_event("startup")
async def startup_db_client():
    await test_mongodb_connection()

@app.get("/")
async def root():
    return {"message": "Chatbot is running and you can access it at http://127.0.0.1:8000/docs."}