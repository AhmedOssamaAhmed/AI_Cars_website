# 🚗 Car Selling Platform

An AI-powered car listing platform that combines **real AI image classification**, natural language processing, and automated email delivery to streamline the car selling process.

## ✨ Features

- **🖼️ Real AI Image Classification**: Uses Microsoft ResNet-50 model for accurate car type detection
- **🧠 Smart Text Processing**: Uses GPT-4o mini to extract structured car information from descriptions
- **📧 Automated Email Delivery**: Sends car listings with images and JSON data to user's email
- **🔒 Security Features**: Prompt injection prevention and input validation
- **🎨 Modern UI**: Beautiful Streamlit interface with responsive design
- **⚙️ Environment-based Configuration**: Secure setup through .env file
- **📊 Structured Output**: Generates clean JSON format matching your specifications
- **🤖 Free AI Model**: No API costs for image classification

## 🏗️ Architecture

The platform consists of four main components:

1. **AI Image Classifier**: Uses Microsoft ResNet-50 for real car type detection
2. **Text Processor**: Uses Azure OpenAI GPT-4o mini to extract structured information
3. **Email Sender**: Delivers car listings via Gmail SMTP
4. **Web Interface**: Streamlit-based user interface for easy interaction

## 🚀 Quick Start

### 🌐 **Live Demo (AWS EC2)**
**Access the deployed application directly:**
- **URL**: http://16.16.129.60:8501
- **Status**: Live and running on AWS EC2
- **No setup required** - just open the link in your browser!

### Prerequisites

- Python 3.8 or higher
- Gmail account with app password
- Internet connection for Azure OpenAI API
- **4GB+ RAM** (for AI model loading)

### Installation (Local Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd car-selling-platform
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: This will download the AI model (~100MB) on first run

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update with your credentials:
     ```env
     GMAIL_USER=your_actual_gmail@gmail.com
     GMAIL_PASSWORD=your_actual_gmail_app_password
     AZURE_OPENAI_API_KEY=your_azure_openai_api_key
     ```

5. **Run the application**
   ```bash
   streamlit run main_app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`
   - The application will open automatically

## 🔑 Environment Configuration

### Create .env File

Create a `.env` file in your project root with the following structure:

```env
# Gmail Configuration (for testing)
GMAIL_USER=msamy@orion360.com
GMAIL_PASSWORD=your_gmail_app_password_here

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://orionopenai2-techtest.openai.azure.com
AZURE_OPENAI_API_KEY=GET_YOUR_OWN_API_KEY
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini-AO242
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Application Settings
MAX_IMAGE_SIZE=10485760
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,bmp
```

### Important Notes:

- **Gmail Credentials**: You can use `msamy@orion360.com` for testing, but you need to provide your own Gmail app password
- **API Key**: **DO NOT use the provided API key** - get your own from Azure OpenAI
- **App Password**: Generate a Gmail app password (not your regular password)

### How to Get Gmail App Password:

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate a password for "Mail"
4. Use this password in your `.env` file

## 📖 Usage Guide

### Step 1: Upload Car Image
1. Click "Choose a car image" in the left column
2. Select a clear image of the car (JPG, PNG, or BMP format)
3. Click "🔍 Analyze Car Type" to detect the car type using AI

### Step 2: Enter Your Email & Describe the Car
1. In the right column, enter your email address to receive the car details
2. Enter a detailed description of the car including brand, model, year, color, engine size, price, condition, any issues, etc.
3. Click "🧠 Process Description" to extract structured information

### Step 3: Submit Listing
1. Review the extracted information
2. Click "🚀 Submit & Send Email" to send the listing
3. The system will automatically send an email with the car image and JSON data

## 🔧 Configuration

### Gmail Setup

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
3. **Update .env file** with your credentials

### Azure OpenAI

**⚠️ IMPORTANT**: You need to get your own API key:
- **Deployment**: gpt-4o-mini-AO242
- **Endpoint**: orionopenai2-techtest.openai.azure.com
- **API Key**: **Get your own from Azure OpenAI portal**

## 🚀 Deployment

### AWS EC2 Deployment

The application is currently deployed and running on AWS EC2:

- **Instance**: AWS EC2 (t3.medium or higher recommended)
- **Public IP**: 16.16.129.60
- **Port**: 8501 (Streamlit default)
- **Access URL**: http://16.16.129.60:8501
- **Status**: ✅ Live and accessible

### Deployment Steps (for reference)

