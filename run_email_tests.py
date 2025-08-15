#!/usr/bin/env python3
"""
Email Sender Test Runner
Run this script to test the email functionality and diagnose authentication issues.
"""

import sys
import os
import subprocess
from pathlib import Path

def run_tests():
    """Run the email sender tests."""
    print("🚗 Car Selling Platform - Email Tests")
    print("=" * 50)
    
    # Check if test file exists
    test_file = Path("test_email_sender.py")
    if not test_file.exists():
        print("❌ Test file not found: test_email_sender.py")
        return False
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
        print("   Create a .env file with your Gmail credentials:")
        print("   GMAIL_USER=your_email@gmail.com")
        print("   GMAIL_PASSWORD=your_app_password")
        print()
    else:
        print("✅ .env file found")
    
    # Check if config.py exists
    config_file = Path("config.py")
    if not config_file.exists():
        print("❌ Config file not found: config.py")
        return False
    
    print("✅ Config file found")
    print()
    
    # Run the tests
    print("🧪 Running Email Sender Tests...")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "unittest", 
            "test_email_sender", "-v"
        ], capture_output=True, text=True, timeout=60)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        print(f"\nExit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Tests timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_specific_test(test_name):
    """Run a specific test by name."""
    print(f"🧪 Running specific test: {test_name}")
    print("-" * 40)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "unittest", 
            f"test_email_sender.TestEmailSender.{test_name}", "-v"
        ], capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        success = run_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
