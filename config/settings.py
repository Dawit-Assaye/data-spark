import os
from dotenv import load_dotenv

load_dotenv()

# Try to import streamlit for secrets (Streamlit Cloud)
try:
    import streamlit as st
    # Streamlit Cloud uses st.secrets
    _streamlit_available = True
except ImportError:
    _streamlit_available = False

# API Configuration
# Priority: Streamlit secrets > Environment variable > .env file
if _streamlit_available:
    try:
        # Try to get API key from Streamlit secrets first, then environment variable
        # This will raise StreamlitSecretNotFoundError if no secrets.toml exists
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    except Exception:
        # If secrets are not available (e.g., in Cloud Run), use environment variable
        # This catches StreamlitSecretNotFoundError, AttributeError, KeyError, etc.
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
else:
    # Not in Streamlit environment, use env vars or .env
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
