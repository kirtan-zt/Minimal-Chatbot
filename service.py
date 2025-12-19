from google import genai
from utils.config import Config
from utils.database import messages_collection
from prompts.chat_prompts import get_chat_system_prompt
import datetime

client = genai.Client(api_key=Config.GEMINI_API_KEY)

async def generate_chat_response(session_id: str, user_prompt: str):
    # Fetch Chat History (e.g., last 10 messages)
    # We sort by timestamp descending to get newest, then reverse to keep order
    cursor = messages_collection.find({"session_id": session_id}).sort("timestamp", -1).limit(10)
    history_docs = await cursor.to_list(length=10)
    history_docs.reverse() # Put them back in chronological order

    # Format history for Gemini SDK
    # Gemini expects a list of dicts with 'role' and 'parts'
    formatted_history = []
    for doc in history_docs:
        # Map our roles to Gemini roles ('assistant' becomes 'model')
        role = "model" if doc["role"] == "assistant" else "user"
        formatted_history.append({"role": role, "parts": [{"text": doc["content"]}]})

    # 3. Save the CURRENT user message to DB
    user_doc = {
        "session_id": session_id,
        "role": "user",
        "content": user_prompt,
        "timestamp": datetime.datetime.utcnow()
    }
    await messages_collection.insert_one(user_doc)

    # 4. Call Gemini with Context
    # We add the new prompt as the final message in the conversation
    response = client.models.generate_content(
        model=Config.DEFAULT_MODEL,
        contents=formatted_history + [{"role": "user", "parts": [{"text": user_prompt}]}],
        config={
            "system_instruction": get_chat_system_prompt(),
            "temperature": 0.7
        }
    )
    bot_text = response.text

    # 5. Save Bot Response to DB
    bot_doc = {
        "session_id": session_id,
        "role": "assistant",
        "content": bot_text,
        "timestamp": datetime.datetime.utcnow()
    }
    await messages_collection.insert_one(bot_doc)

    return bot_text