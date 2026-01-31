"""
Demo with Telegram - Sends pattern alerts to your Telegram
Uses simulated data to demonstrate notifications
"""
import asyncio
import numpy as np
from pattern_detector import ReversalPatternDetector, Pattern
from telegram_notifier import TelegramNotifier
from config import Config


def generate_pattern_data():
    """Generate data with clear patterns"""
    np.random.seed(42)
    
    # Create Head & Shoulders pattern
    base = 100000
    prices = []
    
    # Uptrend to left shoulder
    for i in range(10):
        prices.append(base + i * 200 + np.random.uniform(-100, 100))
    
    # Left shoulder peak
    for i in range(3):
        prices.append(base + 2000 + np.random.uniform(-50, 50))
    
    # Down to trough
    for i in range(5):
        prices.append(base + 2000 - i * 300 + np.random.uniform(-100, 100))
    
    # Up to head
    for i in range(7):
        prices.append(base + 500 + i * 400 + np.random.uniform(-100, 100))
    
    # Down from head
    for i in range(7):
        prices.append(base + 3300 - i * 400 + np.random.uniform(-100, 100))
    
    # Up to right shoulder
    for i in range(5):
        prices.append(base + 500 + i * 300 + np.random.uniform(-100, 100))
    
    # Right shoulder peak
    for i in range(3):
        prices.append(base + 2000 + np.random.uniform(-50, 50))
    
    # Downtrend
    for i in range(10):
        prices.append(base + 2000 - i * 200 + np.random.uniform(-100, 100))
    
    prices = np.array(prices)
    highs = prices + np.random.uniform(50, 200, len(prices))
    lows = prices - np.random.uniform(50, 200, len(prices))
    closes = prices
    
    return highs, lows, closes


async def demo_with_telegram():
    """Demo that sends alerts to Telegram"""
    print("\n" + "="*70)
    print("🚀 REVERSAL BOT - TELEGRAM NOTIFICATION DEMO")
    print("="*70)
    print("This demo will send pattern detection alerts to your Telegram")
    print("="*70 + "\n")
    
    # Initialize
    detector = ReversalPatternDetector(tolerance=0.03, min_bars=5)
    notifier = TelegramNotifier(
        bot_token=Config.TELEGRAM_BOT_TOKEN,
        chat_id=Config.TELEGRAM_CHAT_ID
    )
    
    # Test Telegram connection
    print("📱 Testing Telegram connection...")
    success = await notifier.send_test_message()
    
    if not success:
        print("❌ Telegram connection failed. Please check your credentials.")
        return
    
    print("✅ Telegram connected successfully!\n")
    
    # Generate data
    print("📊 Generating simulated BTC/USDT data with patterns...")
    highs, lows, closes = generate_pattern_data()
    current_price = closes[-1]
    
    print(f"💰 Simulated Price: ${current_price:,.2f}")
    print(f"📈 Analyzing {len(closes)} candles...\n")
    
    # Detect patterns
    print("🔍 Detecting reversal patterns...")
    patterns = detector.detect_all_patterns(highs, lows, closes)
    
    # Filter high confidence
    high_conf_patterns = [p for p in patterns if p.confidence >= 0.7]
    
    print(f"✓ Found {len(patterns)} total patterns")
    print(f"✓ {len(high_conf_patterns)} high-confidence patterns (≥70%)\n")
    
    if high_conf_patterns:
        print(f"📤 Sending {len(high_conf_patterns)} alert(s) to Telegram...\n")
        
        for i, pattern in enumerate(high_conf_patterns, 1):
            print(f"   Sending alert #{i}: {pattern.pattern_type} ({pattern.confidence*100:.1f}%)")
            
            success = await notifier.send_pattern_alert(
                pattern=pattern,
                symbol="BTC/USDT (DEMO)",
                timeframe="1h",
                current_price=current_price
            )
            
            if success:
                print(f"   ✅ Alert sent successfully!")
            else:
                print(f"   ❌ Failed to send alert")
            
            # Small delay between messages
            await asyncio.sleep(1)
    else:
        print("ℹ️  No high-confidence patterns to send")
    
    print("\n" + "="*70)
    print("✅ Demo completed!")
    print("="*70)
    print("\n📱 Check your Telegram for the pattern alerts!")
    print("\n💡 To run with live data:")
    print("   1. Fix internet connection to Binance API")
    print("   2. Run: python main.py")
    print("\n⚠️  This was a demo with simulated data")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_with_telegram())
