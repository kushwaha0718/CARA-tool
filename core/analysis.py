from core.nlp_setup import sia

def detect_risks(clauses):
    return {
        "Penalty / Liquidated Damages": [c for c in clauses if "penalty" in c.lower() or "fine" in c.lower()],
        "Indemnity": [c for c in clauses if "indemnify" in c.lower()],
        "Termination Risk": [c for c in clauses if "terminate" in c.lower()],
        "Arbitration / Jurisdiction": [c for c in clauses if "arbitration" in c.lower() or "jurisdiction" in c.lower()],
        "Auto-Renewal / Lock-in": [c for c in clauses if "renew" in c.lower() or "lock-in" in c.lower()],
        "Non-Compete / IP": [c for c in clauses if "non-compete" in c.lower() or "intellectual property" in c.lower()],
    }

def assign_risk_scores(risks):
    clause_scores = {}
    for category, clauses in risks.items():
        for clause in clauses:
            if "penalty" in category.lower():
                clause_scores[clause] = "High"
            elif "indemnity" in category.lower():
                clause_scores[clause] = "Medium"
            else:
                clause_scores[clause] = "Low"

    if "High" in clause_scores.values():
        return clause_scores, "High"
    if "Medium" in clause_scores.values():
        return clause_scores, "Medium"
    return clause_scores, "Low"

def detect_ambiguities(clauses):
    vague = ["reasonable", "best efforts", "as appropriate", "may", "could"]
    return [c for c in clauses if any(v in c.lower() for v in vague)]

def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    if scores["compound"] >= 0.05:
        return "Positive"
    elif scores["compound"] <= -0.05:
        return "Negative"
    return "Neutral"
