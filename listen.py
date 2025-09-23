import asyncio
import json
import requests
import sounddevice as sd
import numpy as np
import websockets
import time
import warnings
import subprocess
import os

warnings.filterwarnings("ignore", category=UserWarning, module="sounddevice")

API_KEY = "8461cb9f-7560-4c62-a120-7173b2696850"
ASSISTANT_ID = "a6210139-4abf-4ed8-b1a5-0996953045b3"
CALL_URL = "https://api.vapi.ai/call"


def create_ws_call():
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "assistantId": ASSISTANT_ID,
        "transport": {
            "provider": "vapi.websocket",
            "audioFormat": {
                "format": "pcm_s16le",
                "container": "raw",
                "sampleRate": 16000,
            },
        },
    }
    resp = requests.post(CALL_URL, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    print("✅ Call started:", data)
    ws_url = data["transport"]["websocketCallUrl"]
    print("🔗 Connect to:", ws_url)
    return ws_url


async def audio_producer(queue: asyncio.Queue):
    """Capture mic and push PCM chunks into queue"""

    def callback(indata, frames, time, status):
        if status:
            print("⚠️ Audio status:", status)
        audio_int16 = (indata[:, 0] * 32767).astype(np.int16)
        queue.put_nowait(audio_int16.tobytes())

    with sd.InputStream(samplerate=16000, channels=1, dtype="float32", callback=callback):
        print("🎤 Recording... press Ctrl+C to stop")
        await asyncio.Future()  # run forever


async def audio_consumer(ws, queue: asyncio.Queue):
    """Send mic audio from queue to websocket"""
    while True:
        chunk = await queue.get()
        await ws.send(chunk)


async def listen(ws):
    buffer = ""
    phrase_detected = False
    instrument_name = None
    complete_phrase_received = False  # Track if we've received the complete phrase

    with sd.OutputStream(samplerate=16000, channels=1, dtype="int16") as speaker:
        async for message in ws:
            if isinstance(message, (bytes, bytearray)):
                audio = np.frombuffer(message, dtype=np.int16)
                speaker.write(audio)
                continue

            try:
                data = json.loads(message)
            except Exception:
                continue

            if data.get("type") == "model-output":
                buffer += data.get("output", "")
                print("🧩 Buffer:", buffer)

                # Check for complete phrase - wait for the full "detected, please hum in 5 seconds" message
                if not phrase_detected and "detected, please hum in 5 seconds" in buffer:
                    # Extract instrument name more carefully
                    parts = buffer.split(" detected")[0].strip().split()
                    if len(parts) >= 2:
                        instrument_name = parts[-1]  # Last word before "detected"
                    else:
                        instrument_name = "piano"  # fallback
                    
                    print(f"✅ Instrument: {instrument_name}")
                    with open("instrument.txt", "w") as f:
                        f.write(instrument_name)
                    phrase_detected = True
                    complete_phrase_received = True  # Mark that we've received the complete phrase
                    print("✅ Complete phrase received, will wait for assistant to finish speaking...")

            elif data.get("type") == "speech-update":
                # Only close after we've received the complete phrase AND the assistant has finished speaking
                if (
                    complete_phrase_received
                    and data.get("status") == "stopped"
                    and data.get("role") == "assistant"
                ):  
                    await asyncio.sleep(3)
                    print("🔚 Assistant finished complete phrase, waiting 5s then closing...")
                    # Give more time to ensure the assistant has completely finished speaking
                    
                    await ws.close(code=1000, reason="done")
                    return  # exit listen()


async def main():
    ws_url = create_ws_call()
    queue = asyncio.Queue()

    try:
        async with websockets.connect(ws_url) as ws:
            await asyncio.gather(
                audio_producer(queue),
                audio_consumer(ws, queue),
                listen(ws),
            )
    except Exception as e:
        print("⚠️ Main loop ended:", e)


async def full_pipeline():
    """Complete pipeline: voice assistant -> hum recording -> MIDI -> CUA"""
    # Run websocket loop
    await main()

    # After WS closes, start hum recording
    
    # Get the instrument from the file (set by Vapi assistant)
    instrument = "piano"  # default fallback
    try:
        with open("instrument.txt", "r") as f:
            instrument = f.read().strip()
            print(f"🎵 Detected instrument: {instrument}")
    except FileNotFoundError:
        print("⚠️ No instrument.txt found, using default: piano")
    
    # Create timestamped WAV filename
    timestamp = int(time.time())
    wav_file = f"hum_{timestamp}.wav"
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run hum recording and MIDI conversion in Python 3.11 environment
    venv_basic_pitch = os.path.join(script_dir, "venv_basic_pitch")
    hum_cmd = [
        "bash", "-c",
        f"cd '{script_dir}' && source '{venv_basic_pitch}/bin/activate' && python -c \"from hum import record_hum; print(record_hum('{wav_file}', instrument='{instrument}'))\""
    ]
    
    result = subprocess.run(hum_cmd, capture_output=True, text=True, cwd=script_dir)
    if result.returncode == 0:
        # Parse the output to extract just the MIDI filename (last line)
        output_lines = result.stdout.strip().split('\n')
        midi_file = output_lines[-1].strip()  # Get the last line which should be the MIDI file path
        print(f"✅ MIDI file created: {midi_file}")
        
        # Run CUA in Python 3.13 environment
        print("🚀 Sending to CUA for DAW processing...")
        venv_cua = os.path.join(script_dir, "venv_cua")
        
        # Create temporary script for CUA
        temp_script = f"""import asyncio
import sys
import os
sys.path.append('{script_dir}')
from cua import computer_use_agent

async def main():
    midi_file = "{midi_file}"
    instrument = "{instrument}"
    await computer_use_agent(midi_file, instrument)

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        temp_script_path = os.path.join(script_dir, "temp_cua_script.py")
        with open(temp_script_path, "w") as f:
            f.write(temp_script)
            
        try:
            # Run CUA script in Python 3.13 environment
            cua_cmd = [
                "bash", "-c",
                f"cd '{script_dir}' && source '{venv_cua}/bin/activate' && python '{temp_script_path}'"
            ]
            
            cua_result = subprocess.run(cua_cmd, capture_output=True, text=True, cwd=script_dir)
            if cua_result.returncode != 0:
                print(f"❌ CUA failed: {cua_result.stderr}")
            
            # Clean up temporary script
            os.remove(temp_script_path)
            
        except Exception as e:
            print(f"❌ Error running CUA: {e}")
    else:
        print(f"❌ Failed to create MIDI file: {result.stderr}")


def start_listening():
    """
    Entrypoint to start the backend pipeline. Designed to be called from a
    separate process (recommended) to isolate TensorFlow / PortAudio.
    """
    print("📡 listen.py start_listening() called")
    asyncio.run(full_pipeline())


if __name__ == "__main__":
    start_listening()