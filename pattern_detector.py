"""
Reversal Pattern Detection Module
Detects major reversal patterns in price data
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Pattern:
    """Represents a detected pattern"""
    pattern_type: str
    confidence: float
    start_idx: int
    end_idx: int
    key_levels: Dict[str, float]
    description: str


class ReversalPatternDetector:
    """Detects reversal patterns in OHLCV data"""
    
    def __init__(self, tolerance: float = 0.02, min_bars: int = 10):
        """
        Initialize pattern detector
        
        Args:
            tolerance: Price tolerance for pattern matching (2% default)
            min_bars: Minimum bars required for pattern detection
        """
        self.tolerance = tolerance
        self.min_bars = min_bars
    
    def detect_all_patterns(self, highs: np.ndarray, lows: np.ndarray, 
                           closes: np.ndarray) -> List[Pattern]:
        """
        Detect all reversal patterns in the data
        
        Args:
            highs: Array of high prices
            lows: Array of low prices
            closes: Array of close prices
            
        Returns:
            List of detected patterns
        """
        patterns = []
        
        # Detect each pattern type
        patterns.extend(self.detect_head_and_shoulders(highs, lows, closes))
        patterns.extend(self.detect_inverse_head_and_shoulders(highs, lows, closes))
        patterns.extend(self.detect_double_top(highs, closes))
        patterns.extend(self.detect_double_bottom(lows, closes))
        patterns.extend(self.detect_triple_top(highs, closes))
        patterns.extend(self.detect_triple_bottom(lows, closes))
        patterns.extend(self.detect_rounding_bottom(lows, closes))
        patterns.extend(self.detect_spike_pattern(highs, lows, closes))
        
        return patterns
    
    def detect_head_and_shoulders(self, highs: np.ndarray, lows: np.ndarray, 
                                  closes: np.ndarray) -> List[Pattern]:
        """
        Detect Head and Shoulders pattern (bearish reversal)
        Pattern: Left Shoulder < Head > Right Shoulder with neckline support
        """
        patterns = []
        n = len(highs)
        
        if n < 20:
            return patterns
        
        # Look for three peaks
        for i in range(10, n - 10):
            # Find potential head (highest point)
            head_idx = i
            head_high = highs[head_idx]
            
            # Find left shoulder (peak before head)
            left_shoulder_idx = None
            for j in range(head_idx - 10, head_idx - 3):
                if self._is_local_peak(highs, j, window=3):
                    left_shoulder_idx = j
                    break
            
            if left_shoulder_idx is None:
                continue
            
            # Find right shoulder (peak after head)
            right_shoulder_idx = None
            for j in range(head_idx + 3, min(head_idx + 10, n - 1)):
                if self._is_local_peak(highs, j, window=3):
                    right_shoulder_idx = j
                    break
            
            if right_shoulder_idx is None:
                continue
            
            left_shoulder_high = highs[left_shoulder_idx]
            right_shoulder_high = highs[right_shoulder_idx]
            
            # Validate pattern structure
            # 1. Head should be higher than both shoulders
            if head_high <= left_shoulder_high or head_high <= right_shoulder_high:
                continue
            
            # 2. Shoulders should be roughly equal height
            shoulder_diff = abs(left_shoulder_high - right_shoulder_high) / left_shoulder_high
            if shoulder_diff > self.tolerance:
                continue
            
            # 3. Find neckline (support level connecting troughs)
            trough1_idx = left_shoulder_idx + np.argmin(lows[left_shoulder_idx:head_idx])
            trough2_idx = head_idx + np.argmin(lows[head_idx:right_shoulder_idx])
            neckline = (lows[trough1_idx] + lows[trough2_idx]) / 2
            
            # Calculate confidence
            confidence = self._calculate_hs_confidence(
                head_high, left_shoulder_high, right_shoulder_high, shoulder_diff
            )
            
            pattern = Pattern(
                pattern_type="Head and Shoulders",
                confidence=confidence,
                start_idx=left_shoulder_idx,
                end_idx=right_shoulder_idx,
                key_levels={
                    "head": head_high,
                    "left_shoulder": left_shoulder_high,
                    "right_shoulder": right_shoulder_high,
                    "neckline": neckline
                },
                description=f"Bearish H&S: Head={head_high:.2f}, Neckline={neckline:.2f}"
            )
            patterns.append(pattern)
        
        return patterns
    
    def detect_inverse_head_and_shoulders(self, highs: np.ndarray, lows: np.ndarray, 
                                         closes: np.ndarray) -> List[Pattern]:
        """
        Detect Inverse Head and Shoulders pattern (bullish reversal)
        Pattern: Left Shoulder > Head < Right Shoulder with neckline resistance
        """
        patterns = []
        n = len(lows)
        
        if n < 20:
            return patterns
        
        # Look for three troughs
        for i in range(10, n - 10):
            # Find potential head (lowest point)
            head_idx = i
            head_low = lows[head_idx]
            
            # Find left shoulder (trough before head)
            left_shoulder_idx = None
            for j in range(head_idx - 10, head_idx - 3):
                if self._is_local_trough(lows, j, window=3):
                    left_shoulder_idx = j
                    break
            
            if left_shoulder_idx is None:
                continue
            
            # Find right shoulder (trough after head)
            right_shoulder_idx = None
            for j in range(head_idx + 3, min(head_idx + 10, n - 1)):
                if self._is_local_trough(lows, j, window=3):
                    right_shoulder_idx = j
                    break
            
            if right_shoulder_idx is None:
                continue
            
            left_shoulder_low = lows[left_shoulder_idx]
            right_shoulder_low = lows[right_shoulder_idx]
            
            # Validate pattern structure
            # 1. Head should be lower than both shoulders
            if head_low >= left_shoulder_low or head_low >= right_shoulder_low:
                continue
            
            # 2. Shoulders should be roughly equal depth
            shoulder_diff = abs(left_shoulder_low - right_shoulder_low) / left_shoulder_low
            if shoulder_diff > self.tolerance:
                continue
            
            # 3. Find neckline (resistance level connecting peaks)
            peak1_idx = left_shoulder_idx + np.argmax(highs[left_shoulder_idx:head_idx])
            peak2_idx = head_idx + np.argmax(highs[head_idx:right_shoulder_idx])
            neckline = (highs[peak1_idx] + highs[peak2_idx]) / 2
            
            # Calculate confidence
            confidence = self._calculate_hs_confidence(
                head_low, left_shoulder_low, right_shoulder_low, shoulder_diff
            )
            
            pattern = Pattern(
                pattern_type="Inverse Head and Shoulders",
                confidence=confidence,
                start_idx=left_shoulder_idx,
                end_idx=right_shoulder_idx,
                key_levels={
                    "head": head_low,
                    "left_shoulder": left_shoulder_low,
                    "right_shoulder": right_shoulder_low,
                    "neckline": neckline
                },
                description=f"Bullish IH&S: Head={head_low:.2f}, Neckline={neckline:.2f}"
            )
            patterns.append(pattern)
        
        return patterns
    
    def detect_double_top(self, highs: np.ndarray, closes: np.ndarray) -> List[Pattern]:
        """
        Detect Double Top pattern (bearish reversal)
        Two peaks at similar price levels
        """
        patterns = []
        n = len(highs)
        
        if n < 15:
            return patterns
        
        for i in range(5, n - 10):
            if not self._is_local_peak(highs, i, window=3):
                continue
            
            first_peak = highs[i]
            
            # Look for second peak
            for j in range(i + 5, min(i + 20, n - 1)):
                if not self._is_local_peak(highs, j, window=3):
                    continue
                
                second_peak = highs[j]
                
                # Check if peaks are at similar levels
                peak_diff = abs(first_peak - second_peak) / first_peak
                if peak_diff > self.tolerance:
                    continue
                
                # Find valley between peaks
                valley_idx = i + np.argmin(highs[i:j])
                valley_level = highs[valley_idx]
                
                # Validate pattern: valley should be significantly lower
                if (first_peak - valley_level) / first_peak < 0.02:
                    continue
                
                confidence = 1.0 - peak_diff
                
                pattern = Pattern(
                    pattern_type="Double Top",
                    confidence=confidence,
                    start_idx=i,
                    end_idx=j,
                    key_levels={
                        "peak1": first_peak,
                        "peak2": second_peak,
                        "support": valley_level
                    },
                    description=f"Bearish Double Top: Peaks={first_peak:.2f}, Support={valley_level:.2f}"
                )
                patterns.append(pattern)
        
        return patterns
    
    def detect_double_bottom(self, lows: np.ndarray, closes: np.ndarray) -> List[Pattern]:
        """
        Detect Double Bottom pattern (bullish reversal)
        Two troughs at similar price levels
        """
        patterns = []
        n = len(lows)
        
        if n < 15:
            return patterns
        
        for i in range(5, n - 10):
            if not self._is_local_trough(lows, i, window=3):
                continue
            
            first_bottom = lows[i]
            
            # Look for second bottom
            for j in range(i + 5, min(i + 20, n - 1)):
                if not self._is_local_trough(lows, j, window=3):
                    continue
                
                second_bottom = lows[j]
                
                # Check if bottoms are at similar levels
                bottom_diff = abs(first_bottom - second_bottom) / first_bottom
                if bottom_diff > self.tolerance:
                    continue
                
                # Find peak between bottoms
                peak_idx = i + np.argmax(lows[i:j])
                peak_level = lows[peak_idx]
                
                # Validate pattern: peak should be significantly higher
                if (peak_level - first_bottom) / first_bottom < 0.02:
                    continue
                
                confidence = 1.0 - bottom_diff
                
                pattern = Pattern(
                    pattern_type="Double Bottom",
                    confidence=confidence,
                    start_idx=i,
                    end_idx=j,
                    key_levels={
                        "bottom1": first_bottom,
                        "bottom2": second_bottom,
                        "resistance": peak_level
                    },
                    description=f"Bullish Double Bottom: Bottoms={first_bottom:.2f}, Resistance={peak_level:.2f}"
                )
                patterns.append(pattern)
        
        return patterns
    
    def detect_triple_top(self, highs: np.ndarray, closes: np.ndarray) -> List[Pattern]:
        """
        Detect Triple Top pattern (bearish reversal)
        Three peaks at similar price levels
        """
        patterns = []
        n = len(highs)
        
        if n < 25:
            return patterns
        
        for i in range(5, n - 20):
            if not self._is_local_peak(highs, i, window=3):
                continue
            
            first_peak = highs[i]
            
            # Look for second peak
            second_peak_idx = None
            for j in range(i + 5, min(i + 15, n - 10)):
                if self._is_local_peak(highs, j, window=3):
                    if abs(highs[j] - first_peak) / first_peak <= self.tolerance:
                        second_peak_idx = j
                        break
            
            if second_peak_idx is None:
                continue
            
            # Look for third peak
            for k in range(second_peak_idx + 5, min(second_peak_idx + 15, n - 1)):
                if not self._is_local_peak(highs, k, window=3):
                    continue
                
                third_peak = highs[k]
                
                # Check if all peaks are at similar levels
                avg_peak = (first_peak + highs[second_peak_idx] + third_peak) / 3
                if abs(first_peak - avg_peak) / avg_peak > self.tolerance:
                    continue
                if abs(highs[second_peak_idx] - avg_peak) / avg_peak > self.tolerance:
                    continue
                if abs(third_peak - avg_peak) / avg_peak > self.tolerance:
                    continue
                
                # Find support level
                support = min(np.min(highs[i:second_peak_idx]), 
                            np.min(highs[second_peak_idx:k]))
                
                confidence = 0.95
                
                pattern = Pattern(
                    pattern_type="Triple Top",
                    confidence=confidence,
                    start_idx=i,
                    end_idx=k,
                    key_levels={
                        "peak1": first_peak,
                        "peak2": highs[second_peak_idx],
                        "peak3": third_peak,
                        "support": support
                    },
                    description=f"Bearish Triple Top: Peaks≈{avg_peak:.2f}, Support={support:.2f}"
                )
                patterns.append(pattern)
        
        return patterns
    
    def detect_triple_bottom(self, lows: np.ndarray, closes: np.ndarray) -> List[Pattern]:
        """
        Detect Triple Bottom pattern (bullish reversal)
        Three troughs at similar price levels
        """
        patterns = []
        n = len(lows)
        
        if n < 25:
            return patterns
        
        for i in range(5, n - 20):
            if not self._is_local_trough(lows, i, window=3):
                continue
            
            first_bottom = lows[i]
            
            # Look for second bottom
            second_bottom_idx = None
            for j in range(i + 5, min(i + 15, n - 10)):
                if self._is_local_trough(lows, j, window=3):
                    if abs(lows[j] - first_bottom) / first_bottom <= self.tolerance:
                        second_bottom_idx = j
                        break
            
            if second_bottom_idx is None:
                continue
            
            # Look for third bottom
            for k in range(second_bottom_idx + 5, min(second_bottom_idx + 15, n - 1)):
                if not self._is_local_trough(lows, k, window=3):
                    continue
                
                third_bottom = lows[k]
                
                # Check if all bottoms are at similar levels
                avg_bottom = (first_bottom + lows[second_bottom_idx] + third_bottom) / 3
                if abs(first_bottom - avg_bottom) / avg_bottom > self.tolerance:
                    continue
                if abs(lows[second_bottom_idx] - avg_bottom) / avg_bottom > self.tolerance:
                    continue
                if abs(third_bottom - avg_bottom) / avg_bottom > self.tolerance:
                    continue
                
                # Find resistance level
                resistance = max(np.max(lows[i:second_bottom_idx]), 
                               np.max(lows[second_bottom_idx:k]))
                
                confidence = 0.95
                
                pattern = Pattern(
                    pattern_type="Triple Bottom",
                    confidence=confidence,
                    start_idx=i,
                    end_idx=k,
                    key_levels={
                        "bottom1": first_bottom,
                        "bottom2": lows[second_bottom_idx],
                        "bottom3": third_bottom,
                        "resistance": resistance
                    },
                    description=f"Bullish Triple Bottom: Bottoms≈{avg_bottom:.2f}, Resistance={resistance:.2f}"
                )
                patterns.append(pattern)
        
        return patterns
    
    def detect_rounding_bottom(self, lows: np.ndarray, closes: np.ndarray) -> List[Pattern]:
        """
        Detect Rounding Bottom pattern (bullish reversal)
        Gradual U-shaped curve
        """
        patterns = []
        n = len(lows)
        
        if n < 30:
            return patterns
        
        # Use sliding window to detect U-shape
        window_size = 20
        for i in range(n - window_size):
            window = lows[i:i + window_size]
            
            # Check if it forms a U-shape
            left_third = window[:window_size // 3]
            middle_third = window[window_size // 3:2 * window_size // 3]
            right_third = window[2 * window_size // 3:]
            
            # Middle should be lower than sides
            if np.mean(middle_third) >= np.mean(left_third) or \
               np.mean(middle_third) >= np.mean(right_third):
                continue
            
            # Check for gradual descent and ascent
            left_slope = np.polyfit(range(len(left_third)), left_third, 1)[0]
            right_slope = np.polyfit(range(len(right_third)), right_third, 1)[0]
            
            # Left should descend, right should ascend
            if left_slope >= 0 or right_slope <= 0:
                continue
            
            # Check symmetry
            if abs(abs(left_slope) - abs(right_slope)) / abs(left_slope) > 0.5:
                continue
            
            bottom_level = np.min(window)
            entry_level = lows[i]
            exit_level = lows[i + window_size - 1]
            
            # Calculate confidence based on symmetry
            confidence = 1.0 - (abs(abs(left_slope) - abs(right_slope)) / abs(left_slope))
            
            pattern = Pattern(
                pattern_type="Rounding Bottom",
                confidence=confidence,
                start_idx=i,
                end_idx=i + window_size - 1,
                key_levels={
                    "bottom": bottom_level,
                    "entry": entry_level,
                    "current": exit_level
                },
                description=f"Bullish Rounding Bottom: Bottom={bottom_level:.2f}, Current={exit_level:.2f}"
            )
            patterns.append(pattern)
        
        return patterns
    
    def detect_spike_pattern(self, highs: np.ndarray, lows: np.ndarray, 
                            closes: np.ndarray) -> List[Pattern]:
        """
        Detect Spike (V) pattern - sharp reversal
        Rapid price movement followed by immediate reversal
        """
        patterns = []
        n = len(closes)
        
        if n < 10:
            return patterns
        
        # Look for sharp V-shaped reversals
        for i in range(5, n - 5):
            # Calculate price velocity before and after
            before_change = (closes[i] - closes[i - 5]) / closes[i - 5]
            after_change = (closes[i + 5] - closes[i]) / closes[i]
            
            # Bullish V: Sharp drop followed by sharp rise
            if before_change < -0.05 and after_change > 0.05:
                spike_low = lows[i]
                confidence = min(abs(before_change), abs(after_change)) / 0.1
                
                pattern = Pattern(
                    pattern_type="Spike V (Bullish)",
                    confidence=min(confidence, 1.0),
                    start_idx=i - 5,
                    end_idx=i + 5,
                    key_levels={
                        "spike_low": spike_low,
                        "entry": closes[i - 5],
                        "exit": closes[i + 5]
                    },
                    description=f"Bullish Spike: Low={spike_low:.2f}, Recovery={after_change*100:.1f}%"
                )
                patterns.append(pattern)
            
            # Bearish Inverse V: Sharp rise followed by sharp drop
            elif before_change > 0.05 and after_change < -0.05:
                spike_high = highs[i]
                confidence = min(abs(before_change), abs(after_change)) / 0.1
                
                pattern = Pattern(
                    pattern_type="Spike V (Bearish)",
                    confidence=min(confidence, 1.0),
                    start_idx=i - 5,
                    end_idx=i + 5,
                    key_levels={
                        "spike_high": spike_high,
                        "entry": closes[i - 5],
                        "exit": closes[i + 5]
                    },
                    description=f"Bearish Spike: High={spike_high:.2f}, Drop={after_change*100:.1f}%"
                )
                patterns.append(pattern)
        
        return patterns
    
    # Helper methods
    def _is_local_peak(self, data: np.ndarray, idx: int, window: int = 3) -> bool:
        """Check if index is a local peak"""
        if idx < window or idx >= len(data) - window:
            return False
        
        local_data = data[idx - window:idx + window + 1]
        return data[idx] == np.max(local_data)
    
    def _is_local_trough(self, data: np.ndarray, idx: int, window: int = 3) -> bool:
        """Check if index is a local trough"""
        if idx < window or idx >= len(data) - window:
            return False
        
        local_data = data[idx - window:idx + window + 1]
        return data[idx] == np.min(local_data)
    
    def _calculate_hs_confidence(self, head: float, left_shoulder: float, 
                                 right_shoulder: float, shoulder_diff: float) -> float:
        """Calculate confidence for H&S pattern"""
        # Higher confidence if shoulders are more symmetric
        symmetry_score = 1.0 - shoulder_diff
        
        # Higher confidence if head is significantly different from shoulders
        head_prominence = abs(head - (left_shoulder + right_shoulder) / 2) / head
        prominence_score = min(head_prominence / 0.05, 1.0)
        
        return (symmetry_score * 0.6 + prominence_score * 0.4)
