import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

# Pick device (MPS for Apple Silicon GPU, CUDA for Nvidia, fallback CPU)
device = "mps" if torch.backends.mps.is_available() else (
    "cuda" if torch.cuda.is_available() else "cpu"
)
print(f"Using device: {device}")

# Load the melody-conditioned model (can also use 'small', 'medium', 'large')
model = MusicGen.get_pretrained('melody')

# Configure generation parameters
model.set_generation_params(
    duration=8,         # seconds of audio
    use_sampling=True,  # stochastic decoding
    top_k=250,          # limits vocab search, faster and more focused
    temperature=1.0     # randomness scale
)

# Load your humming/melody
melody, sr = torchaudio.load("./hum_1758589234.wav")

# Text prompt
descriptions = [
    "orchestral pop-rock"
]

# Generate conditioned on melody + description
wav = model.generate_with_chroma(
    descriptions,
    melody[None],  # add batch dimension
    sr
)

# Save result(s)
for idx, one_wav in enumerate(wav):
    out_path = f"output_{idx}.wav"
    audio_write(out_path, one_wav.cpu(), model.sample_rate, strategy="loudness")
    print(f"Saved: {out_path}")