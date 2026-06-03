# 1st Voice Agent

A small voice-based agent that uses SpeechRecognition for speech input, Gemini (via `agent.ask_gemini`) for responses, and Microsoft Edge TTS (`edge-tts`) for speech output. Plays audio locally with `pygame`.

## Features
- Live microphone input via `speech_recognition` (requires PyAudio)
- Streaming text responses from the `ask_gemini` agent
- Natural-sounding TTS via `edge-tts` and `pygame` playback

## Requirements
- Python 3.10+
- Windows recommended (tested on Windows)

## Installation
1. Clone the repo:

```bash
git clone https://github.com/Abdullah17521/1st-voice-agent.git
cd 1st-voice-agent
```

2. Create and activate a virtualenv:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# On Windows, if PyAudio fails to build, you can use pipwin:
# pip install pipwin
# pipwin install pyaudio
```

4. Create a `.env` file (see `.env.example`) and set any keys needed by `agent.py`.

## Usage
Run the voice agent from the project root:

```bash
python main.py
```

Speak clearly into your microphone. Say `exit`, `quit`, or `stop` to end the session.

## Files
- `main.py` — entrypoint that listens, queries the agent, and speaks responses
- `agent.py` — wraps the Gemini/AI calls (ensure it is configured)
- `voice_agent.py` / `app.py` — extra utilities and app interfaces

## Notes
- The repository includes a `venv` directory and other local artifacts. Add them to `.gitignore` (provided).
- If you plan to push to GitHub, ensure your local git user/email are configured and you have push access to the target repo.

## License
Project code — see repository for license details.
