# 1st Voice Agent

A small voice-based voice agent built on Groq Cloud and Microsoft Edge TTS. The repository includes:

- `main.py` — local microphone voice assistant with `speech_recognition`, `pygame`, and `edge-tts`
- `app.py` — a Streamlit web UI version with audio upload, transcription, and browser playback
- `agent.py` — Groq client wrapper for chat completions
- `voice_agent.py` / `test_tts.py` — helper scripts for offline TTS and voice testing

## Features
- Local microphone speech input via `SpeechRecognition`
- Voice response generation through Groq Cloud (`llama-3.3-70b-versatile`)
- Natural-sounding text-to-speech using `edge-tts`
- Optional Streamlit web interface for browser voice interactions

## Requirements
- Python 3.10+
- Windows recommended for microphone and audio playback support

## Installation
1. Clone the repo:

```bash
git clone https://github.com/Abdullah17521/1st-voice-agent.git
cd 1st-voice-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example and add your Groq API key:

```bash
copy .env.example .env
```

Then set:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Run the local voice assistant

```bash
python main.py
```

### Run the Streamlit web interface

```bash
streamlit run app.py
```

## Notes
- Keep `.env` private; `GROQ_API_KEY` should never be committed.
- `requirements.txt` includes the packages needed for both local and Streamlit use.

## License
Project code — see repository for license details.
