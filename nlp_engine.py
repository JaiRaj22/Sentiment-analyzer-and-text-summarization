from transformers import pipeline
import spacy
import pandas as pd
import os

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
            # For environments where it might not be linked correctly but is installed
            try:
                import en_core_web_sm
                self.nlp = en_core_web_sm.load()
            except ImportError:
                # Last resort fallback (useful for local but might fail on some cloud platforms)
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")

    def analyze_sentiment(self, text):
        truncated_text = text[:512]
        result = self.sentiment_analyzer(truncated_text)[0]
        return result

    def generate_summary(self, text):
        input_length = len(text.split())
        if input_length < 50:
            return text

        max_len = min(150, int(input_length * 0.5))
        min_len = min(30, int(max_len * 0.5))

        truncated_text = text[:2000]
        summary = self.summarizer(truncated_text, max_length=max_len, min_length=min_len, do_sample=False)[0]
        return summary['summary_text']

    def perform_ner(self, text):
        doc = self.nlp(text[:1000000])
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        df = pd.DataFrame(entities, columns=['Entity', 'Label'])
        return df
