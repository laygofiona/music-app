# Windows Setup Guide for JarviSonix 🪟

This guide will help you set up JarviSonix on Windows from scratch.

## 📋 Prerequisites

### 1. Install Python (Both 3.11 and 3.13)
Download and install both Python versions from [python.org](https://www.python.org/downloads/):

1. **Python 3.11**: Download from https://www.python.org/downloads/release/python-3117/
2. **Python 3.13**: Download from https://www.python.org/downloads/release/python-3130/

**Important**: During installation, check "Add Python to PATH" for both versions.

### 2. Install Git
Download from https://git-scm.com/download/win and install with default settings.

### 3. Install Docker Desktop
Download from https://www.docker.com/products/docker-desktop/ and install.

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)

1. **Open Command Prompt as Administrator**
   - Press `Win + R`, type `cmd`, press `Ctrl + Shift + Enter`

2. **Clone the repository:**
   ```cmd
   git clone <your-repo-url>
   cd music-app
   ```

3. **Run the setup script:**
   ```cmd
   setup_windows.bat
   ```

4. **Wait for installation to complete** (this may take 10-15 minutes)

### Option 2: Manual Setup

If the automated setup doesn't work, follow these steps:

#### Step 1: Create Python 3.11 Environment
```cmd
python -m venv venv_basic_pitch
venv_basic_pitch\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements_basic_pitch.txt
deactivate
```

#### Step 2: Create Python 3.13 Environment
```cmd
python -m venv venv_cua
venv_cua\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements_cua.txt
deactivate
```

#### Step 3: Install Main Dependencies
```cmd
pip install -r requirements.txt
```

## 🎮 Running the Application

### Method 1: GUI Application (Recommended)
```cmd
python front-end/app.py
```

### Method 2: Command Line
```cmd
python listen.py
```

## 🔧 Configuration

### 1. Set Up Vapi API Key
Edit `listen.py` and replace the API key:
```python
API_KEY = "your-vapi-api-key-here"
ASSISTANT_ID = "your-assistant-id-here"
```

### 2. Ensure Docker is Running
- Start Docker Desktop
- Wait for it to fully load (green icon in system tray)

## 🐛 Troubleshooting

### Issue: "Python not found"
**Solution**: Add Python to PATH
1. Search "Environment Variables" in Start Menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables"
4. Under "System Variables", find "Path" and click "Edit"
5. Add these paths:
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts\`
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\`
   - `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\Scripts\`

### Issue: "pip not found"
**Solution**: Reinstall Python with "Add to PATH" checked

### Issue: "Docker not running"
**Solution**: 
1. Start Docker Desktop
2. Wait for it to show "Docker Desktop is running"
3. Try the command again

### Issue: "Module not found" errors
**Solution**: Check which Python environment you're using:
```cmd
python --version
where python
```

### Issue: Virtual environment activation fails
**Solution**: Use full path:
```cmd
C:\path\to\your\project\venv_basic_pitch\Scripts\activate
```

### Issue: Permission errors
**Solution**: Run Command Prompt as Administrator

## 📁 File Structure After Setup

Your project should look like this:
```
music-app/
├── venv_basic_pitch/          # Python 3.11 environment
├── venv_cua/                  # Python 3.13 environment
├── front-end/
│   └── app.py                # GUI application
├── listen.py                 # Main script
├── midi.py                   # MIDI conversion
├── cua.py                    # Computer automation
├── hum.py                    # Hum recording
├── requirements.txt          # Main dependencies
├── requirements_basic_pitch.txt
├── requirements_cua.txt
├── setup_windows.bat         # Setup script
└── README.md
```

## 🎯 Testing Your Setup

1. **Test Python versions:**
   ```cmd
   python --version
   python -m venv --help
   ```

2. **Test virtual environments:**
   ```cmd
   venv_basic_pitch\Scripts\activate
   python --version
   deactivate
   ```

3. **Test Docker:**
   ```cmd
   docker --version
   docker run hello-world
   ```

4. **Test the application:**
   ```cmd
   python front-end/app.py
   ```

## 🚨 Common Error Messages and Solutions

| Error | Solution |
|-------|----------|
| `'python' is not recognized` | Install Python and add to PATH |
| `'pip' is not recognized` | Reinstall Python with PATH option |
| `Permission denied` | Run as Administrator |
| `ModuleNotFoundError` | Activate correct virtual environment |
| `Docker connection failed` | Start Docker Desktop |
| `Port already in use` | Close other applications using port 8000 |

## 📞 Getting Help

If you're still having issues:

1. **Check the main README.md** for general troubleshooting
2. **Review the console output** for specific error messages
3. **Ensure all prerequisites are installed** correctly
4. **Try the manual setup** if automated setup fails
5. **Create an issue** in the repository with your error details

## 🎉 Success!

Once everything is working, you should be able to:
- Start the GUI application
- Speak to specify an instrument
- Hum your melody
- See it automatically converted to MIDI and played in BandLab

**Happy music making! 🎵**
