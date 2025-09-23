# JarviSonix – Hack the North Submission (Team: jasoncaogit)

Transform a hummed melody into a full track using a voice agent + CUA automation.


## What this agent does
- Listens to the user (voice) to pick an instrument.
- Records a short hum.
- Converts hum → MIDI with Basic Pitch (Python 3.11 env).
- Automates BandLab in the browser using CUA (Python 3.13 env + Docker), imports MIDI, and plays back.

## Models and tools used
- Computer-Use Agent: CUA (Docker container provider) to drive the browser (BandLab),
  backed by a LOCAL LLM via Ollama (`llama3.1:8b`).
- Voice: Vapi.ai session and WebSocket audio.
- Audio→MIDI: Spotify Basic Pitch (local, Python 3.11).

Local vs Hybrid:
- Local: CUA runs locally with Docker; LLM served by Ollama locally; Basic Pitch runs locally.
- Hybrid (optional): If enabled, MusicGen via Replicate (cloud) for enhancement.




## Run
- GUI: `python front-end/app.py`
- CLI: `python listen.py`

Both orchestrate:
- 3.11 env executes `hum.py`/MIDI conversion
- 3.13 env executes `cua.py` (CUA agent in Docker)

## Ollama configuration (in use)
- Ensure `ollama` is installed and running.
- Pull model once: `ollama pull llama3.1:8b`.
- `cua.py` is configured to use Ollama for the LLM (Computer-Use Agent planning/execution).

## Demo video
- https://drive.google.com/file/d/1e5J7VUdoneriWpfgqHblY4JbaJWMk72p/view?usp=sharingß


