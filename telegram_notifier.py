"""
Telegram Notification Module
Sends pattern detection alerts to Telegram
"""
import asyncio
from typing import List, Optional
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import logging

from pattern_detector import Pattern


class TelegramNotifier:
    """Sends trading alerts to Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Telegram chat ID to send messages to
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id
        self.logger = logging.getLogger(__name__)
        
    async def send_pattern_alert(self, pattern: Pattern, symbol: str, 
                                 timeframe: str, current_price: float) -> bool:
        """
        Send pattern detection alert to Telegram
        
        Args:
            pattern: Detected pattern object
            symbol: Trading symbol (e.g., BTC/USDT)
            timeframe: Timeframe (e.g., 1h, 4h, 1d)
            current_price: Current market price
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            message = self._format_pattern_message(
                pattern, symbol, timeframe, current_price
            )
            
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            
            self.logger.info(f"Sent alert for {pattern.pattern_type} on {symbol}")
            return True
            
        except TelegramError as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending message: {e}")
            return False
    
    async def send_multiple_alerts(self, patterns: List[Pattern], symbol: str,
                                   timeframe: str, current_price: float) -> int:
        """
        Send multiple pattern alerts
        
        Args:
            patterns: List of detected patterns
            symbol: Trading symbol
            timeframe: Timeframe
            current_price: Current market price
            
        Returns:
            Number of successfully sent messages
        """
        success_count = 0
        
        for pattern in patterns:
            if await self.send_pattern_alert(pattern, symbol, timeframe, current_price):
                success_count += 1
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
        
        return success_count
    
    def _format_pattern_message(self, pattern: Pattern, symbol: str,
                                timeframe: str, current_price: float) -> str:
        """
        Format pattern detection message for Telegram
        
        Args:
            pattern: Detected pattern
            symbol: Trading symbol
            timeframe: Timeframe
            current_price: Current price
            
        Returns:
            Formatted HTML message
        """
        # Determine if bullish or bearish
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
        
        # Build message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
{signal_emoji} <b>REVERSAL PATTERN DETECTED</b> {signal_emoji}

📊 <b>Symbol:</b> {symbol}
⏰ <b>Timeframe:</b> {timeframe}
🔍 <b>Pattern:</b> {pattern.pattern_type}
📈 <b>Signal:</b> {signal_type}
💪 <b>Confidence:</b> {pattern.confidence * 100:.1f}%

💰 <b>Current Price:</b> ${current_price:.2f}

<b>Key Levels:</b>
"""
        
        # Add key levels
        for level_name, level_value in pattern.key_levels.items():
            formatted_name = level_name.replace('_', ' ').title()
            message += f"  • {formatted_name}: ${level_value:.2f}\n"
        
        message += f"\n📝 <b>Description:</b>\n{pattern.description}"
        message += f"\n\n🕐 <b>Time:</b> {timestamp}"
        
        # Add trading suggestion
        if is_bullish:
            message += "\n\n💡 <b>Suggestion:</b> Consider LONG position"
        else:
            message += "\n\n💡 <b>Suggestion:</b> Consider SHORT position"
        
        message += "\n\n⚠️ <i>Always use proper risk management!</i>"
        
        return message
    
    async def send_test_message(self) -> bool:
        """
        Send test message to verify Telegram connection
        
        Returns:
            True if successful, False otherwise
        """
        try:
            test_message = """
🤖 <b>Reversal Bot Connected!</b>

✅ Telegram notifications are working properly.
🔍 Bot is now monitoring for reversal patterns.

Patterns being monitored:
  • Head & Shoulders
  • Inverse Head & Shoulders
  • Double Tops/Bottoms
  • Triple Tops/Bottoms
  • Rounding Bottom
  • Spike (V) Patterns

Good luck trading! 📈
"""
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=test_message,
                parse_mode='HTML'
            )
            
            self.logger.info("Test message sent successfully")
            return True
            
        except TelegramError as e:
            self.logger.error(f"Failed to send test message: {e}")
            return False
    
    async def send_error_alert(self, error_message: str) -> bool:
        """
        Send error alert to Telegram
        
        Args:
            error_message: Error description
            
        Returns:
            True if successful, False otherwise
        """
        try:
            message = f"""
⚠️ <b>BOT ERROR</b> ⚠️

An error occurred in the reversal bot:

<code>{error_message}</code>

Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send error alert: {e}")
            return False
