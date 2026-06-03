import speech_recognition as sr
import pyttsx3
from agent import ask_groq

engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text):
    print("\nAgent:", text)
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS Error:", e)

# ---------- SPEECH TO TEXT ----------
def listen():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            audio = r.listen(source, timeout=6, phrase_time_limit=12)

        text = r.recognize_google(audio)
        print("You:", text)
        return text

    except sr.WaitTimeoutError:
        print("No speech detected...")
        return None
    except sr.UnknownValueError:
        print("Could not understand...")
        return None
    except Exception as e:
        print("Mic Error:", e)
        return None

# ---------- MAIN LOOP ----------
def main():
    print("=== AI VOICE AGENT STARTED ===")
    speak("Hello, I am your AI voice assistant.")

    while True:
        user_text = listen()
        if not user_text:
            continue

        try:
            response = ask_groq(user_text)
            speak(response)
        except Exception as e:
            print("Error:", e)
            speak("Sorry, something went wrong")

if __name__ == "__main__":
    main()