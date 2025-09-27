import sounddevice as sd
import soundfile as sf
import numpy as np
import time

def play_beep(frequency=800, duration=0.5, samplerate=44100):
    """
    Play a beep sound to signal the start of recording.
    
    Args:
        frequency: Frequency of the beep in Hz (default: 800Hz - a pleasant tone)
        duration: Duration of the beep in seconds (default: 0.5s)
        samplerate: Sample rate for audio generation (default: 44100Hz)
    """
    # Generate a sine wave for the beep sound
    # This creates a clean, pleasant beep tone
    t = np.linspace(0, duration, int(samplerate * duration), False)
    beep_sound = np.sin(2 * np.pi * frequency * t)
    
    # Add a slight fade-in and fade-out to make it sound more pleasant
    # This prevents any clicking sounds at the start/end
    fade_samples = int(0.01 * samplerate)  # 10ms fade
    beep_sound[:fade_samples] *= np.linspace(0, 1, fade_samples)
    beep_sound[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    try:
        # Play the beep through the default audio output
        # This gives users a clear audio cue that recording is about to start
        sd.play(beep_sound, samplerate=samplerate)
        sd.wait()  # Wait for the beep to finish playing
        print("🔊 Beep played - recording will start now!")
    except Exception as e:
        # If audio output fails, just print a message
        # This ensures the recording process continues even if beep fails
        print(f"⚠️ Could not play beep: {e}")
        print("🎤 Recording will start without audio cue...")

def record_hum(output_file="hum.wav", instrument="piano", samplerate=44100, channels=1, silence_thresh=0.01, min_silence_len=2):
    time.sleep(3)
    print("🎤 Ready. Start humming...")
    
    # Play a beep to signal that recording is about to start
    # This gives users a clear audio cue to begin humming
    print("🔊 Playing start beep...")
    play_beep(frequency=800, duration=0.5, samplerate=samplerate)
    
    # Small delay after beep to let users prepare
    time.sleep(0.2)
    print("🎵 Recording started - hum your melody now!")
    
    recording = []
    silence_counter = 0
    chunk_size = int(samplerate * 0.1)  # 100ms chunks

    with sd.InputStream(samplerate=samplerate, channels=channels) as stream:
        while True:
            chunk, _ = stream.read(chunk_size)
            chunk = chunk.copy()
            recording.append(chunk)

            volume = np.abs(chunk).mean()
            if volume < silence_thresh:
                silence_counter += 1
            else:
                silence_counter = 0

            if silence_counter > min_silence_len * 10:  # e.g. 2s silence
                break

    recording = np.concatenate(recording, axis=0)
    sf.write(output_file, recording, samplerate)
    print(f"✅ Saved recording to {output_file}")
    
    # Route to appropriate MIDI generator based on instrument
    print(f"🎵 Processing for instrument: {instrument}")
    
    if instrument.lower() in ["drums", "drum", "percussion"]:
        # Use drum_midi.py for drum processing
        print("🥁 Using drum MIDI generator...")
        from drum_midi import clap_to_drum_groove
        midi_file = clap_to_drum_groove(output_file, f"drum_groove_{int(time.time())}.mid")
        return midi_file
    else:
        # Use midi.py for melodic instruments (piano, guitar, etc.)
        print(f"🎹 Using melodic MIDI generator for {instrument}...")
        from midi import convert_to_midi
        midi_file = convert_to_midi(output_file, ".")
        return midi_file

if __name__ == "__main__":
    record_hum()