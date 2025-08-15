# Configuration Package
from .config import *

__all__ = ['AZURE_OPENAI_API_KEY', 'AZURE_OPENAI_ENDPOINT', 'AZURE_OPENAI_DEPLOYMENT_NAME', 
           'AZURE_OPENAI_API_VERSION', 'GMAIL_USER', 'GMAIL_PASSWORD', 'RECIPIENT_EMAIL',
           'MAX_IMAGE_SIZE', 'SUPPORTED_IMAGE_FORMATS', 'validate_credentials']
