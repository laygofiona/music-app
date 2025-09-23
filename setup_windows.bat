@echo off
echo Setting up JarviSonix Music App on Windows...

REM Create virtual environments
echo Creating Python 3.11 environment for basic-pitch...
python -m venv venv_basic_pitch
call venv_basic_pitch\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements_basic_pitch.txt

echo Creating Python 3.13 environment for CUA...
python -m venv venv_cua
call venv_cua\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements_cua.txt

REM Install main requirements in current environment
echo Installing main requirements...
pip install -r requirements.txt

echo Setup complete! 
echo.
echo To run the app:
echo 1. Start the GUI: python front-end/app.py
echo 2. Or run directly: python listen.py
echo.
pause
