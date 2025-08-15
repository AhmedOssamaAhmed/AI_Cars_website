# 🚗 Car Selling Platform - Setup Guide

## 🔐 Environment Variables Setup

To use this application securely, you need to create a `.env` file in your project root directory.

### Step 1: Create .env file
Create a file named `.env` (no extension) in your project directory with the following content:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=<add your own key>
AZURE_OPENAI_ENDPOINT=https://orionopenai2-techtest.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini-AO242

# Gmail Configuration (Update these with your credentials)
GMAIL_USER=your_actual_gmail@gmail.com
GMAIL_PASSWORD=your_actual_gmail_app_password
```

### Step 2: Gmail Setup
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to [myaccount.google.com](https://myaccount.google.com)
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and generate a password
   - Copy the 16-character password
3. **Update the .env file** with your actual Gmail and app password

### Step 3: Run the Application
```bash
streamlit run main_app.py
```

## 🎯 How It Works Now

1. **Upload Car Image** → AI detects car type
2. **Enter Your Email** → Where to receive the car details
3. **Describe the Car** → AI extracts structured information
4. **Submit** → Car details sent to your email in the new JSON format

## 📧 New JSON Output Format

The application now generates car information in this structure:

```json
{
  "car": {
    "body_type": "sedan",
    "color": "Blue",
    "brand": "Ford",
    "model": "Fusion",
    "manufactured_year": 2015,
    "motor_size_cc": 2000,
    "tires": {
      "type": "brand-new",
      "manufactured_year": 2022
    },
    "windows": "tinted",
    "notices": [
      {
        "type": "collision",
        "description": "The rear bumper has been replaced after a minor collision."
      }
    ],
    "price": {
      "amount": 1000000,
      "currency": "L.E"
    }
  }
}
```

## 🔒 Security Features

- **Environment Variables**: Sensitive data stored in .env file (not in code)
- **User Email Input**: Users specify where to send their car details
- **Prompt Injection Prevention**: AI input sanitization and validation
- **No Data Storage**: All processing done in memory

## 🚨 Important Notes

- **Never commit your .env file** to version control
- **Use app passwords, not regular Gmail passwords**
- **Keep your Azure OpenAI API key secure**
- **The .env file should be in your .gitignore**

## 🆘 Troubleshooting

If you encounter issues:
1. Check that your .env file is in the project root
2. Verify Gmail credentials and 2FA setup
3. Ensure Azure OpenAI credentials are correct
4. Check the application logs for specific error messages
