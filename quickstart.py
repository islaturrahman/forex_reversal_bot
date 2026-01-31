"""
Quick Start Guide for GOLD/USD Reversal Bot
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║         GOLD/USD REVERSAL PATTERN DETECTION BOT             ║
╚══════════════════════════════════════════════════════════════╝

📋 SETUP INSTRUCTIONS:

1. Install Dependencies:
   pip install -r requirements.txt

2. Configure Telegram:
   - Create a bot with @BotFather on Telegram
   - Get your bot token
   - Get your chat ID from @userinfobot
   - Edit .env file and add your credentials

3. Configure Exchange (Optional):
   The bot is pre-configured for GOLD/USD (XAU/USD) on OANDA.
   
   For other exchanges or symbols, edit .env:
   - EXCHANGE=oanda (or binance, etc.)
   - SYMBOLS=XAU/USD (or EUR/USD, BTC/USDT, etc.)

4. Run the Bot:
   python main.py

═══════════════════════════════════════════════════════════════

📊 DETECTED PATTERNS:

✓ Head & Shoulders (Bearish)
✓ Inverse Head & Shoulders (Bullish)
✓ Double Top/Bottom
✓ Triple Top/Bottom
✓ Rounding Bottom (Bullish)
✓ Spike V Pattern (Both directions)

═══════════════════════════════════════════════════════════════

⚙️  CONFIGURATION (.env file):

TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EXCHANGE=oanda
SYMBOLS=XAU/USD
TIMEFRAMES=15m,1h,4h
SCAN_INTERVAL=60
MIN_CONFIDENCE=0.7

═══════════════════════════════════════════════════════════════

🧪 TESTING:

Run test script to verify pattern detection:
   python test_patterns.py

═══════════════════════════════════════════════════════════════

📱 TELEGRAM ALERTS INCLUDE:

• Pattern type and direction (bullish/bearish)
• Confidence level
• Current price
• Key support/resistance levels
• Trading suggestions

═══════════════════════════════════════════════════════════════

⚠️  IMPORTANT NOTES:

• OANDA requires API credentials for live data
• For testing, you can use 'binance' exchange (no auth needed)
• Always use proper risk management
• This is for educational purposes

═══════════════════════════════════════════════════════════════

🚀 QUICK START COMMANDS:

# Install dependencies
pip install -r requirements.txt

# Edit configuration
nano .env

# Test pattern detection
python test_patterns.py

# Run the bot
python main.py

═══════════════════════════════════════════════════════════════

For more information, see README.md

Good luck trading! 📈
""")
