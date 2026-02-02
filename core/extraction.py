import re
import nltk
from nltk.tokenize import sent_tokenize

from core.nlp_setup import nlp

# Ensure NLTK resources exist
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# TEXT EXTRACTION
def extract_text(file, file_type):
    if file_type == "pdf":
        import fitz
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in doc)

    elif file_type == "docx":
        from docx import Document
        document = Document(file)
        return "\n".join(p.text for p in document.paragraphs)

    elif file_type == "txt":
        return file.read().decode("utf-8")

    return ""


# CLAUSE EXTRACTION
def extract_clauses(text):
    try:
        return [
            s.strip()
            for s in sent_tokenize(text)
            if len(s.strip()) > 15
        ]
    except Exception:
        # fallback split
        return [
            s.strip()
            for s in text.split(".")
            if len(s.strip()) > 15
        ]


# ENTITY EXTRACTION
def extract_entities(text):
    entities = {
        "Parties": [],
        "Dates": [],
        "Amounts": [],
        "Jurisdiction": []
    }

    # --- spaCy (local) ---
    try:
        if nlp.has_pipe("ner"):
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ("ORG", "PERSON"):
                    entities["Parties"].append(ent.text)
                elif ent.label_ == "DATE":
                    entities["Dates"].append(ent.text)
                elif ent.label_ in ("GPE", "LOC"):
                    entities["Jurisdiction"].append(ent.text)
                elif ent.label_ == "MONEY":
                    entities["Amounts"].append(ent.text)
    except Exception:
        pass

    # --- Fallback heuristics (cloud) ---
    if not entities["Dates"]:
        entities["Dates"] = re.findall(
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d+\s+(days?|months?|years?)\b',
            text,
            re.IGNORECASE
        )

    if not entities["Amounts"]:
        entities["Amounts"] = re.findall(
            r'(₹\s?\d+(?:,\d+)*|\$\s?\d+(?:,\d+)*|\bINR\s?\d+(?:,\d+)*)',
            text,
            re.IGNORECASE
        )

    if not entities["Jurisdiction"]:
        entities["Jurisdiction"] = re.findall(
            r'\b(India|Hyderabad|Delhi|Mumbai|Bangalore|Chennai|Telangana)\b',
            text,
            re.IGNORECASE
        )

    if not entities["Parties"]:
        entities["Parties"] = re.findall(
            r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Ltd|Limited|LLP|Pvt\. Ltd\.)\b',
            text
        )

    # Clean + deduplicate
    for k in entities:
        entities[k] = sorted(set(e.strip() for e in entities[k]))

    return entities


# CONTRACT CLASSIFICATION
def classify_contract(text):
    t = text.lower()
    if "employment" in t:
        return "Employment Agreement"
    if "service" in t:
        return "Service Contract"
    if "lease" in t:
        return "Lease Agreement"
    return "General Contract"
