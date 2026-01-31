"""
Test script for pattern detection
Tests pattern detection algorithms with sample data
"""
import numpy as np
from pattern_detector import ReversalPatternDetector


def generate_head_and_shoulders_data():
    """Generate synthetic H&S pattern"""
    # Left shoulder
    left = [100, 105, 110, 108, 105, 102, 100]
    # Head
    head = [102, 108, 115, 120, 118, 112, 105]
    # Right shoulder
    right = [107, 110, 108, 105, 102, 100, 98]
    
    prices = left + head + right
    highs = np.array([p + np.random.uniform(0, 2) for p in prices])
    lows = np.array([p - np.random.uniform(0, 2) for p in prices])
    closes = np.array(prices)
    
    return highs, lows, closes


def generate_double_bottom_data():
    """Generate synthetic double bottom pattern"""
    prices = [100, 95, 90, 85, 88, 92, 95, 93, 90, 87, 85, 88, 92, 97, 100]
    
    highs = np.array([p + np.random.uniform(0, 2) for p in prices])
    lows = np.array([p - np.random.uniform(0, 2) for p in prices])
    closes = np.array(prices)
    
    return highs, lows, closes


def generate_spike_pattern_data():
    """Generate synthetic spike V pattern"""
    # Sharp drop then sharp recovery
    prices = [100, 98, 95, 90, 85, 80, 85, 90, 95, 100, 105]
    
    highs = np.array([p + np.random.uniform(0, 1) for p in prices])
    lows = np.array([p - np.random.uniform(0, 1) for p in prices])
    closes = np.array(prices)
    
    return highs, lows, closes


def test_pattern_detection():
    """Test pattern detection with synthetic data"""
    detector = ReversalPatternDetector(tolerance=0.03, min_bars=5)
    
    print("\n" + "="*60)
    print("PATTERN DETECTION TEST")
    print("="*60)
    
    # Test Head & Shoulders
    print("\n1. Testing Head & Shoulders Detection...")
    highs, lows, closes = generate_head_and_shoulders_data()
    patterns = detector.detect_head_and_shoulders(highs, lows, closes)
    print(f"   Found {len(patterns)} H&S pattern(s)")
    for p in patterns:
        print(f"   - {p.description}")
        print(f"     Confidence: {p.confidence*100:.1f}%")
    
    # Test Double Bottom
    print("\n2. Testing Double Bottom Detection...")
    highs, lows, closes = generate_double_bottom_data()
    patterns = detector.detect_double_bottom(lows, closes)
    print(f"   Found {len(patterns)} Double Bottom pattern(s)")
    for p in patterns:
        print(f"   - {p.description}")
        print(f"     Confidence: {p.confidence*100:.1f}%")
    
    # Test Spike Pattern
    print("\n3. Testing Spike V Pattern Detection...")
    highs, lows, closes = generate_spike_pattern_data()
    patterns = detector.detect_spike_pattern(highs, lows, closes)
    print(f"   Found {len(patterns)} Spike pattern(s)")
    for p in patterns:
        print(f"   - {p.description}")
        print(f"     Confidence: {p.confidence*100:.1f}%")
    
    # Test all patterns together
    print("\n4. Testing All Patterns Detection...")
    highs, lows, closes = generate_head_and_shoulders_data()
    all_patterns = detector.detect_all_patterns(highs, lows, closes)
    print(f"   Total patterns found: {len(all_patterns)}")
    for p in all_patterns:
        print(f"   - {p.pattern_type}: {p.confidence*100:.1f}% confidence")
    
    print("\n" + "="*60)
    print("✓ Pattern detection tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_pattern_detection()
