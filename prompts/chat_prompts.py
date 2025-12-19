def get_chat_system_prompt():
    return (
        "You are a helpful and knowledgeable AI assistant. "
        "Use the provided conversation history to maintain context, "
        "but if the information isn't there, use your own general knowledge to answer."
    )