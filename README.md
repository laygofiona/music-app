# JarviSonix - AI Music Creation Pipeline 🎵

Transform your humming into professional music using AI! This app combines voice recognition, MIDI conversion, and automated DAW control to create a seamless music creation experience.

## 🚀 Features

- **Voice Recognition**: Tell the AI what instrument you want to play
- **Hum Recording**: Record your melody by humming
- **MIDI Conversion**: Convert audio to MIDI using basic-pitch
- **DAW Automation**: Automatically import MIDI and play in BandLab
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

### Windows
- Python 3.11 and Python 3.13 (install both versions)
- Git
- Docker Desktop (for CUA computer automation)

### macOS
- Python 3.11 and Python 3.13 (using asdf or pyenv)
- Git
- Docker Desktop

## 🛠️ Installation

### Quick Setup (Windows)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd music-app
   ```

2. **Run the Windows setup script:**
   ```cmd
   setup_windows.bat
   ```

3. **Start the application:**
   ```cmd
   python front-end/app.py
   ```

### Manual Setup (Windows)

1. **Create Python 3.11 environment for basic-pitch:**
   ```cmd
   python -m venv venv_basic_pitch
   venv_basic_pitch\Scripts\activate
   pip install -r requirements_basic_pitch.txt
   ```

2. **Create Python 3.13 environment for CUA:**
   ```cmd
   python -m venv venv_cua
   venv_cua\Scripts\activate
   pip install -r requirements_cua.txt
   ```

3. **Install main dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

### macOS Setup

1. **Clone and setup:**
   ```bash
   git clone <your-repo-url>
   cd music-app
   chmod +x setup_mac.sh
   ./setup_mac.sh
   ```

## 🎮 Usage

### Method 1: GUI Application
```cmd
python front-end/app.py
```

### Method 2: Command Line
```cmd
python listen.py
```

## 🔧 Configuration

### API Keys
Make sure you have your Vapi API key set up in `listen.py`:
```python
API_KEY = "your-vapi-api-key-here"
ASSISTANT_ID = "your-assistant-id-here"
```

### Docker Setup
Ensure Docker Desktop is running for the CUA automation to work properly.

## 📁 Project Structure

```
music-app/
├── front-end/
│   └── app.py              # GUI application
├── listen.py               # Main orchestration script
├── midi.py                 # MIDI conversion with basic-pitch
├── cua.py                  # Computer automation for DAW
├── hum.py                  # Hum recording functionality
├── melody.py               # Optional: MusicGen for enhancement
├── requirements.txt        # Main dependencies
├── requirements_basic_pitch.txt  # Python 3.11 dependencies
├── requirements_cua.txt    # Python 3.13 dependencies
├── setup_windows.bat       # Windows setup script
├── setup_mac.sh           # macOS setup script
└── README.md              # This file
```

## 🔄 How It Works

1. **Voice Input**: User speaks to specify instrument
2. **Hum Recording**: User hums their melody
3. **MIDI Conversion**: Audio is converted to MIDI using basic-pitch
4. **DAW Automation**: CUA agent imports MIDI and plays in BandLab
5. **Result**: Professional-sounding music track

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors:**
- Make sure you're using the correct Python version for each component
- Verify virtual environments are activated

**Docker connection issues:**
- Ensure Docker Desktop is running
- Check if ports 8000 and 5900 are available

**Audio recording issues:**
- Check microphone permissions
- Verify sounddevice installation

**CUA automation not working:**
- Ensure `cua-som` is installed in the Python 3.13 environment
- Check Docker container logs

### Environment Issues

**Python version conflicts:**
```cmd
# Check Python versions
python --version
python3.11 --version
python3.13 --version
```

**Virtual environment issues:**
```cmd
# Recreate environments if needed
rmdir /s venv_basic_pitch venv_cua
setup_windows.bat
```

## 🚀 Advanced Usage

### Custom Instruments
Modify the instrument detection in `listen.py` to add more instrument types.

### Different DAWs
Update `cua.py` to work with other DAWs like Logic Pro, Ableton Live, etc.

### Music Enhancement
Use `melody.py` to enhance your generated MIDI with AI-generated accompaniments.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on both Windows and macOS
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Vapi** for voice AI capabilities
- **basic-pitch** for audio-to-MIDI conversion
- **CUA** for computer automation
- **BandLab** for the DAW platform
- **MusicGen** for optional music enhancement

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the logs in the console
3. Ensure all prerequisites are installed
4. Create an issue in the repository

---

**Happy Music Making! 🎶**