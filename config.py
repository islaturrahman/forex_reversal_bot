"""
Configuration Module
Manages bot settings and credentials
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration settings"""
    
    # Telegram Settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Exchange Settings (oanda for forex, binance for crypto)
    EXCHANGE = os.getenv('EXCHANGE', 'oanda')
    
    # Trading Symbols to Monitor
    SYMBOLS = os.getenv('SYMBOLS', 'XAU/USD').split(',')
    
    # Timeframes to Monitor (in minutes)
    TIMEFRAMES = os.getenv('TIMEFRAMES', '15m,1h,4h').split(',')
    
    # Pattern Detection Settings
    PATTERN_TOLERANCE = float(os.getenv('PATTERN_TOLERANCE', '0.02'))  # 2% default
    MIN_BARS = int(os.getenv('MIN_BARS', '10'))
    LOOKBACK_PERIODS = int(os.getenv('LOOKBACK_PERIODS', '100'))
    
    # Bot Settings
    SCAN_INTERVAL = int(os.getenv('SCAN_INTERVAL', '60'))  # seconds
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.7'))  # 70% minimum
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration
        
        Returns:
            True if config is valid, False otherwise
        """
        errors = []
        
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is not set")
        
        if not cls.TELEGRAM_CHAT_ID:
            errors.append("TELEGRAM_CHAT_ID is not set")
        
        if not cls.SYMBOLS:
            errors.append("No symbols configured")
        
        if not cls.TIMEFRAMES:
            errors.append("No timeframes configured")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (without sensitive data)"""
        print("\n" + "="*50)
        print("REVERSAL BOT CONFIGURATION")
        print("="*50)
        print(f"Exchange: {cls.EXCHANGE}")
        print(f"Symbols: {', '.join(cls.SYMBOLS)}")
        print(f"Timeframes: {', '.join(cls.TIMEFRAMES)}")
        print(f"Pattern Tolerance: {cls.PATTERN_TOLERANCE * 100}%")
        print(f"Min Confidence: {cls.MIN_CONFIDENCE * 100}%")
        print(f"Scan Interval: {cls.SCAN_INTERVAL}s")
        print(f"Lookback Periods: {cls.LOOKBACK_PERIODS}")
        print(f"Telegram Configured: {'✓' if cls.TELEGRAM_BOT_TOKEN else '✗'}")
        print("="*50 + "\n")
