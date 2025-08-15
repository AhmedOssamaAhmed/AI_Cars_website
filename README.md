# 🚗 Car Selling Platform

AI-powered platform for listing cars with **image classification**, **NLP description parsing**, and **automated email delivery**.

## ✨ Features
- 🖼️ AI car type detection (Microsoft ResNet-50)
- 🧠 GPT-based description-to-JSON extraction
- 📧 Automated email with images + structured data
- 🔒 Prompt injection prevention & input validation
- 🎨 Modern Streamlit UI

## 🚀 Live Demo
**URL**: http://16.16.129.60:8501

---

## 🛠 Quick Start

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd car-selling-platform
```

### 2️⃣ Create & Activate Virtual Environment
```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure `.env`
Create a `.env` file in the project root (or copy `.env.example` and rename it to `.env`):

```env
# Gmail (requires 2FA and an app password)
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# App Settings
MAX_IMAGE_SIZE=10485760
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,bmp
```

💡 **Tip:** To get a Gmail App Password — Enable 2FA in Gmail → *Google Account → Security → App passwords* → Create password for "Mail" → Use it here.

### 5️⃣ Run the App
```bash
streamlit run main_app.py
```
Then open **http://localhost:8501** in your browser.

---

## 📂 Project Structure
```
car-selling-platform/
├── main_app.py              # Main Streamlit application
├── image_classifier.py      # AI-powered car type detection
├── text_processor.py        # AI text processing
├── email_sender.py          # Email delivery system
├── config.py                # Configuration & constants
├── requirements.txt         # Python dependencies
├── .env.example             # Sample environment variables
└── README.md                # This file
```

---

**Built with ❤️ using Python, Streamlit, Azure OpenAI, and Microsoft ResNet-50**
