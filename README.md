# 🚗 Car Selling Platform

AI-powered platform for listing cars with **image classification**, **NLP description parsing**, and **automated email delivery**.

## ✨ Features
- 🖼️ AI car type detection (Microsoft ResNet-50)
- 🧠 GPT-based description-to-JSON extraction
- 📧 Automated email with images + structured data
- 🔒 Prompt injection prevention & input validation
- 🎨 Modern Streamlit UI
- **🎨 Modern UI**: Beautiful Streamlit interface with responsive design
- **⚙️ Environment-based Configuration**: Secure setup through .env file
- **📊 Structured Output**: Generates clean JSON format matching your specifications
- **🤖 Free AI Model**: No API costs for image classification
- **📁 Organized Structure**: Professional folder organization for maintainability

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

### 5️⃣ Run the application
   ```bash
   # Option 1: Use the launcher script (recommended)
   python run_app.py
   
   # Option 2: Direct Streamlit command
   streamlit run src/main_app.py
   ```
Then open **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
car-selling-platform/
├── 📁 src/                    # Source code
│   ├── 📁 core/              # Core application logic
│   │   ├── __init__.py
│   │   ├── image_classifier.py      # AI-powered car type detection (ResNet-50)
│   │   ├── text_processor.py        # AI text processing with GPT-4o mini
│   │   └── email_sender.py          # Email delivery system
│   ├── 📁 config/            # Configuration
│   │   ├── __init__.py
│   │   └── config.py                # Configuration and credentials
│   ├── __init__.py
│   └── main_app.py                  # Main Streamlit application
├── 📁 docs/                   # Documentation
│   ├── __init__.py
│   ├── user_manual.md              # Detailed user instructions
│   ├── solution_design.md          # Architecture and design documentation
│   └── solution_creation_prompt.md # LLM prompt for solution creation
├── 📁 scripts/                # Utility scripts
│   ├── __init__.py
│   └── diagnose_gmail.py           # Gmail authentication diagnostic tool
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from env_example.txt)
├── env_example.txt                 # Environment variables template
├── .gitignore                      # Git ignore patterns
├── run_app.py                      # Application launcher script
├── README.md                       # This file
└── user_manual.md                  # User instructions (moved to docs/)
```