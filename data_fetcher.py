"""
Data Fetcher Module
Fetches OHLCV data from cryptocurrency exchanges
"""
import ccxt
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import time


class DataFetcher:
    """Fetches market data from exchanges"""
    
    def __init__(self, exchange_name: str = 'binance'):
        """
        Initialize data fetcher
        
        Args:
            exchange_name: Name of the exchange (default: binance)
        """
        self.logger = logging.getLogger(__name__)
        self.exchange_name = exchange_name
        
        try:
            exchange_class = getattr(ccxt, exchange_name)
            
            # Configure based on exchange type
            config = {'enableRateLimit': True}
            
            # For forex exchanges like OANDA, don't set defaultType
            if exchange_name.lower() not in ['oanda', 'fxcm']:
                config['options'] = {'defaultType': 'spot'}
            
            self.exchange = exchange_class(config)
            self.logger.info(f"Connected to {exchange_name} exchange")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize exchange: {e}")
            raise
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', 
                    limit: int = 100) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data for a symbol
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candle timeframe (e.g., '1m', '5m', '1h', '1d')
            limit: Number of candles to fetch
            
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            # Fetch data from exchange
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            if not ohlcv:
                self.logger.warning(f"No data received for {symbol} {timeframe}")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Convert to numeric types
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            self.logger.debug(f"Fetched {len(df)} candles for {symbol} {timeframe}")
            return df
            
        except ccxt.NetworkError as e:
            self.logger.error(f"Network error fetching {symbol}: {e}")
            return None
        except ccxt.ExchangeError as e:
            self.logger.error(f"Exchange error fetching {symbol}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current market price for a symbol
        
        Args:
            symbol: Trading pair
            
        Returns:
            Current price or None if error
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return float(ticker['last'])
        except Exception as e:
            self.logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    def fetch_multiple_symbols(self, symbols: List[str], timeframe: str = '1h',
                               limit: int = 100) -> Dict[str, pd.DataFrame]:
        """
        Fetch OHLCV data for multiple symbols
        
        Args:
            symbols: List of trading pairs
            timeframe: Candle timeframe
            limit: Number of candles per symbol
            
        Returns:
            Dictionary mapping symbols to DataFrames
        """
        data = {}
        
        for symbol in symbols:
            df = self.fetch_ohlcv(symbol, timeframe, limit)
            if df is not None:
                data[symbol] = df
            
            # Small delay to respect rate limits
            time.sleep(0.2)
        
        return data
    
    def get_numpy_arrays(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, 
                                                           np.ndarray, np.ndarray]:
        """
        Convert DataFrame to numpy arrays for pattern detection
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            Tuple of (highs, lows, closes, volumes) as numpy arrays
        """
        highs = df['high'].to_numpy()
        lows = df['low'].to_numpy()
        closes = df['close'].to_numpy()
        volumes = df['volume'].to_numpy()
        
        return highs, lows, closes, volumes
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate OHLCV data quality
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            True if data is valid, False otherwise
        """
        if df is None or df.empty:
            return False
        
        # Check for required columns
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_cols):
            return False
        
        # Check for NaN values
        if df[required_cols].isnull().any().any():
            self.logger.warning("Data contains NaN values")
            return False
        
        # Check for invalid prices (high >= low, etc.)
        if not (df['high'] >= df['low']).all():
            self.logger.warning("Invalid OHLC data: high < low")
            return False
        
        if not (df['high'] >= df['close']).all():
            self.logger.warning("Invalid OHLC data: high < close")
            return False
        
        if not (df['low'] <= df['close']).all():
            self.logger.warning("Invalid OHLC data: low > close")
            return False
        
        return True
