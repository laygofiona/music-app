# JarviSonix – Hack the North Submission (Team: jasoncaogit)

Transform a hummed melody into MIDI, then automate a DAW workflow with a voice-driven Computer-Use Agent (CUA). This README focuses on what’s implemented now: Vapi voice agent, MIDI conversion, CUA automation, and local Ollama LLM.


## What this agent does
- Listens to the user (voice) to pick an instrument.
- Records a short hum.
- Converts hum → MIDI with Basic Pitch (Python 3.11 env).
- Automates BandLab in the browser using CUA (Python 3.13 env + Docker), imports MIDI, and plays back.

## Models and tools used (and what runs where)
- Computer-Use Agent: CUA (Docker container provider) driving the browser (BandLab),
  backed by a LOCAL LLM via Ollama (`llama3.1:8b`).
- Voice: Vapi.ai session and WebSocket audio.
- Audio→MIDI: Spotify Basic Pitch (local, Python 3.11).

Local vs Hybrid design:
- Local: CUA runs locally with Docker; LLM is local via Ollama; Basic Pitch is local.
- Hybrid (optional/not required): If enabled later, cloud services (e.g., Replicate) can be used for music enhancement.

## How to use this agent
This repository contains the full source code and a simple way to run the agent locally.

### Prerequisites
- Docker Desktop
- Python 3.11 (for Basic Pitch) and Python 3.13 (for CUA)
- Ollama installed with a local model:
  - `ollama pull llama3.1:8b`

### Required environment variables
- Vapi (voice agent):
  - `VAPI_API_KEY`
  - `VAPI_ASSISTANT_ID`

### Run
- GUI: `python front-end/app.py`
- CLI (headless): `python listen.py`

The pipeline orchestrates:
- 3.11 env runs hum recording and MIDI conversion (`hum.py`, `midi.py`)
- 3.13 env runs the CUA browser automation (`cua.py`) using local Ollama





## Demo video
- https://drive.google.com/file/d/1e5J7VUdoneriWpfgqHblY4JbaJWMk72p/view?usp=sharingß


