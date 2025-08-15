#!/usr/bin/env python3
"""
Car Selling Platform - Launcher Script
Run this script from the project root to start the application.
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit application."""
    try:
        # Check if we're in the right directory
        if not os.path.exists("src/main_app.py"):
            print("❌ Error: Please run this script from the project root directory.")
            print("   Make sure you're in the folder containing the 'src' directory.")
            sys.exit(1)
        
        print("🚗 Starting Car Selling Platform...")
        print("📁 Using source directory: src/")
        print("🌐 The app will open at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        print("-" * 50)
        
        # Run the Streamlit application
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/main_app.py",
            "--server.port", "8501"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
