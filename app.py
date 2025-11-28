import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data.loader import load_data
from src.data.profiler import generate_profile, format_profile_for_prompt
from src.ai.agent import process_query
from src.visualization.chart_generator import should_visualize, create_chart
import tempfile
import os
import json

# Page configuration
st.set_page_config(
    page_title="InsightSpark - Autonomous Insight Agent",
    page_icon="✨",
    layout="wide"
)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data_profile_str' not in st.session_state:
    st.session_state.data_profile_str = ""
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'last_narrated' not in st.session_state:
    st.session_state.last_narrated = None

# Header
st.title("✨ InsightSpark - Autonomous Insight Agent")
st.markdown("**Your AI-powered data analyst. Upload data, ask questions, get insights.**")

# Sidebar for file upload
with st.sidebar:
    st.header("📊 Data Upload")
    
    from config.settings import MAX_FILE_SIZE_MB
    uploaded_file = st.file_uploader(
        "Upload CSV or JSON file",
        type=['csv', 'json'],
        help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
    )
    
    st.divider()
    st.header("🔊 Voice Settings")
    voice_enabled = st.toggle(
        "Enable Voice Narration",
        value=st.session_state.voice_enabled,
        help="Narrate insights using Gemini-generated voice-optimized narratives"
    )
    st.session_state.voice_enabled = voice_enabled
    
    if voice_enabled:
        st.caption("💡 Insights will be narrated with Gemini-optimized voice narratives")
        st.caption("🎙️ Powered by Gemini AI + Browser TTS")
    
    if uploaded_file is not None:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            st.error(f"File size ({file_size_mb:.2f}MB) exceeds maximum ({MAX_FILE_SIZE_MB}MB)")
        else:
            # Save uploaded file temporarily
            file_ext = uploaded_file.name.split('.')[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Load data
                df = load_data(tmp_path, file_ext)
                st.session_state.df = df
                
                # Generate profile
                profile = generate_profile(df)
                st.session_state.profile = profile
                st.session_state.data_profile_str = format_profile_for_prompt(profile)
                
                st.success(f"✅ Data loaded successfully! ({len(df)} rows, {len(df.columns)} columns)")
                
                # Display profile
                st.subheader("📋 Data Profile")
                st.write(f"**Rows:** {profile['row_count']}")
                st.write(f"**Columns:** {profile['column_count']}")
                
                st.write("**Column Types:**")
                for col, dtype in profile['dtypes'].items():
                    st.write(f"- {col}: `{dtype}`")
                
                st.write("**First 5 Rows:**")
                st.dataframe(df.head(5), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
            finally:
                # Clean up temp file
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

# Main chat interface
if st.session_state.df is not None:
    st.header("💬 Ask Questions About Your Data")
    
    # Voice narration component (JavaScript)
    if st.session_state.voice_enabled and st.session_state.last_narrated:
        narration_text = st.session_state.last_narrated
        # Reset after use
        st.session_state.last_narrated = None
        
        # Escape text for JavaScript
        narration_js = json.dumps(narration_text)
        
        # Inject JavaScript for text-to-speech
        st.components.v1.html(f"""
        <script>
            (function() {{
                if ('speechSynthesis' in window) {{
                    // Wait for voices to load
                    const speakText = () => {{
                        const utterance = new SpeechSynthesisUtterance();
                        utterance.text = {narration_js};
                        utterance.rate = 0.9;
                        utterance.pitch = 1.0;
                        utterance.volume = 1.0;
                        
                        // Try to use a natural-sounding voice
                        const voices = speechSynthesis.getVoices();
                        const preferredVoice = voices.find(voice => 
                            voice.lang.includes('en') && 
                            (voice.name.includes('Natural') || voice.name.includes('Neural') || voice.name.includes('Premium'))
                        ) || voices.find(voice => voice.lang.includes('en-US')) || voices.find(voice => voice.lang.includes('en')) || voices[0];
                        
                        if (preferredVoice) {{
                            utterance.voice = preferredVoice;
                        }}
                        
                        speechSynthesis.speak(utterance);
                    }};
                    
                    // Load voices if not already loaded
                    if (speechSynthesis.getVoices().length === 0) {{
                        speechSynthesis.onvoiceschanged = speakText;
                    }} else {{
                        speakText();
                    }}
                }}
            }})();
        </script>
        """, height=0)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            if "code" in message:
                with st.expander("🔍 View Generated Code"):
                    st.code(message["code"], language="python")
            
            if "fig" in message and message["fig"] is not None:
                st.plotly_chart(message["fig"], use_container_width=True)
    
    # Query input
    user_query = st.chat_input("Ask a question about your data...")
    
    if user_query:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Process query
        with st.spinner("🤔 Analyzing your data..."):
            try:
                response = process_query(
                    user_query,
                    st.session_state.df,
                    st.session_state.data_profile_str
                )
                
                # Display assistant response
                assistant_message = {"role": "assistant", "content": ""}
                
                if response.get('error'):
                    assistant_message["content"] = f"❌ Error: {response['error']}"
                    if response.get('was_retried'):
                        assistant_message["content"] += "\n\n🔄 Attempted automatic correction."
                else:
                    # Show result
                    if response.get('result') is not None:
                        if isinstance(response['result'], pd.DataFrame):
                            assistant_message["content"] = "📊 **Result:**"
                            st.dataframe(response['result'], use_container_width=True)
                        else:
                            assistant_message["content"] = f"📊 **Result:** {response['result']}"
                    
                    # Show visualization if available
                    if response.get('fig') is not None:
                        assistant_message["fig"] = response['fig']
                    elif should_visualize(response.get('result')):
                        # Auto-generate chart
                        chart = create_chart(response.get('result'))
                        if chart:
                            assistant_message["fig"] = chart
                    
                    # Show summary
                    if response.get('summary'):
                        assistant_message["content"] += f"\n\n💡 **Insight:** {response['summary']}"
                        # Store voice narrative for narration (prefer voice-optimized, fallback to summary)
                        assistant_message["summary_text"] = response.get('voice_narrative', response.get('summary', ''))
                
                # Add code to message
                assistant_message["code"] = response.get('code', '')
                
                st.session_state.chat_history.append(assistant_message)
                
                # Trigger voice narration if enabled
                if st.session_state.voice_enabled and response.get('summary'):
                    st.session_state.last_narrated = response['summary']
                
                # Rerun to show new message
                st.rerun()
                
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
else:
    st.info("👆 Please upload a CSV or JSON file to get started!")

# Footer
st.markdown("---")
st.markdown("**InsightSpark MVP** - Built with Streamlit & Google Gemini API")

