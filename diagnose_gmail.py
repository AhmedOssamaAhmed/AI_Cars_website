#!/usr/bin/env python3
"""
Gmail Configuration Diagnostic Tool
This script helps diagnose Gmail authentication issues.
"""

import os
import sys
import smtplib
import ssl
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and load it."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Create a .env file in your project root with:")
        print("   GMAIL_USER=your_email@gmail.com")
        print("   GMAIL_PASSWORD=your_app_password")
        return False
    
    print("✅ .env file found")
    
    # Load environment variables
    load_dotenv()
    return True

def check_credentials():
    """Check if Gmail credentials are properly set."""
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    
    if not gmail_user or gmail_user == "your-email@gmail.com":
        print("❌ GMAIL_USER not properly configured")
        print("   Current value:", gmail_user)
        return False
    
    if not gmail_password or gmail_password == "your-app-password":
        print("❌ GMAIL_PASSWORD not properly configured")
        print("   Current value:", gmail_password[:10] + "..." if gmail_password else "None")
        return False
    
    print("✅ Gmail credentials found")
    print(f"   User: {gmail_user}")
    print(f"   Password: {gmail_password[:10]}...")
    return True

def test_smtp_connection(gmail_user, gmail_password):
    """Test SMTP connection to Gmail."""
    print("\n🔌 Testing SMTP Connection...")
    
    try:
        # Create SMTP connection
        print("   Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        
        # Start TLS
        print("   Starting TLS...")
        server.starttls(context=ssl.create_default_context())
        
        # Login
        print("   Attempting login...")
        server.login(gmail_user, gmail_password)
        
        print("✅ SMTP connection successful!")
        print("✅ Gmail authentication successful!")
        
        # Close connection
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure 2-Factor Authentication is enabled on your Gmail account")
        print("   2. Generate an App Password (not your regular password)")
        print("   3. Go to: myaccount.google.com → Security → 2-Step Verification → App passwords")
        print("   4. Select 'Mail' and generate a new password")
        print("   5. Update your .env file with the new app password")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("   Check your internet connection and firewall settings")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_gmail_settings():
    """Provide Gmail setup instructions."""
    print("\n📋 Gmail Setup Checklist:")
    print("   1. ✅ Enable 2-Factor Authentication on your Gmail account")
    print("   2. ✅ Generate an App Password for 'Mail'")
    print("   3. ✅ Update your .env file with the app password")
    print("   4. ✅ Make sure the .env file is in your project root")
    print("   5. ✅ Never commit the .env file to version control")

def main():
    """Main diagnostic function."""
    print("🚗 Car Selling Platform - Gmail Diagnostic Tool")
    print("=" * 55)
    
    # Check environment file
    if not check_env_file():
        return
    
    # Check credentials
    if not check_credentials():
        return
    
    # Get credentials
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    
    # Test SMTP connection
    if test_smtp_connection(gmail_user, gmail_password):
        print("\n🎉 Gmail configuration is working correctly!")
        print("   You should be able to send emails from the application.")
    else:
        print("\n⚠️  Gmail configuration has issues.")
        check_gmail_settings()
    
    print("\n" + "=" * 55)

if __name__ == "__main__":
    main()
