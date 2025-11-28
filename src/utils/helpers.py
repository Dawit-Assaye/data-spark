def format_dataframe_for_display(df, max_rows=100):
    """Format dataframe for display, limiting rows."""
    if len(df) > max_rows:
        return df.head(max_rows)
    return df

