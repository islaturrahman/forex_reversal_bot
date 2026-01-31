"""
Reversal Pattern Detection Bot
Main application that monitors markets and sends Telegram alerts
"""
import asyncio
import logging
import sys
from datetime import datetime
from typing import Set, Tuple

from config import Config
from data_fetcher import DataFetcher
from pattern_detector import ReversalPatternDetector
from telegram_notifier import TelegramNotifier


class ReversalBot:
    """Main bot orchestrator"""
    
    def __init__(self):
        """Initialize the reversal bot"""
        # Setup logging
        self._setup_logging()
        
        # Validate configuration
        if not Config.validate():
            self.logger.error("Invalid configuration. Please check your .env file")
            sys.exit(1)
        
        Config.display()
        
        # Initialize components
        self.data_fetcher = DataFetcher(Config.EXCHANGE)
        self.pattern_detector = ReversalPatternDetector(
            tolerance=Config.PATTERN_TOLERANCE,
            min_bars=Config.MIN_BARS
        )
        self.telegram_notifier = TelegramNotifier(
            bot_token=Config.TELEGRAM_BOT_TOKEN,
            chat_id=Config.TELEGRAM_CHAT_ID
        )
        
        # Track already notified patterns to avoid duplicates
        self.notified_patterns: Set[Tuple[str, str, str]] = set()
        
        self.logger.info("Reversal Bot initialized successfully")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('reversal_bot.log')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def test_connection(self) -> bool:
        """
        Test Telegram connection
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("Testing Telegram connection...")
        success = await self.telegram_notifier.send_test_message()
        
        if success:
            self.logger.info("✓ Telegram connection successful")
        else:
            self.logger.error("✗ Telegram connection failed")
        
        return success
    
    async def scan_symbol(self, symbol: str, timeframe: str):
        """
        Scan a single symbol for reversal patterns
        
        Args:
            symbol: Trading pair to scan
            timeframe: Timeframe to analyze
        """
        try:
            # Fetch market data
            df = self.data_fetcher.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=Config.LOOKBACK_PERIODS
            )
            
            if df is None or not self.data_fetcher.validate_data(df):
                self.logger.warning(f"Invalid data for {symbol} {timeframe}")
                return
            
            # Convert to numpy arrays
            highs, lows, closes, volumes = self.data_fetcher.get_numpy_arrays(df)
            
            # Detect patterns
            patterns = self.pattern_detector.detect_all_patterns(highs, lows, closes)
            
            # Filter by confidence threshold
            high_confidence_patterns = [
                p for p in patterns 
                if p.confidence >= Config.MIN_CONFIDENCE
            ]
            
            if not high_confidence_patterns:
                self.logger.debug(f"No high-confidence patterns found for {symbol} {timeframe}")
                return
            
            # Get current price
            current_price = self.data_fetcher.get_current_price(symbol)
            if current_price is None:
                current_price = closes[-1]
            
            # Send notifications for new patterns
            for pattern in high_confidence_patterns:
                # Create unique identifier for this pattern
                pattern_id = (symbol, timeframe, pattern.pattern_type)
                
                # Skip if already notified
                if pattern_id in self.notified_patterns:
                    continue
                
                # Send Telegram alert
                success = await self.telegram_notifier.send_pattern_alert(
                    pattern=pattern,
                    symbol=symbol,
                    timeframe=timeframe,
                    current_price=current_price
                )
                
                if success:
                    self.notified_patterns.add(pattern_id)
                    self.logger.info(
                        f"✓ Alert sent: {pattern.pattern_type} on {symbol} {timeframe} "
                        f"(Confidence: {pattern.confidence*100:.1f}%)"
                    )
                
                # Small delay between notifications
                await asyncio.sleep(1)
        
        except Exception as e:
            self.logger.error(f"Error scanning {symbol} {timeframe}: {e}")
            await self.telegram_notifier.send_error_alert(
                f"Error scanning {symbol} {timeframe}: {str(e)}"
            )
    
    async def scan_all_markets(self):
        """Scan all configured symbols and timeframes"""
        self.logger.info("Starting market scan...")
        
        tasks = []
        for symbol in Config.SYMBOLS:
            for timeframe in Config.TIMEFRAMES:
                task = self.scan_symbol(symbol, timeframe)
                tasks.append(task)
        
        # Run all scans concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.logger.info("Market scan completed")
    
    async def run(self):
        """Main bot loop"""
        self.logger.info("Starting Reversal Bot...")
        
        # Test Telegram connection
        if not await self.test_connection():
            self.logger.error("Failed to connect to Telegram. Exiting...")
            return
        
        # Main monitoring loop
        scan_count = 0
        try:
            while True:
                scan_count += 1
                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"Scan #{scan_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info(f"{'='*60}")
                
                # Scan all markets
                await self.scan_all_markets()
                
                # Clear old notifications periodically (every 10 scans)
                if scan_count % 10 == 0:
                    self.logger.info("Clearing notification cache...")
                    self.notified_patterns.clear()
                
                # Wait before next scan
                self.logger.info(f"Waiting {Config.SCAN_INTERVAL} seconds until next scan...")
                await asyncio.sleep(Config.SCAN_INTERVAL)
        
        except KeyboardInterrupt:
            self.logger.info("\nBot stopped by user")
        except Exception as e:
            self.logger.error(f"Fatal error: {e}")
            await self.telegram_notifier.send_error_alert(f"Fatal error: {str(e)}")
            raise


async def main():
    """Entry point"""
    bot = ReversalBot()
    await bot.run()


if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())
