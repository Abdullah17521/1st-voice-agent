import streamlit as st
from agent import ask_groq
import edge_tts
import asyncio
import base64
import re
from groq import Groq
import os
from dotenv import load_dotenv

# Environmental parameters load karein
load_dotenv()

# Page configurations
st.set_page_config(page_title="AI Voice Agent", page_icon="🎙️", layout="centered")

st.title("🎙️ GPT-Style Web Voice Agent")
st.write("Powered by Groq Cloud (Llama 3.3 & Whisper) & Edge-TTS")
st.write("---")

# Safe Environment checklist
GROQ_REAL_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_REAL_KEY:
    st.error("⚠️ GROQ_API_KEY is missing! App will fail. Setup your key in your Local .env file or Streamlit Secrets panel.")
    st.stop()

# Initialize groq client with verified token
groq_client = Groq(api_key=GROQ_REAL_KEY)

# Session state initialization for chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

def clean_text(text):
    return re.sub(r'[\*\#\_\-\[\]\(\)\{\}]', '', text)

# Edge-TTS Async Function to generate audio for browser player
async def generate_audio_b64(text):
    clean_to_speak = clean_text(text).strip()
    if not clean_to_speak:
        return None
    
    voice = "en-US-GuyNeural"
    communicate = edge_tts.Communicate(clean_to_speak, voice)
    
    audio_bytes = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
            
    return base64.b64encode(audio_bytes).decode()

# Render historical messages on refresh
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- USER INPUT CONTROLS ---
st.write("### Interact with Agent")

audio_input = st.audio_input("Record your voice query:")
text_input = st.chat_input("Or type your question here...")

user_query = ""

# Automatically Transcribe Audio if Captured
if audio_input is not None:
    audio_bytes = audio_input.read()
    
    if audio_bytes:
        with st.spinner("Transcribing your voice... 🎙️"):
            try:
                file_tuple = ("audio.wav", audio_bytes, "audio/wav")
                transcription = groq_client.audio.transcriptions.create(
                    file=file_tuple,
                    model="whisper-large-v3", 
                    language="en",
                    response_format="text"
                )
                user_query = transcription.strip()
                
            except Exception as e:
                st.error(f"Speech-to-Text Error: {e}")

# Handle Text Input (Fallback)
if text_input:
    user_query = text_input

# Main execution trigger
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(f"**You Said:** {user_query}")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = ask_groq(user_query)
            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            try:
                audio_b64 = asyncio.run(generate_audio_b64(response_text))
                if audio_b64:
                    audio_html = f"""
                        <audio autoplay class="stAudio">
                        <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                        </audio>
                    """
                    st.components.v1.html(audio_html, height=0)
            except Exception as e:
                st.error(f"Audio Playback Error: {e}")

with st.sidebar:
    st.header("Voice Agent Dashboard")
    st.success("Secure pipeline configured! Ready for secure deployment.")