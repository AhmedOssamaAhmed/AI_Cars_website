#!/usr/bin/env python3
"""
Test script for the Car Selling Platform
Run this to verify all components are working correctly
"""

import sys
import os
import tempfile
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow (PIL) imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import smtplib
        print("✅ SMTP library imported successfully")
    except ImportError as e:
        print(f"❌ SMTP import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration file loading."""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
        print("✅ Configuration loaded successfully")
        print(f"   API Key: {AZURE_OPENAI_API_KEY[:10]}...")
        print(f"   Endpoint: {AZURE_OPENAI_ENDPOINT[:50]}...")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_image_classifier():
    """Test the dummy image classifier."""
    print("\n🔍 Testing image classifier...")
    
    try:
        from image_classifier import CarImageClassifier
        
        classifier = CarImageClassifier()
        print("✅ Image classifier initialized successfully")
        
        # Test with dummy image path
        result = classifier.classify_car_type("dummy_path.jpg")
        print(f"✅ Classification result: {result['car_type']} (confidence: {result['confidence']:.1%})")
        
        return True
    except Exception as e:
        print(f"❌ Image classifier test failed: {e}")
        return False

def test_text_processor():
    """Test the text processor (without API calls)."""
    print("\n🔍 Testing text processor...")
    
    try:
        from text_processor import TextProcessor
        
        processor = TextProcessor()
        print("✅ Text processor initialized successfully")
        
        # Test input sanitization
        test_text = "This is a test car description"
        sanitized = processor.sanitize_input(test_text)
        print(f"✅ Input sanitization: '{test_text}' -> '{sanitized}'")
        
        # Test validation
        is_valid, error_msg = processor.validate_input(test_text)
        print(f"✅ Input validation: {is_valid} (error: {error_msg})")
        
        return True
    except Exception as e:
        print(f"❌ Text processor test failed: {e}")
        return False

def test_email_sender():
    """Test email sender initialization."""
    print("\n🔍 Testing email sender...")
    
    try:
        from email_sender import EmailSender
        
        sender = EmailSender()
        print("✅ Email sender initialized successfully")
        
        # Test credential validation
        is_valid = sender.validate_credentials()
        print(f"✅ Credential validation: {is_valid}")
        
        return True
    except Exception as e:
        print(f"❌ Email sender test failed: {e}")
        return False

def test_streamlit_app():
    """Test if the main app can be imported."""
    print("\n🔍 Testing main application...")
    
    try:
        import main_app
        print("✅ Main application imported successfully")
        return True
    except Exception as e:
        print(f"❌ Main application import failed: {e}")
        return False

def create_test_image():
    """Create a test image for testing."""
    print("\n🔍 Creating test image...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple test image
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add some text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 50), "Test Car Image", fill='black', font=font)
        draw.text((50, 100), "For Platform Testing", fill='black', font=font)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            img.save(tmp_file.name, 'JPEG')
            print(f"✅ Test image created: {tmp_file.name}")
            return tmp_file.name
            
    except Exception as e:
        print(f"❌ Test image creation failed: {e}")
        return None

def run_all_tests():
    """Run all tests and provide summary."""
    print("🚗 Car Selling Platform - Component Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Image Classifier", test_image_classifier),
        ("Text Processor", test_text_processor),
        ("Email Sender", test_email_sender),
        ("Main Application", test_streamlit_app),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("streamlit run main_app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
