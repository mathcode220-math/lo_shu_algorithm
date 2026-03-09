"""
Main Runner for Lo Shu Algorithm Tests
=======================================
Run this file to execute all tests and generate results.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tests.test_suite import LoShuTestSuite, save_test_images


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("       LO SHU BALANCE ALGORITHM - TEST RUNNER")
    print("=" * 70)
    print("\nBased on the Lo Shu Magic Square (3x3) properties:")
    print("  8  1  6")
    print("  3  5  7")
    print("  4  9  2")
    print("\nMagic Constant: 15 | Center: 5 | Diagonal Pairs Sum: 10")
    print("=" * 70 + "\n")
    
    # Run test suite
    suite = LoShuTestSuite()
    results = suite.run_all_tests()
    
    # Generate test images
    print("\nGenerating sample test images...")
    test_images = save_test_images()
    
    print("\n" + "=" * 70)
    print("TEST EXECUTION COMPLETE")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    main()
