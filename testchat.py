import tkinter as tk
from tkinter import scrolledtext
from interpreter import interpreter

# Configure the interpreter to use Azure OpenAI Service
interpreter.llm.api_key = '...'
interpreter.llm.api_base = '...'
interpreter.llm.api_type = '...'
interpreter.llm.api_version = '...'  # or the version you are using
interpreter.llm.model = '...'
interpreter.llm.supports_vision = True  # Enable vision support


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

def get_interpreter_response(prompt):
    # Call the interpreter's chat method with the user's prompt
    messages = interpreter.chat(prompt, display=False, stream=False)
    # Extract the response from the messages
    response = messages[-1]['content'] if messages else "No response"
    return response

def interrupt():
    # Reset the interpreter to stop any ongoing processing
    interpreter.reset()
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "System: The operation has been interrupted.\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Set up the main application window
root = tk.Tk()
root.title("Chat UI")

# Create a scrolled text widget for the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a text widget for user input
input_box = tk.Text(root, height=3)
input_box.pack(padx=10, pady=10, fill=tk.X, expand=False)

# Create a send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10, side=tk.LEFT)

# Create an interrupt button
interrupt_button = tk.Button(root, text="Interrupt", command=interrupt)
interrupt_button.pack(padx=10, pady=10, side=tk.RIGHT)

# Run the application
root.mainloop()