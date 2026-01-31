#!/bin/bash

# Installation script for Reversal Bot
# This script sets up a virtual environment and installs dependencies

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     GOLD/USD Reversal Bot - Installation Script             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "NEXT STEPS:"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Configure your Telegram credentials in .env file:"
echo "   nano .env"
echo ""
echo "3. Run the bot:"
echo "   python main.py"
echo ""
echo "4. Or test pattern detection first:"
echo "   python test_patterns.py"
echo ""
echo "═══════════════════════════════════════════════════════════════"
