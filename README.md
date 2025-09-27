# JarviSonix – Hack the North Submission (Team: jasoncaogit)

Transform a hummed melody into MIDI, then automate a DAW workflow with a voice-driven Computer-Use Agent (CUA). This README focuses on what’s implemented now: Vapi voice agent, MIDI conversion, CUA automation, and local Ollama LLM.


## What this agent does
- Listens to the user (voice) to pick an instrument.
- Records a short hum with audio beep cue.
- Converts hum → MIDI with Basic Pitch (Python 3.11 env).
- **Uses Ollama LLM to generate intelligent, context-aware automation instructions** based on instrument type and audio context.
- Automates BandLab in the browser using CUA (Python 3.13 env + Docker), imports MIDI, and plays back.

## Models and tools used (and what runs where)
- **Ollama LLM Integration**: Local `llama3.1:8b` model generates intelligent automation instructions based on:
  - Instrument type (guitar, piano, drums, etc.)
  - User intent and audio context
  - Target DAW (BandLab Studio) specifics
  - User experience level and workflow preferences
- Computer-Use Agent: CUA (Docker container provider) driving the browser (BandLab),
  using Ollama-enhanced prompts for better automation success.
- Voice: Vapi.ai session and WebSocket audio.
- Audio→MIDI: Spotify Basic Pitch (local, Python 3.11).

## Ollama LLM Integration

The system uses Ollama to generate **intelligent, context-aware automation instructions** instead of hardcoded prompts. This dramatically improves automation success rates.

### How Ollama Enhancement Works

1. **Audio Context Capture**: System captures rich context including:
   - Instrument type (guitar, piano, drums, etc.)
   - User intent ("create melody", "add rhythm", etc.)
   - Audio source (humming, clapping, etc.)
   - Target DAW (BandLab Studio)
   - User experience level

2. **Intelligent Prompt Generation**: Ollama generates customized instructions like:
   - **Guitar**: "Set up electric guitar with appropriate effects..."
   - **Piano**: "Configure grand piano with proper velocity settings..."
   - **Drums**: "Import as drum track with percussion mapping..."

3. **Enhanced Automation**: CUA receives context-specific instructions instead of generic ones, leading to:
   - Higher success rates for DAW automation
   - Better instrument-specific workflows
   - More intuitive user experience

### Ollama Setup
```bash
# Install and start Ollama
ollama serve
ollama pull llama3.1:8b


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
- 3.11 env runs hum recording (with audio beep cue) and MIDI conversion (`hum.py`, `midi.py`)
- 3.13 env runs the CUA browser automation (`cua.py`) using **Ollama-enhanced prompts** for intelligent automation

### Complete Pipeline Flow
```
Voice Assistant → Hum Recording (with beep) → MIDI Conversion
                                                      ↓
Audio Context → Ollama LLM → Enhanced Instructions → CUA Automation
                                                      ↓
                                            BandLab Studio Automation
```

## Key Benefits of Ollama Integration

- **🧠 Intelligent Automation**: Context-aware prompts adapt to specific instruments and user intent
- **📈 Higher Success Rates**: Enhanced instructions lead to more reliable DAW automation
- **🎯 Instrument-Specific**: Different workflows for guitar vs piano vs drums
- **🔄 Fallback Safety**: System works even if Ollama is unavailable (uses basic prompts)
- **⚡ Local Processing**: No cloud dependencies, all processing happens locally
- **🎵 Better UX**: More intuitive automation that understands user context





## Demo video
- https://drive.google.com/file/d/1e5J7VUdoneriWpfgqHblY4JbaJWMk72p/view?usp=sharingß


