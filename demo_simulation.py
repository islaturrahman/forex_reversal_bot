"""
Demo script with simulated data - Shows pattern detection in action
No internet connection required
"""
import numpy as np
from pattern_detector import ReversalPatternDetector


def generate_realistic_price_data(base_price=100000, length=100):
    """Generate realistic price data with patterns"""
    np.random.seed(42)
    
    # Create base trend
    trend = np.linspace(0, 10, length)
    noise = np.random.normal(0, 500, length)
    prices = base_price + trend * 100 + noise
    
    # Add a head and shoulders pattern in the middle
    mid = length // 2
    for i in range(mid - 15, mid + 15):
        if i < mid - 10:  # Left shoulder
            prices[i] += (i - (mid - 15)) * 200
        elif i < mid - 5:  # Down to trough
            prices[i] += (mid - 10 - i) * 200
        elif i < mid:  # Up to head
            prices[i] += (i - (mid - 5)) * 400
        elif i < mid + 5:  # Down from head
            prices[i] += (mid - i) * 400
        elif i < mid + 10:  # Up to right shoulder
            prices[i] += (i - (mid + 5)) * 200
        else:  # Down from right shoulder
            prices[i] += (mid + 15 - i) * 200
    
    # Generate OHLC from close prices
    highs = prices + np.random.uniform(100, 500, length)
    lows = prices - np.random.uniform(100, 500, length)
    closes = prices
    
    return highs, lows, closes


def main():
    print("\n" + "="*70)
    print("🚀 REVERSAL PATTERN DETECTION BOT - SIMULATION DEMO")
    print("="*70)
    print("Demonstrating pattern detection with simulated BTC/USDT data")
    print("="*70 + "\n")
    
    # Initialize detector
    detector = ReversalPatternDetector(tolerance=0.02, min_bars=10)
    
    # Generate simulated data
    print("📊 Generating simulated market data...")
    highs, lows, closes = generate_realistic_price_data(base_price=100000, length=100)
    
    current_price = closes[-1]
    print(f"💰 Simulated Current Price: ${current_price:,.2f}")
    print(f"📈 Candles analyzed: {len(closes)}")
    print(f"📉 Price Range: ${lows.min():,.2f} - ${highs.max():,.2f}\n")
    
    # Detect all patterns
    print("🔍 Scanning for reversal patterns...\n")
    print("-" * 70)
    
    patterns = detector.detect_all_patterns(highs, lows, closes)
    
    if patterns:
        print(f"\n🎯 Found {len(patterns)} pattern(s):\n")
        
        for i, pattern in enumerate(patterns, 1):
            # Determine signal type
            bullish_patterns = [
                "Inverse Head and Shoulders",
                "Double Bottom",
                "Triple Bottom",
                "Rounding Bottom",
                "Spike V (Bullish)"
            ]
            
            is_bullish = pattern.pattern_type in bullish_patterns
            signal_emoji = "🟢" if is_bullish else "🔴"
            signal_type = "BULLISH" if is_bullish else "BEARISH"
            
            print(f"{signal_emoji} Pattern #{i}: {pattern.pattern_type}")
            print(f"   Signal: {signal_type}")
            print(f"   Confidence: {pattern.confidence * 100:.1f}%")
            print(f"   Candles: {pattern.start_idx} to {pattern.end_idx}")
            print(f"   Description: {pattern.description}")
            
            # Show key levels
            print(f"   Key Price Levels:")
            for level_name, level_value in pattern.key_levels.items():
                formatted_name = level_name.replace('_', ' ').title()
                print(f"     • {formatted_name}: ${level_value:,.2f}")
            
            # Trading suggestion
            if is_bullish:
                print(f"   💡 Suggestion: Consider LONG position")
                print(f"   🎯 Potential Entry: ${current_price:,.2f}")
                if 'resistance' in pattern.key_levels:
                    print(f"   🎯 Target: ${pattern.key_levels['resistance']:,.2f}")
            else:
                print(f"   💡 Suggestion: Consider SHORT position")
                print(f"   🎯 Potential Entry: ${current_price:,.2f}")
                if 'support' in pattern.key_levels:
                    print(f"   🎯 Target: ${pattern.key_levels['support']:,.2f}")
            
            print()
    else:
        print("ℹ️  No patterns detected in this dataset")
    
    print("=" * 70)
    print("✅ Simulation completed!")
    print("=" * 70)
    print("\n📋 Pattern Detection Summary:")
    print(f"   • Total patterns detected: {len(patterns)}")
    
    # Count by type
    pattern_types = {}
    for p in patterns:
        pattern_types[p.pattern_type] = pattern_types.get(p.pattern_type, 0) + 1
    
    if pattern_types:
        print("\n   Pattern breakdown:")
        for ptype, count in pattern_types.items():
            print(f"     • {ptype}: {count}")
    
    # Show high confidence patterns
    high_conf = [p for p in patterns if p.confidence >= 0.7]
    print(f"\n   High confidence patterns (≥70%): {len(high_conf)}")
    
    print("\n" + "=" * 70)
    print("💡 Next Steps:")
    print("   1. Configure Telegram credentials in .env file")
    print("   2. Run: python main.py (for live trading)")
    print("   3. Run: python demo.py (for live data without Telegram)")
    print("\n⚠️  Remember: This is a simulation. Always backtest with real data!")
    print("⚠️  Always use proper risk management when trading!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
