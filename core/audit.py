import json
import os
from datetime import datetime

def log_audit(action, detail):
    with open("audit_log.json", "a", encoding="utf-8") as f:
        json.dump({
            "time": datetime.now().isoformat(),
            "action": action,
            "detail": detail
        }, f)
        f.write("\n")

def load_audit_logs():
    if os.path.exists("audit_log.json"):
        with open("audit_log.json", "r") as f:
            return [json.loads(line) for line in f if line.strip()]
    return []
