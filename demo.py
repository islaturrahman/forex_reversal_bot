"""
Demo script - Run bot without Telegram for testing
Shows pattern detection in action
"""
import asyncio
import logging
import sys
from datetime import datetime

from config import Config
from data_fetcher import DataFetcher
from pattern_detector import ReversalPatternDetector


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def demo_scan():
    """Demo scan without Telegram"""
    print("\n" + "="*70)
    print("🚀 REVERSAL PATTERN DETECTION BOT - DEMO MODE")
    print("="*70)
    print(f"Exchange: {Config.EXCHANGE}")
    print(f"Symbol: {Config.SYMBOLS[0]}")
    print(f"Timeframes: {', '.join(Config.TIMEFRAMES)}")
    print(f"Min Confidence: {Config.MIN_CONFIDENCE * 100}%")
    print("="*70 + "\n")
    
    # Initialize components
    data_fetcher = DataFetcher(Config.EXCHANGE)
    pattern_detector = ReversalPatternDetector(
        tolerance=Config.PATTERN_TOLERANCE,
        min_bars=Config.MIN_BARS
    )
    
    symbol = Config.SYMBOLS[0]
    
    for timeframe in Config.TIMEFRAMES:
        print(f"\n📊 Scanning {symbol} on {timeframe} timeframe...")
        print("-" * 70)
        
        try:
            # Fetch data
            df = data_fetcher.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=Config.LOOKBACK_PERIODS
            )
            
            if df is None or not data_fetcher.validate_data(df):
                logger.warning(f"Invalid data for {symbol} {timeframe}")
                continue
            
            # Get current price
            current_price = data_fetcher.get_current_price(symbol)
            if current_price is None:
                current_price = df['close'].iloc[-1]
            
            print(f"💰 Current Price: ${current_price:,.2f}")
            print(f"📈 Candles analyzed: {len(df)}")
            
            # Convert to numpy arrays
            highs, lows, closes, volumes = data_fetcher.get_numpy_arrays(df)
            
            # Detect patterns
            patterns = pattern_detector.detect_all_patterns(highs, lows, closes)
            
            # Filter by confidence
            high_confidence_patterns = [
                p for p in patterns 
                if p.confidence >= Config.MIN_CONFIDENCE
            ]
            
            if high_confidence_patterns:
                print(f"\n🎯 Found {len(high_confidence_patterns)} high-confidence pattern(s):\n")
                
                for i, pattern in enumerate(high_confidence_patterns, 1):
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
                    print(f"   Description: {pattern.description}")
                    
                    # Show key levels
                    print(f"   Key Levels:")
                    for level_name, level_value in pattern.key_levels.items():
                        formatted_name = level_name.replace('_', ' ').title()
                        print(f"     • {formatted_name}: ${level_value:,.2f}")
                    
                    if is_bullish:
                        print(f"   💡 Suggestion: Consider LONG position")
                    else:
                        print(f"   💡 Suggestion: Consider SHORT position")
                    print()
            else:
                print(f"ℹ️  No high-confidence patterns detected")
                
                # Show all patterns with lower confidence
                if patterns:
                    print(f"\n📋 Found {len(patterns)} pattern(s) with lower confidence:")
                    for pattern in patterns:
                        print(f"   • {pattern.pattern_type}: {pattern.confidence * 100:.1f}%")
        
        except Exception as e:
            logger.error(f"Error scanning {symbol} {timeframe}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("✅ Demo scan completed!")
    print("="*70)
    print("\n💡 To enable Telegram notifications:")
    print("   1. Get bot token from @BotFather")
    print("   2. Get chat ID from @userinfobot")
    print("   3. Edit .env file and add credentials")
    print("   4. Run: python main.py")
    print("\n⚠️  Remember: Always use proper risk management!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demo_scan())
