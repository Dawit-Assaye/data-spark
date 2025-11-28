import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add your Gemini API key.")
if len(GEMINI_API_KEY) < 20:  # Basic validation - API keys are typically longer
    raise ValueError("GEMINI_API_KEY appears to be invalid. Please check your .env file.")

# File Upload Configuration
MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = ['.csv', '.json']

# Execution Configuration
ALLOWED_LIBRARIES = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly']
MAX_RETRY_ATTEMPTS = 1

# UI Configuration
CHART_TYPES = ['bar', 'line', 'pie']

