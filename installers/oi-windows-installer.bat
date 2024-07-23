@echo off

echo Starting Open Interpreter installation...
timeout /t 2

echo This will take approximately 5 minutes...
timeout /t 2

REM Set up a virtual environment
python -m venv opai

REM Activate the virtual environment
call opai\Scripts\activate.bat

REM Install the necessary packages
pip install open-interpreter
pip install tk pillow pyttsx3 speechrecognition pyautogui keyboard langchain_community langchain_openai chromadb

REM Install pyaudio
pip install pyaudio

echo.
echo Open Interpreter has been installed. Run the following command to use it:
echo.
echo call opai\Scripts\activate.bat && python testchat.py
