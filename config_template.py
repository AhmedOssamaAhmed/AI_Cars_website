# Copy this file to config.py and update with your actual credentials
# This template shows the required configuration structure

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "your_azure_openai_api_key_here")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://your-endpoint.openai.azure.com")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "your_deployment_name")

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER", "your_gmail_address@gmail.com")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "your_gmail_app_password")

# Application Settings
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp']
