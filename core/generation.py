from core.nlp_setup import generator

def generate_explanation(clause):
    prompt = f"Explain this contract clause in simple business English:\n{clause}\nExplanation:"
    try:
        out = generator(prompt)[0]["generated_text"]
        return out.split("Explanation:")[-1].strip()
    except Exception:
        return "Explanation not available."

def suggest_alternatives(clause):
    if "penalty" in clause.lower():
        return "Consider negotiating a cap on penalties or ensuring mutual penalties."
    if "indemnify" in clause.lower():
        return "Limit the scope and duration of indemnity obligations."
    return "Clarify the scope, timelines, or limits as needed."
