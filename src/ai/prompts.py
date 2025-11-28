def get_code_generation_prompt(user_query: str, data_profile: str) -> str:
    """Generate prompt for code generation."""
    return f"""You are an expert Python Data Analyst.

You have access to a pandas DataFrame variable named `df`.

{data_profile}

User Question: "{user_query}"

Instructions:
1. Write Python code to answer the question using pandas.
2. Assign the final result (text, number, or dataframe) to a variable named `result`.
3. If a visualization is appropriate (time-series, category distribution, comparisons), create a Plotly figure and assign it to `fig`.
4. IMPORTANT: Do NOT use import statements. The following are already available:
   - pandas (as `pd`)
   - numpy (as `np`)
   - plotly.graph_objects (as `go`)
   - plotly.express (as `px`)
   - matplotlib.pyplot (as `plt`)
   - seaborn (as `sns`)
   - datetime (as `datetime`)
   - timedelta (as `timedelta`)
5. Use only the pre-imported libraries listed above.
6. Output ONLY the Python code, wrapped in ```python``` blocks.
7. Do not include explanations or markdown outside code blocks.

Code:"""

def get_error_correction_prompt(user_query: str, data_profile: str, error_message: str, failed_code: str) -> str:
    """Generate prompt for error correction."""
    return f"""You are an expert Python Data Analyst.

You have access to a pandas DataFrame variable named `df`.

{data_profile}

User Question: "{user_query}"

Previous code that failed:
```python
{failed_code}
```

Error message:
{error_message}

Please correct the code and try again. Output ONLY the corrected Python code wrapped in ```python``` blocks."""

def get_summary_prompt(user_query: str, result_description: str) -> str:
    """Generate prompt for narrative summary."""
    return f"""Based on the following analysis:

User Question: "{user_query}"
Result: {result_description}

Generate a 2-sentence executive summary explaining what the data shows. Be specific with numbers and insights."""

def get_voice_narrative_prompt(user_query: str, result_description: str, summary: str) -> str:
    """Generate prompt for voice-optimized narrative."""
    return f"""You are a data analyst presenting insights in a conversational, engaging way for voice narration.

User Question: "{user_query}"
Analysis Result: {result_description}
Summary: {summary}

Generate a natural, conversational narrative (2-3 sentences) that:
1. Is optimized for voice narration - use natural speech patterns
2. Sounds engaging and conversational, like you're explaining to a colleague
3. Includes specific numbers and insights from the data
4. Uses simple, clear language that flows well when spoken
5. Avoids complex jargon or technical terms that are hard to say aloud
6. Has a friendly, professional tone

Write it as if you're speaking directly to the user. Do not include markdown or formatting."""

def get_followup_prompt(data_profile: str, recent_queries: list) -> str:
    """Generate prompt for follow-up suggestions."""
    return f"""Based on the dataset profile and recent queries, suggest 3 relevant follow-up questions a user might ask.

Dataset: {data_profile}
Recent queries: {recent_queries}

Output 3 questions, one per line, without numbering."""

