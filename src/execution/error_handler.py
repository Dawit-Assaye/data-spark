from typing import Tuple, Dict, Any
from src.execution.executor import execute_code
from src.ai.code_generator import correct_code

def execute_with_retry(code: str, df, user_query: str, data_profile: str) -> Tuple[Dict[str, Any], str, bool]:
    """
    Execute code with automatic retry on error.
    
    Returns:
        Tuple of (result_dict, error_message, was_retried)
    """
    result_dict, error_message = execute_code(code, df)
    
    if error_message:
        # Retry once with error feedback
        corrected_code = correct_code(user_query, data_profile, error_message, code)
        result_dict, error_message = execute_code(corrected_code, df)
        return result_dict, error_message, True
    
    return result_dict, error_message, False

