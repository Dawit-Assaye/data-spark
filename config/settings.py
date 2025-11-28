import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
# Try to get from environment variable (Cloud Run) or .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Validate API key (only in local development, Cloud Run will have it as env var)
if not GEMINI_API_KEY:
    # Don't raise error immediately - allow app to start and show error in UI
    import warnings
    warnings.warn("GEMINI_API_KEY not found. Please set it in .env file or as Cloud Run environment variable.")
elif len(GEMINI_API_KEY) < 20:  # Basic validation - API keys are typically longer
    import warnings
    warnings.warn("GEMINI_API_KEY appears to be invalid. Please check your configuration.")

# File Upload Configuration
MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = ['.csv', '.json']

# Execution Configuration
ALLOWED_LIBRARIES = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly']
MAX_RETRY_ATTEMPTS = 1

# UI Configuration
CHART_TYPES = ['bar', 'line', 'pie']

