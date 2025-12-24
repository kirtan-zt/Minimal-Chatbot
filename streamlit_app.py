import streamlit as st
import requests
import uuid

# FastAPI Endpoint
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Gemini Chatbot", layout="centered")

st.title("🤖 Gemini AI Assistant")

# 1. Initialize Session State
if "session_id" not in st.session_state:
    """
    Ensures each browser tab has a unique session_id for your MongoDB logic
    """
    st.session_state.session_id = str(uuid.uuid4())

# Initialize local chat history to display in Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Input Logic
if prompt := st.chat_input("What is on your mind?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare payload for your FastAPI 'ChatInput' model
    payload = {
        "session_id": st.session_state.session_id,
        "prompt": prompt
    }

    # 4. Request to FastAPI
    with st.spinner("Generating response..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                bot_text = result.get("response")

                # Display bot response
                with st.chat_message("assistant"):
                    st.markdown(bot_text)
                
                # Update local history
                st.session_state.messages.append({"role": "assistant", "content": bot_text})
            else:
                st.error(f"Error: Received status code {response.status_code}")
        except Exception as e:
            st.error(f"Connection failed: {e}")