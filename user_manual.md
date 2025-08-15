# 🚗 Car Selling Platform - User Manual

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Guide](#installation-guide)
3. [Gmail Configuration](#gmail-configuration)
4. [First-Time Setup](#first-time-setup)
5. [Using the Application](#using-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Features](#advanced-features)
8. [FAQs](#frequently-asked-questions)

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11 (as specified)
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet**: Stable connection for Azure OpenAI and Gmail

### Recommended Requirements
- **Operating System**: Windows 11
- **Python**: Version 3.9 or higher
- **RAM**: 8GB or higher
- **Storage**: 1GB free space
- **Internet**: High-speed connection (10+ Mbps)

## 🚀 Installation Guide

### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, **check "Add Python to PATH"**
3. Verify installation by opening Command Prompt:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Download the Application
1. Clone or download the repository to your local machine
2. Open Command Prompt in the project directory
3. Create a virtual environment (recommended):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

### Step 3: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 4: Verify Installation
```cmd
python -c "import streamlit, openai, PIL; print('All packages installed successfully!')"
```

## 📧 Gmail Configuration

### Prerequisites
- Gmail account with 2-Factor Authentication enabled
- Access to Google Account settings

### Step-by-Step Setup

#### 1. Enable 2-Factor Authentication
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the setup process

#### 2. Generate App Password
1. In Google Account settings, go to "Security"
2. Under "2-Step Verification", click "App passwords"
3. Select "Mail" from the dropdown
4. Click "Generate"
5. **Copy the 16-character password** (you won't see it again)

#### 3. Update Configuration
1. Open `config.py` in your project
2. Replace `your-email@gmail.com` with your Gmail address
3. Replace `your-app-password` with the generated app password
4. Save the file

## 🎯 First-Time Setup

### Step 1: Launch the Application
```cmd
streamlit run main_app.py
```

### Step 2: Configure Gmail in the App
1. The application will open in your browser
2. In the sidebar, enter your Gmail credentials
3. Click outside the input fields to save
4. Verify the status shows "✅ Gmail configured"

### Step 3: Test Configuration
1. Upload a test car image
2. Enter a simple car description
3. Process the description to test AI functionality
4. Submit a test listing to verify email delivery

## 📖 Using the Application

### Workflow Overview
```
Upload Image → Analyze Car Type → Enter Description → Process Text → Submit & Send Email
```

### Detailed Steps

#### Step 1: Upload Car Image
1. **Click "Choose a car image"** in the left column
2. **Select your image file**:
   - Supported formats: JPG, JPEG, PNG, BMP
   - Maximum size: 10MB
   - Recommended: Clear, well-lit car photos
3. **Wait for upload** - the image will display automatically
4. **Click "🔍 Analyze Car Type"** to detect car type

**Tips for Better Image Classification:**
- Use clear, high-resolution images
- Ensure the car is the main subject
- Avoid extreme angles or poor lighting
- Include the entire car in the frame

#### Step 2: Enter Car Description
1. **In the right column**, find the "Describe the car" text area
2. **Enter comprehensive details** including:
   - Make and model
   - Year of manufacture
   - Price (in USD)
   - Mileage (in miles)
   - Condition (new, used, excellent, good, fair, poor)
   - Fuel type (gasoline, diesel, electric, hybrid)
   - Transmission (automatic, manual, CVT)
   - Color
   - Special features (leather seats, sunroof, etc.)
   - Any additional details

**Example Description:**
```
"2019 Toyota Camry SE, excellent condition, 45,000 miles, automatic transmission, 
silver color, leather seats, sunroof, navigation system, backup camera, 
asking $22,500. Well maintained with full service history."
```

#### Step 3: Process Description
1. **Click "🧠 Process Description"** button
2. **Wait for AI processing** (usually 2-5 seconds)
3. **Review extracted information** in the JSON format
4. **Verify accuracy** of extracted fields

#### Step 4: Submit Listing
1. **Review the submission summary** showing:
   - Car details
   - Detected car type
   - Confidence level
   - Price information
2. **Click "🚀 Submit & Send Email"**
3. **Wait for confirmation** of successful email delivery

### Configuration Panel (Sidebar)

#### Gmail Settings
- **Gmail Address**: Your Gmail account
- **App Password**: The 16-character app password
- **Status Indicator**: Shows configuration status

#### Application Information
- **Technology Stack**: Lists used technologies
- **Status Indicators**: System health monitoring

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Gmail Authentication Failed
**Symptoms**: Error message "Gmail authentication failed"
**Solutions**:
- Verify 2-factor authentication is enabled
- Use app password, not regular password
- Check Gmail address spelling
- Ensure app password is copied correctly

#### 2. Image Upload Issues
**Symptoms**: Image won't upload or displays error
**Solutions**:
- Check file format (JPG, PNG, BMP only)
- Reduce file size (max 10MB)
- Try a different image
- Restart the application

#### 3. AI Processing Errors
**Symptoms**: "Text processing failed" or similar errors
**Solutions**:
- Check internet connection
- Verify Azure OpenAI credentials
- Ensure description is detailed enough
- Try shorter description first

#### 4. Email Not Sent
**Symptoms**: "Failed to send email" error
**Solutions**:
- Check Gmail configuration in sidebar
- Verify recipient email address
- Check spam folder
- Ensure Gmail account has sending permissions

#### 5. Application Won't Start
**Symptoms**: Streamlit fails to launch
**Solutions**:
- Verify Python installation
- Check all dependencies are installed
- Try running in Command Prompt as Administrator
- Check firewall/antivirus settings

### Debug Mode
Enable detailed logging for troubleshooting:
```cmd
set STREAMLIT_LOG_LEVEL=debug
streamlit run main_app.py
```

### Error Logs
Check the Command Prompt output for detailed error messages when issues occur.

## 🔧 Advanced Features

### Custom Configuration
- **Modify config.py** for permanent credential storage
- **Adjust image size limits** in configuration
- **Customize email templates** in email_sender.py

### Batch Processing
- Process multiple car descriptions sequentially
- Use the same image for multiple listings
- Maintain session state between submissions

### Data Export
- JSON data is automatically attached to emails
- Copy extracted information from the interface
- Use browser developer tools for data extraction

## ❓ Frequently Asked Questions

### Q: Can I use a different email provider?
**A**: Currently, the application is designed for Gmail. Other providers would require code modifications.

### Q: What if the AI misidentifies the car type?
**A**: The car type is automatically detected from the image. For now, it's a dummy model. The real CV model will provide more accurate results.

### Q: How accurate is the text extraction?
**A**: GPT-4o mini provides high accuracy for well-structured descriptions. Include detailed information for best results.

### Q: Can I edit the extracted information before sending?
**A**: Currently, the extracted information is sent as-is. Future versions may include editing capabilities.

### Q: Is my data stored anywhere?
**A**: No, all data is processed in memory and sent via email. No persistent storage is implemented.

### Q: What happens if the email fails to send?
**A**: The application will show an error message. Check your Gmail configuration and try again.

### Q: Can I use this for other types of vehicles?
**A**: The current dummy model is designed for cars. The real CV model can be trained for other vehicle types.

### Q: How do I update the application?
**A**: Pull the latest code from the repository and reinstall dependencies if needed.

## 📞 Getting Help

### Support Resources
1. **Check this manual** for common solutions
2. **Review error messages** in the application
3. **Check Command Prompt output** for detailed logs
4. **Contact**: msamy@orion360.com

### Reporting Issues
When reporting issues, include:
- Error message text
- Steps to reproduce
- System information
- Screenshots if applicable

---

**Last Updated**: January 2024  
**Version**: 1.0  
**Platform**: Windows PC
