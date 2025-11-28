from src.ai.code_generator import generate_code
from src.execution.error_handler import execute_with_retry
from src.ai.prompts import get_summary_prompt, get_followup_prompt
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use gemini-2.5-flash for fast responses, or gemini-2.5-pro for better quality
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    raise ValueError(f"Failed to configure Gemini API: {str(e)}. Please check your GEMINI_API_KEY in .env file.")

def process_query(user_query: str, df, data_profile: str) -> dict:
    """
    Main agent function to process user query.
    
    Returns:
        Dictionary with: code, result, fig, summary, error, was_retried
    """
    # Generate code
    code = generate_code(user_query, data_profile)
    
    # Execute with retry
    result_dict, error_message, was_retried = execute_with_retry(
        code, df, user_query, data_profile
    )
    
    response = {
        'code': code,
        'result': result_dict.get('result'),
        'fig': result_dict.get('fig'),
        'output': result_dict.get('output'),
        'error': error_message,
        'was_retried': was_retried
    }
    
    # Generate summary if successful
    if not error_message and result_dict.get('result') is not None:
        result_description = str(result_dict['result'])
        if hasattr(result_dict['result'], '__len__') and len(result_dict['result']) > 0:
            result_description = f"DataFrame with {len(result_dict['result'])} rows"
        
        try:
            # Generate regular summary for display
            summary_prompt = get_summary_prompt(user_query, result_description)
            summary_response = model.generate_content(summary_prompt)
            if summary_response and summary_response.text:
                response['summary'] = summary_response.text
                
                # Generate voice-optimized narrative using Gemini
                try:
                    from src.ai.prompts import get_voice_narrative_prompt
                    voice_prompt = get_voice_narrative_prompt(user_query, result_description, response['summary'])
                    voice_response = model.generate_content(voice_prompt)
                    if voice_response and voice_response.text:
                        response['voice_narrative'] = voice_response.text.strip()
                except Exception as voice_error:
                    # If voice narrative generation fails, use summary as fallback
                    response['voice_narrative'] = response['summary']
                    
        except Exception as e:
            # If summary generation fails, continue without it
            error_msg = str(e)
            if "API key" in error_msg or "API_KEY" in error_msg:
                response['summary'] = "Summary generation failed: Invalid API key. Please check your .env file."
            else:
                response['summary'] = f"Summary generation failed: {error_msg}"
    
    return response

