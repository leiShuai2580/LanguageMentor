#!/bin/bash

# Activation script for LanguageMentor Python 3.12 environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="${SCRIPT_DIR}/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please run: python3.12 -m venv venv"
    exit 1
fi

echo "Activating Python 3.12 virtual environment..."
source "${VENV_PATH}/bin/activate"

echo "✓ Virtual environment activated"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo ""
echo "Installed key packages:"
pip list | grep -E "langchain|gradio|loguru"
echo ""
echo "To deactivate, run: deactivate"
