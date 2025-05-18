import streamlit as st
import google.generativeai as genai
import fitz

# Set page config
st.set_page_config(page_title="Gemini PDF Chatbot", page_icon="🤖", layout="centered")

# --- HTML/CSS + Dark Mode Toggle ---
dark_mode = st.toggle("🌙 Dark Mode", value=False)

st.markdown(f"""
    <style>
        body {{
            background-color: {"#0e1117" if dark_mode else "#f4f6f8"};
            color: {"#f0f0f0" if dark_mode else "#000"};
            font-family: 'Segoe UI', sans-serif;
        }}
        h1 {{
            text-align: center;
            color: {"#dcdcdc" if dark_mode else "#2c3e50"};
        }}
        .pdf-preview {{
            background-color: {"#1c1c1c" if dark_mode else "#ffffff"};
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            color: {"#f0f0f0" if dark_mode else "#000"};
        }}
        .chat-box {{
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            font-size: 1rem;
        }}
        .chat-user {{
            background-color: {"#3a3b3c" if dark_mode else "#dff9fb"};
            color: {"#fff" if dark_mode else "#000"};
        }}
        .chat-assistant {{
            background-color: {"#2c2f33" if dark_mode else "#f1f2f6"};
            color: {"#fff" if dark_mode else "#000"};
        }}
    </style>
""", unsafe_allow_html=True)

# --- Gemini Setup ---
genai.configure(api_key="AIzaSyDtcV4YqBQYtu7tUsJwk8R-NSremm1Z2NA")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Session State ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    st.session_state.pdf_text_pages = []

# --- Title ---
st.title("📄 Gemini PDF Chatbot 🤖")

# --- File Upload ---
uploaded_pdf = st.file_uploader("📤 Upload a PDF file", type="pdf")

# --- PDF Processing ---
if uploaded_pdf:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    pages = [doc.load_page(p).get_text() for p in range(len(doc))]
    st.session_state.pdf_text_pages = pages

    page_options = [f"Page {i+1}" for i in range(len(pages))]
    selected_page = st.selectbox("📃 Select PDF Page to Ask From", page_options)

    selected_page_num = int(selected_page.split()[-1]) - 1
    st.markdown(f"<div class='pdf-preview'><strong>📄 Page Preview:</strong><br>{pages[selected_page_num][:1000]}</div>", unsafe_allow_html=True)

# --- Display Previous Messages ---
for msg in st.session_state.messages:
    role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
    st.markdown(f"<div class='chat-box {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# --- User Input ---
user_input = st.chat_input("Ask something related to the selected page...")

if user_input and uploaded_pdf:
    st.markdown(f"<div class='chat-box chat-user'>{user_input}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    page_text = st.session_state.pdf_text_pages[selected_page_num][:2000]

    prompt = (
        "You are a helpful assistant specialized in Data Science only. "
        "You must answer **only** questions related to Data Science topics (e.g., Machine Learning, Statistics, Data Analysis, etc.). "
        "If a question is outside the scope of Data Science, politely respond with: "
        "'Sorry, I can only answer questions related to Data Science.'\n\n"
        f"{page_text}\n\nUser query: {user_input}"
    )

    try:
        response = st.session_state.chat.send_message(prompt)
        answer = response.text
    except Exception as e:
        answer = f"❌ Error: {e}"

    st.markdown(f"<div class='chat-box chat-assistant'>{answer}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": answer})
