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
- 🔊 **Voice Narration**: Gemini-powered voice-optimized narratives

## Quick Start

### Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   Get your free Gemini API key from [Google AI Studio](https://ai.google.dev)

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

### Deploy to Streamlit Cloud (Recommended)

**Easiest deployment option - takes 5 minutes!**

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

See [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) for detailed instructions.

### Deploy to Google Cloud Run

For production deployments on GCP:

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Cloud Run deployment instructions.

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
5. Enable voice narration for audio insights

## Example Queries

- "Show me the sales trend over time"
- "What is the average revenue by category?"
- "Which product has the highest sales?"
- "Compare sales across different regions"

## Technology Stack

- **Frontend/Backend**: Streamlit
- **AI Model**: Google Gemini API (gemini-2.5-flash)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Cloud**: Streamlit Cloud (free) or GCP Cloud Run

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)
- ✅ Free for public apps
- ✅ Automatic deployments
- ✅ 5-minute setup
- 📖 See [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)

### Option 2: Google Cloud Run
- ✅ Always Free Tier available
- ✅ More control
- ✅ Private deployments
- 📖 See [DEPLOYMENT.md](DEPLOYMENT.md)

## License

MIT
