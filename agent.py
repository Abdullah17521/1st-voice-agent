import os
from groq import Groq

# Read Groq API key from environment for safety
GROQ_REAL_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_REAL_KEY:
    print("Warning: GROQ_API_KEY not set in environment. Set it in .env or your shell.")
client = Groq(api_key=GROQ_REAL_KEY)

def ask_groq(user_text: str):
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise voice assistant. Give short, direct answers in 1 or 2 sentences max. Do not use bullet points, markdown, or asterisks (**)."
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            # Tasalli se check kiya hai, yeh model bilkul active hai
            model="llama-3.3-70b-versatile", 
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        # Terminal par print hoga taake agar koi naya error aaye toh pata chale
        print(f"Groq LLM Error in agent.py: {e}")
        return "Sorry, I couldn't process that request right now."