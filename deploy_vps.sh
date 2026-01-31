#!/bin/bash

# VPS Deployment Script for GOLD Reversal Bot
# Run this script on your Linux VPS

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     GOLD Reversal Bot - VPS Deployment Script               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3 and pip
echo "🐍 Installing Python 3 and pip..."
sudo apt-get install -y python3 python3-pip python3-venv git

# Clone repository (if not already cloned)
if [ ! -d "reversal_bot" ]; then
    echo "📥 Cloning repository..."
    # Replace with your actual git repository URL
    # git clone https://github.com/yourusername/reversal_bot.git
    echo "⚠️  Please clone your repository manually:"
    echo "   git clone YOUR_REPO_URL"
    echo ""
else
    echo "✓ Repository already exists"
fi

cd reversal_bot

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your credentials:"
    echo "   nano .env"
    echo ""
    echo "   Add your:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_CHAT_ID"
    echo ""
else
    echo "✓ .env file already exists"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Installation Complete!                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Configure Telegram credentials:"
echo "   nano .env"
echo ""
echo "2. Test the bot:"
echo "   source venv/bin/activate"
echo "   python demo_gold.py"
echo ""
echo "3. Run the bot:"
echo "   python main.py"
echo ""
echo "4. Run in background (recommended):"
echo "   nohup python main.py > bot.log 2>&1 &"
echo ""
echo "5. Or use screen/tmux:"
echo "   screen -S goldbot"
echo "   python main.py"
echo "   # Press Ctrl+A then D to detach"
echo ""
echo "6. Check running bot:"
echo "   ps aux | grep main.py"
echo ""
echo "7. View logs:"
echo "   tail -f reversal_bot.log"
echo ""
echo "╚══════════════════════════════════════════════════════════════╝"
