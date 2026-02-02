import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# NLTK setup
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download("vader_lexicon")
    sia = SentimentIntensityAnalyzer()

# spaCy setup (Streamlit Cloud SAFE)
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        # Fallback: blank English pipeline (NO crash)
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        return nlp

nlp = load_spacy_model()

# Text generation model
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer="distilgpt2",
    max_new_tokens=60
)
