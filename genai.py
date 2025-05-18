import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key="AIzaSyDtcV4YqBQYtu7tUsJwk8R-NSremm1Z2NA")

# Load the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize chat and session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Gemini AI Chatbot")

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input from user
user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get assistant response
    try:
        response = st.session_state.chat.send_message(user_input)
        answer = response.text
    except Exception as e:
        answer = f"Error: {str(e)}"

    # Show assistant response
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})