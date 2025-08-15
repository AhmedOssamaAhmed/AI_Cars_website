import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://orionopenai2-techtest.openai.azure.com")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini-AO242")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# Gmail Configuration
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECIPIENT_EMAIL = "msamy@orion360.com"  # Default recipient

# Application Settings
MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB default
SUPPORTED_IMAGE_FORMATS = os.getenv("SUPPORTED_IMAGE_FORMATS", "jpg,jpeg,png,bmp").split(',')

# Validation function to check if required credentials are set
def validate_credentials():
    """Validate that required credentials are set."""
    missing_credentials = []
    
    if not AZURE_OPENAI_API_KEY:
        missing_credentials.append("AZURE_OPENAI_API_KEY")
    
    if not GMAIL_USER:
        missing_credentials.append("GMAIL_USER")
    
    if not GMAIL_PASSWORD:
        missing_credentials.append("GMAIL_PASSWORD")
    
    if missing_credentials:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_credentials)}\n"
            "Please create a .env file with your credentials. See env_example.txt for reference."
        )
    
    return True
