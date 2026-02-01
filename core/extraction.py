import fitz
from docx import Document
from io import BytesIO
from nltk.tokenize import sent_tokenize
from core.nlp_setup import nlp

def extract_text(file, file_type):
    try:
        if file_type == "pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")
            return "\n".join(page.get_text() for page in doc)
        if file_type == "docx":
            doc = Document(BytesIO(file.read()))
            return "\n".join(p.text for p in doc.paragraphs)
        if file_type == "txt":
            return file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""
    return ""

def classify_contract(text):
    t = text.lower()
    if "employment" in t:
        return "Employment Agreement"
    if "vendor" in t or "supplier" in t:
        return "Vendor Contract"
    if "lease" in t or "rent" in t:
        return "Lease Agreement"
    if "partnership" in t:
        return "Partnership Deed"
    if "service" in t:
        return "Service Contract"
    return "General Contract"

def extract_clauses(text):
    return [s.strip() for s in sent_tokenize(text) if len(s.strip()) > 15]

def extract_entities(text):
    doc = nlp(text)
    return {
        "Parties": list(set(ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG"])),
        "Dates": list(set(ent.text for ent in doc.ents if ent.label_ == "DATE")),
        "Amounts": list(set(ent.text for ent in doc.ents if ent.label_ == "MONEY")),
        "Jurisdiction": list(set(ent.text for ent in doc.ents if ent.label_ == "GPE")),
    }
