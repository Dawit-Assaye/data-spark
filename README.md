# DataSpark - Autonomous Insight Agent (MVP)

An AI-powered data analyst that automates data analysis through natural language queries, automated code generation, and intelligent visualization.

## Features

- 📊 **Data Ingestion**: Upload CSV/JSON files (up to 20MB)
- 🔍 **Data Profiling**: Automatic schema and statistics generation
- 💬 **Natural Language Queries**: Ask questions in plain English
- 🤖 **Code Generation**: AI generates and executes Python code
- 🔄 **Self-Correction**: Automatic error handling and retry
- 📈 **Auto-Visualization**: Smart chart generation (Bar, Line, Pie)
- 💡 **Narrative Insights**: AI-generated summaries of findings

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your free Gemini API key from [Google AI Studio](https://ai.google.dev)

### 3. Run Application

```bash
streamlit run app.py
```

## Project Structure

```
dataspark/
├── app.py                 # Main Streamlit app
├── config/                # Configuration
├── src/
│   ├── data/             # Data loading & profiling
│   ├── ai/               # AI agent & code generation
│   ├── execution/        # Code execution sandbox
│   └── visualization/    # Chart generation
└── tests/                # Test datasets
```

## Usage

1. Upload a CSV or JSON file via the sidebar
2. Review the automatic data profile
3. Ask questions in natural language
4. View results, visualizations, and insights
5. Explore follow-up suggestions

## Example Queries

- "Show me the sales trend over time"
- "What is the average revenue by category?"
- "Which product has the highest sales?"
- "Compare sales across different regions"

## Technology Stack

- **Frontend/Backend**: Streamlit
- **AI Model**: Google Gemini API
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Cloud**: GCP Always Free Tier

## License

MIT

