import streamlit as st
import pandas as pd
from utils import extract_text
from nlp_engine import NLPEngine
import plotly.express as px

# Set page config
st.set_page_config(page_title="NLP Insights Dashboard", layout="wide")

@st.cache_resource
def load_engine():
    return NLPEngine()

engine = load_engine()

st.title("NLP Insights Dashboard")
st.markdown("""
This application performs **Sentiment Analysis**, **Text Summarization**, and **Named Entity Recognition (NER)** on uploaded documents.
""")

# Sidebar for input
st.sidebar.header("Input Source")
uploaded_file = st.sidebar.file_uploader("Upload a file (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

text_input = ""

if uploaded_file:
    with st.spinner("Extracting text..."):
        text_input = extract_text(uploaded_file)

if text_input:
    if text_input.startswith("Error") or text_input == "Unsupported file format":
        st.error(text_input)
    else:
        st.subheader("Input Text Preview")
        st.info(text_input[:1000] + ("..." if len(text_input) > 1000 else ""))

        if st.button("Analyze Text"):
            col1, col2 = st.columns(2)

            with st.spinner("Processing..."):
                # Sentiment Analysis
                sentiment = engine.analyze_sentiment(text_input)

                # Summarization
                summary = engine.generate_summary(text_input)

                # NER
                entities_df = engine.perform_ner(text_input)

            with col1:
                st.subheader("📊 Sentiment Analysis")
                st.metric("Label", sentiment['label'])
                st.metric("Confidence", f"{sentiment['score']:.2f}")

                # Simple visualization for sentiment
                sentiment_data = pd.DataFrame({
                    "Sentiment": [sentiment['label']],
                    "Score": [sentiment['score']]
                })
                fig = px.bar(sentiment_data, x="Sentiment", y="Score", color="Sentiment",
                             color_discrete_map={"POSITIVE": "green", "NEGATIVE": "red"})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📝 Text Summary")
                st.write(summary)

            st.divider()

            st.subheader("🔍 Named Entity Recognition (NER)")
            if not entities_df.empty:
                st.dataframe(entities_df, use_container_width=True)

                # Visualization of entities
                entity_counts = entities_df['Label'].value_counts().reset_index()
                entity_counts.columns = ['Entity Type', 'Count']
                fig_ner = px.pie(entity_counts, values='Count', names='Entity Type', title='Distribution of Entity Types')
                st.plotly_chart(fig_ner, use_container_width=True)
            else:
                st.write("No named entities detected.")
else:
    st.info("Please upload a file to begin analysis.")
