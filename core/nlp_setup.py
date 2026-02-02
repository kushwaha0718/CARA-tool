import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import subprocess
import sys

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

# spaCy setup (Streamlit Cloud safe)
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.check_call(
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"]
        )
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# Text generation model
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer="distilgpt2",
    max_new_tokens=60
)
