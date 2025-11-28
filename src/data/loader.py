import pandas as pd
import json
from typing import Union

def load_data(file_path: str, file_type: str) -> pd.DataFrame:
    """Load CSV or JSON file into pandas DataFrame."""
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type == 'json':
            with open(file_path, 'r') as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return df
    except Exception as e:
        raise Exception(f"Error loading file: {str(e)}")

