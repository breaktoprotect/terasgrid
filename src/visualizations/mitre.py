from collections import Counter
from typing import Any, Sequence
from config import CSV_COLUMN_MAP

MITRE_TACTICS = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact",
]


def split_tactics(value: str) -> list[str]:
    """Split a tactics string into a normalized list of tactics."""
    if not value:
        return []
    for sep in (";", "|"):
        value = value.replace(sep, ",")
    return [p.strip() for p in value.split(",") if p.strip()]


def count_tactics(rows: Sequence[Any]) -> list[int]:
    """Count the occurrences of each MITRE tactic in the given rows."""
    tactics_field = CSV_COLUMN_MAP["mitre_tactic_optional"]
    c = Counter()
    for r in rows:
        for t in split_tactics(r[tactics_field]):
            if t in MITRE_TACTICS:
                c[t] += 1
    return [c.get(t, 0) for t in MITRE_TACTICS]
