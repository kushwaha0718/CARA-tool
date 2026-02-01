import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import os

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

# spaCy setup
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Text generation model
generator = pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer="distilgpt2",
    max_new_tokens=60
)
