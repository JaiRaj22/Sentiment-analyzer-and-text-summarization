# NLP Insights Dashboard

A Streamlit-based NLP application that provides:
- **Sentiment Analysis** (using Hugging Face Transformers)
- **Text Summarization** (using Hugging Face Transformers)
- **Named Entity Recognition (NER)** (using spaCy)

## Features
- Upload PDF, DOCX, or TXT files.
- Extract text from web URLs.
- Real-time NLP processing.
- Interactive visualizations.

## Setup

1. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

   *Note: If you encounter `metadata-generation-failed`, please ensure you have the latest version of pip and basic build tools installed.*

2. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```