1. **Launch EC2 Instance**
   - Use Ubuntu 22.04 LTS or Amazon Linux 2
   - Configure security group to allow port 8501
   - Attach Elastic IP for consistent access

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

3. **Deploy Application**
   ```bash
   git clone <repository-url>
   cd car-selling-platform
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run with Streamlit**
   ```bash
   streamlit run main_app.py --server.port 8501 --server.address 0.0.0.0
   ```

5. **Access Application**
   - Open http://16.16.129.60:8501 in your browser

## 🛡️ Security Features

### Prompt Injection Prevention
- Pattern-based filtering of suspicious inputs
- Input sanitization and validation
- Content length limitations
- System prompt isolation

### Data Validation
- File type restrictions (JPG, PNG, BMP)
- File size limits (10MB maximum)
- Content appropriateness checks
- Error handling for malformed inputs

## 📁 Project Structure

```
car-selling-platform/
├── main_app.py              # Main Streamlit application
├── image_classifier.py      # AI-powered car type detection (ResNet-50)
├── text_processor.py        # AI text processing with GPT-4o mini
├── email_sender.py          # Email delivery system
├── config.py                # Configuration and credentials
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create from .env.example)
├── solution_design.md       # Architecture and design documentation
├── README.md               # This file
└── user_manual.md          # Detailed user instructions
```

## 🔍 Sample Input/Output

### Input Example
**Image**: Car photo (JPG/PNG)
**Description**: "2019 Toyota Camry SE, excellent condition, 45,000 miles, automatic transmission, silver color, leather seats, sunroof, asking $22,500"

### Output JSON
```json
{
  "car": {
    "brand": "Toyota",
    "model": "Camry SE",
    "manufactured_year": "2019",
    "body_type": "sedan",
    "color": "Silver",
    "motor_size_cc": "2500",
    "tires": {
      "type": "all-season",
      "condition": "good"
    },
    "windows": {
      "type": "tinted",
      "condition": "excellent"
    },
    "notices": [
      {
        "type": "collision",
        "description": "Minor scratch on rear bumper."
      }
    ],
    "price": {
      "amount": "22500",
      "currency": "USD"
    }
  }
}
```

## 🚧 Future Enhancements

- **Enhanced CV Model**: Fine-tuned car-specific classification model
- **Database Storage**: Persistent storage for car listings
- **User Authentication**: Secure user management system
- **API Endpoints**: RESTful API for external integrations
- **Analytics Dashboard**: Usage tracking and reporting
- **Multi-language Support**: Internationalization features

## 🐛 Troubleshooting

### Common Issues

1. **Gmail Authentication Failed**
   - Ensure you're using an app password, not your regular password
   - Check that 2-factor authentication is enabled
   - Verify the email address is correct

2. **AI Model Loading Issues**
   - Ensure you have 4GB+ RAM available
   - Check internet connection for model download
   - Restart the application if model fails to load

3. **Image Upload Issues**
   - Check file format (JPG, PNG, BMP only)
   - Ensure file size is under 10MB
   - Try a different image if classification fails

4. **AI Processing Errors**
   - Check internet connection
   - Verify Azure OpenAI credentials
   - Ensure description is detailed enough

5. **Email Not Sent**
   - Check Gmail configuration in .env file
   - Verify recipient email address
   - Check spam folder for sent emails

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export STREAMLIT_LOG_LEVEL=debug
streamlit run main_app.py
```

## 📊 Performance Metrics

- **Image Processing**: ~1-3 seconds (AI model)
- **Text Processing**: ~2-5 seconds (depending on description length)
- **Email Delivery**: ~1-3 seconds
- **Total Processing Time**: ~4-11 seconds
- **AI Model Size**: ~100MB (downloaded once)

## 🤝 Contributing

This project is designed for evaluation purposes. For future development:

1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Submit a pull request

## 📄 License

This project is created for evaluation purposes as part of the Orion360 technical assessment.

## 📞 Support

For technical support or questions:
- **Email**: msamy@orion360.com
- **Repository**: Private GitHub repository shared with msamy@orion360.com

## 🙏 Acknowledgments

- **Azure OpenAI** for providing GPT-4o mini access
- **Microsoft ResNet-50** for image classification
- **Hugging Face** for the transformers library
- **Streamlit** for the excellent web framework
- **Orion360** for the technical assessment opportunity

---

**Built with ❤️ using Python, Streamlit, Azure OpenAI, and Microsoft ResNet-50**
