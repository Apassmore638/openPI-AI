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
$pyenv_root exec pip install tk pillow pyttsx3 speechrecognition pyautogui keyboard

# Unset the Python version
$pyenv_root shell --unset

# Initialize pyenv in the shell configuration file
shell_config="$HOME/.bashrc"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> $shell_config
echo 'eval "$(pyenv init --path)"' >> $shell_config
echo 'eval "$(pyenv init -)"' >> $shell_config

echo ""
echo "Open Interpreter has been installed. Run the following command to use it: "
echo ""
echo "source $shell_config && cd $(pwd) && $pyenv_root shell $python_version && python testchat.py"