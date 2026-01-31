"""
Demo for GOLD (XAU/USD & XAU/EUR) with Telegram notifications
Simulates GOLD price movements and sends alerts
"""
import asyncio
import numpy as np
from pattern_detector import ReversalPatternDetector
from telegram_notifier import TelegramNotifier
from config import Config


def generate_gold_price_data(base_price=2650, length=100):
    """Generate realistic GOLD price data with patterns"""
    np.random.seed(42)
    
    # GOLD typically moves in smaller percentages than crypto
    trend = np.linspace(0, 50, length)
    noise = np.random.normal(0, 5, length)
    prices = base_price + trend + noise
    
    # Add a double bottom pattern (bullish for GOLD)
    mid = length // 2
    for i in range(mid - 10, mid + 10):
        if i < mid - 5:  # First bottom
            prices[i] -= (mid - 5 - i) * 2
        elif i < mid:  # Rise to peak
            prices[i] += (i - (mid - 5)) * 3
        elif i < mid + 5:  # Second bottom
            prices[i] -= (mid + 5 - i) * 2
        else:  # Rise after double bottom
            prices[i] += (i - (mid + 5)) * 3
    
    # Generate OHLC
    highs = prices + np.random.uniform(1, 5, length)
    lows = prices - np.random.uniform(1, 5, length)
    closes = prices
    
    return highs, lows, closes


async def demo_gold_telegram():
    """Demo GOLD pattern detection with Telegram alerts"""
    print("\n" + "="*70)
    print("🥇 GOLD REVERSAL BOT - XAU/USD & XAU/EUR")
    print("="*70)
    print("Demonstrating GOLD pattern detection with Telegram notifications")
    print("="*70 + "\n")
    
    # Initialize
    detector = ReversalPatternDetector(tolerance=0.015, min_bars=5)  # Tighter tolerance for GOLD
    notifier = TelegramNotifier(
        bot_token=Config.TELEGRAM_BOT_TOKEN,
        chat_id=Config.TELEGRAM_CHAT_ID
    )
    
    # Test Telegram
    print("📱 Testing Telegram connection...")
    success = await notifier.send_test_message()
    
    if not success:
        print("❌ Telegram connection failed. Check credentials.")
        return
    
    print("✅ Telegram connected!\n")
    
    # Simulate both GOLD pairs
    symbols = ["XAU/USD", "XAU/EUR"]
    base_prices = [2650.00, 2450.00]  # Typical GOLD prices
    
    total_alerts = 0
    
    for symbol, base_price in zip(symbols, base_prices):
        print(f"\n{'='*70}")
        print(f"📊 Analyzing {symbol} (GOLD)")
        print(f"{'='*70}")
        
        # Generate data
        highs, lows, closes = generate_gold_price_data(base_price=base_price, length=100)
        current_price = closes[-1]
        
        print(f"💰 Current Price: ${current_price:,.2f}")
        print(f"📈 Candles analyzed: {len(closes)}")
        print(f"📉 Range: ${lows.min():,.2f} - ${highs.max():,.2f}\n")
        
        # Detect patterns
        print("🔍 Detecting reversal patterns...")
        patterns = detector.detect_all_patterns(highs, lows, closes)
        
        # Filter high confidence
        high_conf = [p for p in patterns if p.confidence >= 0.7]
        
        print(f"✓ Found {len(patterns)} total patterns")
        print(f"✓ {len(high_conf)} high-confidence patterns (≥70%)\n")
        
        if high_conf:
            print(f"📤 Sending {len(high_conf)} alert(s) to Telegram for {symbol}...\n")
            
            for i, pattern in enumerate(high_conf, 1):
                print(f"   Alert #{i}: {pattern.pattern_type} ({pattern.confidence*100:.1f}%)")
                
                success = await notifier.send_pattern_alert(
                    pattern=pattern,
                    symbol=f"{symbol} (GOLD)",
                    timeframe="1h",
                    current_price=current_price
                )
                
                if success:
                    print(f"   ✅ Sent to Telegram!")
                    total_alerts += 1
                else:
                    print(f"   ❌ Failed to send")
                
                await asyncio.sleep(1)
        else:
            print("ℹ️  No high-confidence patterns detected")
    
    print("\n" + "="*70)
    print("✅ GOLD Demo Completed!")
    print("="*70)
    print(f"\n📊 Summary:")
    print(f"   • Symbols analyzed: {', '.join(symbols)}")
    print(f"   • Total alerts sent: {total_alerts}")
    print(f"\n📱 Check your Telegram for GOLD pattern alerts!")
    print("\n💡 To run with live GOLD data:")
    print("   1. Get OANDA API credentials (or use another forex broker)")
    print("   2. Add API credentials to .env file")
    print("   3. Run: python main.py")
    print("\n⚠️  This demo used simulated GOLD prices")
    print("⚠️  Always use proper risk management when trading GOLD!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_gold_telegram())
