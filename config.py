import os
from dotenv import load_dotenv

# Load environment variables from a local .env file.
# Note: On cloud platforms (like Render), environment variables are injected 
# directly into the host system. If a .env file doesn't exist in production, 
# load_dotenv() will fail silently, and os.getenv() will fetch directly from the host.
load_dotenv()

class Config:
    """Application configuration loaded from environment variables."""
    # Google Gemini API key
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Secret Key used by Flask for session cookie encryption (defaults to 'secret123')
    SECRET_KEY = os.getenv("SECRET_KEY", "kpsecret8347")
