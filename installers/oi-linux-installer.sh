#!/bin/bash

echo "Starting Open Interpreter installation..."
sleep 2
echo "This will take approximately 5 minutes..."
sleep 2

# Check if Rust is installed
if ! command -v rustc &> /dev/null
then
    echo "Rust is not installed. Installing now..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
else
    echo "Rust is already installed."
fi

# Install pyenv
curl https://pyenv.run | bash

# Define pyenv location
pyenv_root="$HOME/.pyenv/bin/pyenv"

python_version="3.11.7"

# Install specific Python version using pyenv
$pyenv_root init
$pyenv_root install $python_version --skip-existing
$pyenv_root shell $python_version

# Install necessary Python packages
$pyenv_root exec pip install open-interpreter --break-system-packages
$pyenv_root exec pip install tkinter pillow pyttsx3 speechrecognition pyautogui keyboard

# Unset the Python version
$pyenv_root shell --unset

# Copy the updated testchat.py and image_interpreter.py to the installation directory
install_dir="$HOME/open-interpreter"
mkdir -p $install_dir
cp testchat.py $install_dir
cp image_interpreter.py $install_dir

echo ""
echo "Open Interpreter has been installed. Run the following command to use it: "
echo ""
echo "cd $install_dir && $pyenv_root shell $python_version && python testchat.py"
