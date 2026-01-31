# Reversal Pattern Detection Bot

A Python-based trading bot that detects major reversal patterns in forex markets (GOLD/USD) and sends real-time alerts via Telegram.

## Features

### Detected Patterns
- **Head & Shoulders** - Bearish reversal pattern
- **Inverse Head & Shoulders** - Bullish reversal pattern
- **Double Tops/Bottoms** - Two peaks/troughs at similar levels
- **Triple Tops/Bottoms** - Three peaks/troughs at similar levels
- **Rounding Bottom** - Gradual U-shaped bullish reversal
- **Spike (V) Pattern** - Sharp V-shaped reversals

### Capabilities
- ✅ Real-time pattern detection across multiple symbols
- ✅ Multi-timeframe analysis (1m, 5m, 15m, 1h, 4h, 1d)
- ✅ Telegram notifications with detailed alerts
- ✅ Confidence scoring for each pattern
- ✅ Configurable detection parameters
- ✅ Support for multiple exchanges via CCXT

## Installation

1. **Clone or navigate to the project directory:**
```bash
cd /Users/macbook/Desktop/Tradingbot/reversal_bot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure the bot:**
```bash
cp .env.example .env
```

Edit `.env` and add your Telegram credentials:
- Get bot token from [@BotFather](https://t.me/botfather)
- Get your chat ID from [@userinfobot](https://t.me/userinfobot)

## Configuration

Edit `.env` file to customize:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Exchange (oanda for forex, binance for crypto)
EXCHANGE=oanda

# Symbols to monitor (XAU/USD = GOLD/USD)
SYMBOLS=XAU/USD

# Timeframes
TIMEFRAMES=15m,1h,4h

# Pattern detection sensitivity
PATTERN_TOLERANCE=0.02  # 2% tolerance
MIN_CONFIDENCE=0.7      # 70% minimum confidence

# Scan interval (seconds)
SCAN_INTERVAL=60
```

## Usage

Run the bot:
```bash
python main.py
```

The bot will:
1. Test Telegram connection
2. Start monitoring configured symbols
3. Detect reversal patterns
4. Send alerts when patterns are found

## Telegram Alert Format

Alerts include:
- 📊 Symbol and timeframe
- 🔍 Pattern type
- 📈 Bullish/Bearish signal
- 💪 Confidence percentage
- 💰 Current price
- 📝 Key price levels
- 💡 Trading suggestion

## Project Structure

```
reversal_bot/
├── main.py                 # Main application
├── pattern_detector.py     # Pattern detection algorithms
├── telegram_notifier.py    # Telegram notification system
├── data_fetcher.py         # Market data fetching
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Configuration template
└── README.md             # This file
```

## Pattern Detection Details

### Head & Shoulders
- Identifies three peaks with middle peak highest
- Validates neckline support
- Bearish reversal signal

### Inverse Head & Shoulders
- Identifies three troughs with middle trough lowest
- Validates neckline resistance
- Bullish reversal signal

### Double Top/Bottom
- Detects two peaks/troughs at similar levels
- Validates significant valley/peak between them
- Strong reversal signals

### Triple Top/Bottom
- Detects three peaks/troughs at similar levels
- Higher confidence than double patterns
- Very strong reversal signals

### Rounding Bottom
- Detects U-shaped gradual reversal
- Analyzes slope symmetry
- Bullish continuation signal

### Spike (V) Pattern
- Detects sharp reversals (>5% moves)
- Both bullish and bearish variants
- High-velocity reversal signals

## Logging

Logs are saved to `reversal_bot.log` and displayed in console.

## Safety Notes

⚠️ **Important:**
- This bot is for educational purposes
- Always use proper risk management
- Verify signals before trading
- Past patterns don't guarantee future results

## Troubleshooting

**No patterns detected:**
- Adjust `PATTERN_TOLERANCE` (increase for more patterns)
- Lower `MIN_CONFIDENCE` threshold
- Increase `LOOKBACK_PERIODS`

**Telegram not working:**
- Verify bot token and chat ID
- Check internet connection
- Ensure bot is not blocked

**Exchange errors:**
- Check symbol format (e.g., BTC/USDT)
- Verify exchange supports the symbol
- Check rate limits

## License

MIT License - Free to use and modify

## Support

For issues or questions, check the logs in `reversal_bot.log`
