import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Any

def should_visualize(result: Any) -> bool:
    """Determine if result should be visualized."""
    if result is None:
        return False
    if isinstance(result, pd.DataFrame):
        return len(result) > 0 and len(result.columns) > 0
    if isinstance(result, (int, float)):
        return False
    return True

def create_chart(result: Any, chart_type: str = 'auto') -> go.Figure:
    """Create appropriate chart based on result."""
    if isinstance(result, pd.DataFrame):
        if chart_type == 'auto':
            # Auto-detect chart type
            if len(result.columns) == 2:
                # Likely category-value pair
                return px.bar(result, x=result.columns[0], y=result.columns[1])
            elif 'date' in str(result.columns[0]).lower() or 'time' in str(result.columns[0]).lower():
                return px.line(result, x=result.columns[0], y=result.columns[1])
            else:
                return px.bar(result, x=result.columns[0], y=result.columns[1])
        elif chart_type == 'bar':
            return px.bar(result, x=result.columns[0], y=result.columns[1])
        elif chart_type == 'line':
            return px.line(result, x=result.columns[0], y=result.columns[1])
        elif chart_type == 'pie':
            return px.pie(result, names=result.columns[0], values=result.columns[1])
    
    return None

