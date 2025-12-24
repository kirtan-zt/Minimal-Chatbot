from fastapi import APIRouter, HTTPException
from service import generate_chat_response
from utils.database import messages_collection
from bson import ObjectId
from models import ChatInput

router = APIRouter()

@router.post("/chat")
async def chat(data: ChatInput):
    """
    API endpoint to receive prompt and return the response from LLM
    """
    try:
        response_text = await generate_chat_response(data.session_id, data.prompt)
        return {"status": "success", "response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_chat(id: str):
    """Delete a conversation using ObjectID"""
    try:
        result = await messages_collection.find_one_and_delete({
            "_id": ObjectId(id)
        })
        if result:
            return {"status": "success", "message": "Message deleted"}
        raise HTTPException(status_code=404, detail="Message not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    