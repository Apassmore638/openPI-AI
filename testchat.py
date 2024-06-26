import tkinter as tk
from tkinter import scrolledtext
from interpreter import interpreter
import speech_recognition as sr
import threading
import os
import pyttsx3
import argparse
import keyboard  # Using keyboard library for key bindings

# Argument parsing
parser = argparse.ArgumentParser(description="Open Interpreter Chat UI")
parser.add_argument('--os', type=str, help='Specify the operating system')
args = parser.parse_args()

# Configure the interpreter to use Azure OpenAI Service with environment variables
interpreter.llm.api_key = os.getenv('API_KEY')
interpreter.llm.api_base = os.getenv('API_BASE')
interpreter.llm.api_type = os.getenv('API_TYPE')
interpreter.llm.api_version = os.getenv('API_VERSION')
interpreter.llm.model = os.getenv('MODEL')
interpreter.llm.supports_vision = os.getenv('SUPPORTS_VISION', 'False').lower() in ('true', '1', 't')

# Print the model to ensure it is set correctly
print(f"Model set to: {interpreter.llm.model}")

# Set the operating system if provided
if args.os:
    interpreter.os = args.os

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()

def send_message(event=None):  # Modified to accept an optional event parameter
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

# Create a frame to hold the chat window and the input box
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a text widget for user input
input_box = tk.Text(main_frame, height=3)
input_box.pack(padx=10, pady=10, fill=tk.X, expand=False)

# Bind the Enter key to send_message
keyboard.add_hotkey('enter', send_message)

# Create a frame for the buttons at the bottom
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

# Create a send button
send_button = tk.Button(button_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a speech-to-text button
speech_button = tk.Button(button_frame, text="Speak", command=start_recognition_thread)
speech_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Create a checkbox to toggle text-to-speech
tts_var = tk.BooleanVar()
tts_checkbox = tk.Checkbutton(button_frame, text="Enable Text-to-Speech", variable=tts_var)
tts_checkbox.pack(side=tk.LEFT, padx=5, pady=5)

# Run the application
root.mainloop()