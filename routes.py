from fastapi import APIRouter
from service import generate_chat_response
from utils.database import messages_collection
from bson import ObjectId
from models import ChatInput

router = APIRouter()

@router.post("/chat")
async def chat(data: ChatInput):
    response_text = await generate_chat_response(data.session_id, data.prompt)
    return {"status": "success", "response": response_text}

@router.delete("/{id}")
async def delete_chat(id: str):
    messages_collection.find_one_and_delete({
        "_id": ObjectId(id)
    })