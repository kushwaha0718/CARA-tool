import re
from core.nlp_setup import nlp

def extract_entities(text):
    entities = {
        "Parties": [],
        "Dates": [],
        "Amounts": [],
        "Jurisdiction": []
    }

    # 1. Try spaCy NER (local)
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
        pass  # fallback will handle

    # 2. FALLBACK HEURISTICS (Cloud)

    # Dates
    if not entities["Dates"]:
        entities["Dates"] = re.findall(
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b|\b\d+\s+(days?|months?|years?)\b',
            text,
            re.IGNORECASE
        )

    # Amounts (₹, $, INR)
    if not entities["Amounts"]:
        entities["Amounts"] = re.findall(
            r'(₹\s?\d+(?:,\d+)*(?:\.\d+)?|\$\s?\d+(?:,\d+)*(?:\.\d+)?|\bINR\s?\d+(?:,\d+)*)',
            text,
            re.IGNORECASE
        )

    # Jurisdiction
    if not entities["Jurisdiction"]:
        entities["Jurisdiction"] = re.findall(
            r'\b(India|Hyderabad|Bangalore|Delhi|Mumbai|Chennai|Telangana|Karnataka|Andhra Pradesh)\b',
            text,
            re.IGNORECASE
        )

    # Parties (basic heuristic)
    if not entities["Parties"]:
        entities["Parties"] = re.findall(
            r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\s+(?:Ltd|Limited|LLP|Inc|Private Limited|Pvt\. Ltd\.)\b',
            text
        )

    # Deduplicate + clean
    for k in entities:
        entities[k] = sorted(set(e.strip() for e in entities[k]))

    return entities
