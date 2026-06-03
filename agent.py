import os
from dotenv import load_dotenv
from groq import Groq

# Local testing ke liye `.env` file se keys load karein
load_dotenv()

# Streamlit Cloud ya local env dono se automatically key dhoondega
GROQ_REAL_KEY = os.environ.get("GROQ_API_KEY")

def ask_groq(user_text: str):
    if not GROQ_REAL_KEY:
        return "Error: GROQ_API_KEY is missing. Please configure it in environment secrets."
        
    try:
        # Dynamic client init taake deployment par keys refresh ho sakein
        client = Groq(api_key=GROQ_REAL_KEY)
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise voice assistant. Give short, direct answers in 1 or 2 sentences max. Do not use bullet points, markdown, or asterisks."
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq LLM Error: {e}")
        return "Sorry, I couldn't process that request right now."