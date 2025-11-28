import pandas as pd
from typing import Dict, Any

def generate_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate data profile for display and LLM context."""
    profile = {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'first_5_rows': df.head(5).to_dict('records'),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_summary': df.describe().to_dict() if len(df.select_dtypes(include=['number']).columns) > 0 else {}
    }
    return profile

def format_profile_for_prompt(profile: Dict[str, Any]) -> str:
    """Format profile for LLM prompt."""
    columns_info = "\n".join([f"- {col}: {dtype}" for col, dtype in profile['dtypes'].items()])
    return f"""
DataFrame Information:
- Rows: {profile['row_count']}
- Columns: {profile['column_count']}
- Column Details:
{columns_info}
"""

