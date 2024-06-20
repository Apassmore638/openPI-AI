import tkinter as tk
from tkinter import scrolledtext
from interpreter import interpreter
import os
import speech_recognition as sr
import threading
import pyttsx3
import argparse
import keyboard

# Argument parsing
parser = argparse.ArgumentParser(description="Open Interpreter Chat UI")
parser.add_argument('--os', type=str, help='Specify the operating system')
args = parser.parse_args()

# Configure the interpreter to use Azure OpenAI Service with environment variables
import os
interpreter.llm.api_key = os.getenv('AZURE_API_KEY')
interpreter.llm.api_base = os.getenv('AZURE_API_BASE')
interpreter.llm.api_type = os.getenv('AZURE_API_TYPE')
interpreter.llm.api_version = os.getenv('AZURE_API_VERSION')
interpreter.llm.model = os.getenv('AZURE_MODEL')
interpreter.llm.supports_vision = True  # Enable vision support

# Set the operating system if provided
if args.os:
    interpreter.os = args.os

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def send_message():
    user_input = input_box.get("1.0", tk.END).strip()
    if user_input:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n")
        chat_window.config(state=tk.DISABLED)
        input_box.delete("1.0", tk.END)
        
        response = get_interpreter_response(user_input)
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "Bot: " + response + "\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)
        
        if tts_var.get():
            tts_engine.say(response)
            tts_engine.runAndWait()

def get_interpreter_response(prompt):
    # Call the interpreter's chat method with the user's prompt
    messages = interpreter.chat(prompt, display=False, stream=False)
    # Extract the response from the messages
    response = messages[-1]['content'] if messages else "No response"
    return response

def interrupt(event=None):
    # Reset the interpreter to stop any ongoing processing
    interpreter.reset()
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "System: The operation has been interrupted.\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "System: Listening...\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        input_box.insert(tk.END, user_input)
        send_message()
    except sr.UnknownValueError:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "System: Could not understand audio\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)
    except sr.RequestError as e:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f"System: Could not request results; {e}\n")
        chat_window.config(state=tk.DISABLED)
        chat_window.yview(tk.END)

def start_recognition_thread():
    threading.Thread(target=recognize_speech).start()

# Set up the main application window
root = tk.Tk()
root.title("Chat UI")

# Bind Ctrl+C to the interrupt function
root.bind('<Control-c>', interrupt)

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a text widget for user input
input_box = tk.Text(root, height=3)
input_box.pack(padx=10, pady=10, fill=tk.X, expand=False)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.LEFT)

# Create a speech-to-text button
speech_button = tk.Button(root, text="Speak", command=start_recognition_thread)
speech_button.pack(padx=10, pady=10, side=tk.RIGHT)

# Create a checkbox to toggle text-to-speech
tts_var = tk.BooleanVar()
tts_checkbox = tk.Checkbutton(root, text="Enable Text-to-Speech", variable=tts_var)
tts_checkbox.pack(padx=10, pady=10)

# Set up a global hotkey for speech recognition
keyboard.add_hotkey('right ctrl', start_recognition_thread)

# Run the application
root.mainloop()