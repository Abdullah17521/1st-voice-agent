import speech_recognition as sr
from agent import ask_groq
import pygame
import asyncio
import edge_tts
import io
import re

# Pygame mixer ko aik hi dafa shuru mein initialize karein
pygame.mixer.init()

def clean_text(text):
    # Markdown aur asterisks saaf karne ke liye
    return re.sub(r'[\*\#\_\-\[\]\(\)\{\}]', '', text)

# Edge-TTS se audio stream generate kar ke play karne ka function
def speak(text):
    clean_to_speak = clean_text(text).strip()
    if not clean_to_speak:
        return

    print("\nAgent:", clean_to_speak)

    try:
        # Microsoft Edge ki bohot hi pyari natural voice (Guy ya Michelle use kar sakte hain)
        voice = "en-US-GuyNeural" 
        
        # Async task ko sync wrapper mein chalane ka tareeqa
        communicate = edge_tts.Communicate(clean_to_speak, voice)
        
        # Audio data ko memory (bytes) mein stream karein, disk par file save nahi hogi!
        audio_data = b""
        for chunk in communicate.stream_sync():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]

        # Memory stream se direct pygame mein play karein (No File Lock Issue)
        sound_file = io.BytesIO(audio_data)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        # Jab tak bol raha hai wait karein
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()

    except Exception as e:
        print("Edge-TTS Playback Error:", e)

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.6 # Fast capture

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=8)

        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text

    except (sr.WaitTimeoutError, sr.UnknownValueError):
        return None
    except Exception as e:
        print("Mic Error:", e)
        return None

def main():
    print("=== ULTRA-STABLE REAL-TIME VOICE AGENT (EDGE-TTS) ===")
    speak("Hello Abdullah. I am completely ready now. Ask me anything!")

    while True:
        try:
            user_text = listen()

            if not user_text:
                continue

            if user_text.lower() in ["exit", "quit", "stop"]:
                speak("Goodbye Abdullah.")
                break

            # Use the Groq-based ask function (returns full text)
            full_response = ask_groq(user_text)
            if not full_response:
                continue

            print("\nAgent Writing:", full_response)
            speak(full_response)

        except KeyboardInterrupt:
            print("\nStopping Agent...")
            break
        except Exception as e:
            print("Loop Error:", e)

if __name__ == "__main__":
    main()