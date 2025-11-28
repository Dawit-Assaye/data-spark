import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple
import traceback
import sys
from io import StringIO
from datetime import datetime, timedelta

def execute_code(code: str, df: pd.DataFrame) -> Tuple[Dict[str, Any], str]:
    """
    Execute generated Python code in a sandboxed environment.
    
    Returns:
        Tuple of (result_dict, error_message)
        result_dict contains: 'result', 'fig', 'output'
    """
    # Create a safe execution namespace
    # Import builtins but restrict dangerous functions
    import builtins
    safe_builtins = {
        'len': len,
        'str': str,
        'int': int,
        'float': float,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'print': print,
        'range': range,
        'enumerate': enumerate,
        'zip': zip,
        'sorted': sorted,
        'min': min,
        'max': max,
        'sum': sum,
        'abs': abs,
        'round': round,
        'bool': bool,
        'type': type,
        'isinstance': isinstance,
        'hasattr': hasattr,
        'getattr': getattr,
        'setattr': setattr,
    }
    
    # Block import statements by providing a mock __import__
    def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
        raise ImportError(f"Import statements are not allowed. Use pre-imported modules: pd, np, px, go, plt, sns")
    
    namespace = {
        'pd': pd,
        'df': df,
        'go': go,
        'px': px,
        'np': np,
        'plt': plt,
        'sns': sns,
        'datetime': datetime,
        'timedelta': timedelta,
        '__builtins__': safe_builtins,
        '__import__': restricted_import,
    }
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    result_dict = {'result': None, 'fig': None, 'output': ''}
    error_message = None
    
    try:
        # Remove any import statements from code before execution
        lines = code.split('\n')
        filtered_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip import statements
            if stripped.startswith('import ') or stripped.startswith('from '):
                continue
            filtered_lines.append(line)
        
        cleaned_code = '\n'.join(filtered_lines)
        exec(cleaned_code, namespace)
        
        # Capture result
        if 'result' in namespace:
            result_dict['result'] = namespace['result']
        if 'fig' in namespace:
            result_dict['fig'] = namespace['fig']
        
        # Capture output
        result_dict['output'] = captured_output.getvalue()
        
    except Exception as e:
        error_message = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    
    finally:
        sys.stdout = old_stdout
    
    return result_dict, error_message

