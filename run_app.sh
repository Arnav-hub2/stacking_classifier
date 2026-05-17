#!/bin/bash
# Quick Start Script for Credit Default Prediction App

echo "================================"
echo "Credit Default Prediction App"
echo "Quick Start Setup"
echo "================================"

# Check Python installation
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    venv\Scripts\activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the app
echo ""
echo "================================"
echo "Starting Streamlit App..."
echo "================================"
echo ""
echo "The app will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run app.py
