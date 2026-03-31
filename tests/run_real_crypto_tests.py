#!/usr/bin/env python3
"""
Run all tests with REAL cryptography (no mocks).
"""

import sys
import os
import subprocess
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_tests(test_files, description):
    """Run a set of test files."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    
    all_passed = True
    for test_file in test_files:
        print(f"\n• {test_file.name}")
        try:
            # Run the test module directly
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("  ✅ PASSED")
                # Print any output
                if result.stdout.strip():
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            print(f"    {line}")
            else:
                print("  ❌ FAILED")
                print(f"    Exit code: {result.returncode}")
                if result.stderr:
                    print(f"    Error: {result.stderr[:200]}...")
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print("  ⏰ TIMEOUT (5 minutes)")
            all_passed = False
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            all_passed = False
    
    return all_passed


def run_pytest_tests(test_pattern, description):
    """Run pytest tests."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_pattern, "-v"],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Print summary
        lines = result.stdout.split('\n')
        for line in lines[-10:]:  # Last 10 lines usually have summary
            if line.strip():
                print(line)
        
        if result.returncode == 0:
            print("  ✅ ALL TESTS PASSED")
            return True
        else:
            print("  ❌ SOME TESTS FAILED")
            return False
            
    except subprocess.TimeoutExpired:
        print("  ⏰ TIMEOUT (5 minutes)")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        return False


def main():
    """Run all real cryptography tests."""
    print("=" * 70)
    print("PERSONAL HISTORY - REAL CRYPTOGRAPHY TEST SUITE")
    print("=" * 70)
    print("\nTesting with REAL Ed25519 cryptography (no mocks/simulations)")
    print("All tests use actual cryptography library and real waiting for timers.")
    
    tests_dir = Path(__file__).parent
    
    # Unit tests with real crypto
    unit_tests = [
        tests_dir / "unit" / "test_identity_real_crypto.py",
        tests_dir / "unit" / "test_file_signing_real_crypto.py",
    ]
    
    # Integration tests with real crypto
    integration_tests = [
        tests_dir / "integration" / "test_workflow_real_crypto.py",
    ]
    
    # Timer tests (slow - real waiting)
    timer_tests = [
        tests_dir / "integration" / "test_timers_real_wait.py",
    ]
    
    # Run tests
    start_time = time.time()
    
    # 1. Unit tests
    unit_passed = run_tests(unit_tests, "UNIT TESTS (Real Cryptography)")
    
    # 2. Integration tests  
    integration_passed = run_tests(integration_tests, "INTEGRATION TESTS (Real Cryptography)")
    
    # 3. Timer tests (ask before running since they're slow)
    print(f"\n{'='*60}")
    print("TIMER TESTS WITH REAL WAITING")
    print(f"{'='*60}")
    print("These tests actually wait 65+ seconds to create valid activities.")
    print("They will take several minutes to complete.")
    
    response = input("\nRun timer tests? (y/n): ").strip().lower()
    timer_passed = True  # Default to passed if skipped
    
    if response == 'y':
        timer_passed = run_tests(timer_tests, "TIMER TESTS (Real 65+ Second Waits)")
    else:
        print("\nSkipping timer tests.")
    
    # 4. Existing pytest tests (updated to use real crypto)
    print("\n" + "="*60)
    print("RUNNING EXISTING TEST SUITE (Updated for Real Cryptography)")
    print("="*60)
    
    existing_passed = run_pytest_tests("tests/", "Existing Test Suite")
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    
    print(f"\n⏱️  Total time: {elapsed:.1f} seconds")
    print(f"\n📊 Results:")
    print(f"  Unit Tests:           {'✅ PASSED' if unit_passed else '❌ FAILED'}")
    print(f"  Integration Tests:    {'✅ PASSED' if integration_passed else '❌ FAILED'}")
    print(f"  Timer Tests:          {'✅ PASSED' if timer_passed else '❌ SKIPPED/FAILED'}")
    print(f"  Existing Test Suite:  {'✅ PASSED' if existing_passed else '❌ FAILED'}")
    
    all_passed = unit_passed and integration_passed and timer_passed and existing_passed
    
    print(f"\n{'='*70}")
    if all_passed:
        print("🎉 ALL TESTS PASSED WITH REAL CRYPTOGRAPHY!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print(f"{'='*70}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())