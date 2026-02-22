from transformers import pipeline
import spacy
import pandas as pd

class NLPEngine:
    def __init__(self):
        # Load sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

        # Load summarization pipeline
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

        # Load spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback or download if missing (in some environments)
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def analyze_sentiment(self, text):
        # Handle long text by taking first 512 characters or so for a quick sentiment
        # In a real app, we might want to average sentiment over chunks
        truncated_text = text[:512]
        result = self.sentiment_analyzer(truncated_text)[0]
        return result

    def generate_summary(self, text):
        # Summarization also has length limits
        # Simple chunking if needed, but for now let's just take the first 1024 tokens
        input_length = len(text.split())
        if input_length < 50:
            return text # Too short to summarize

        max_len = min(150, int(input_length * 0.5))
        min_len = min(30, int(max_len * 0.5))

        # Truncate text to avoid model errors (approx 1024 tokens)
        truncated_text = text[:2000]
        summary = self.summarizer(truncated_text, max_length=max_len, min_length=min_len, do_sample=False)[0]
        return summary['summary_text']

    def perform_ner(self, text):
        doc = self.nlp(text[:1000000]) # spaCy limit
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        df = pd.DataFrame(entities, columns=['Entity', 'Label'])
        return df
