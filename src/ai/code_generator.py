import google.generativeai as genai
from config.settings import GEMINI_API_KEY
from src.ai.prompts import get_code_generation_prompt, get_error_correction_prompt

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use gemini-2.5-flash for fast responses, or gemini-2.5-pro for better quality
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    raise ValueError(f"Failed to configure Gemini API: {str(e)}. Please check your GEMINI_API_KEY in .env file.")

def extract_code_from_response(response: str) -> str:
    """Extract Python code from markdown code blocks."""
    if '```python' in response:
        code = response.split('```python')[1].split('```')[0].strip()
    elif '```' in response:
        code = response.split('```')[1].split('```')[0].strip()
    else:
        code = response.strip()
    return code

def generate_code(user_query: str, data_profile: str) -> str:
    """Generate Python code to answer user query."""
    try:
        prompt = get_code_generation_prompt(user_query, data_profile)
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("Empty response from Gemini API")
        code = extract_code_from_response(response.text)
        return code
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "API_KEY" in error_msg:
            raise ValueError(f"Invalid Gemini API key. Please check your GEMINI_API_KEY in .env file. Error: {error_msg}")
        raise

def correct_code(user_query: str, data_profile: str, error_message: str, failed_code: str) -> str:
    """Generate corrected code after error."""
    try:
        prompt = get_error_correction_prompt(user_query, data_profile, error_message, failed_code)
        response = model.generate_content(prompt)
        if not response or not response.text:
            raise ValueError("Empty response from Gemini API")
        code = extract_code_from_response(response.text)
        return code
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "API_KEY" in error_msg:
            raise ValueError(f"Invalid Gemini API key. Please check your GEMINI_API_KEY in .env file. Error: {error_msg}")
        raise

