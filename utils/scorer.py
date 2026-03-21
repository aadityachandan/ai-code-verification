# utils/scorer.py

# -------------------------
# 🔥 BASE CONFIDENCE (by sink type)
# -------------------------
BASE_CONFIDENCE = {
    # 🔴 Security (taint-based)
    "EvalTainted": 90,
    "ExecTainted": 90,
    "CommandInjection": 85,
    "UnsafeDeserialization": 85,
    "SQLInjection": 75,
    "PathTraversal": 70,

    # ⚠️ Risk (non-tainted)
    "OSCommand": 60,
    "EvalUsage": 50,
    "ExecUsage": 50,
    "SQLInjectionRisk": 60,
    "PathTraversalRisk": 60,
    "UnsafeDeserializationRisk": 60,

    # 🔐 Secrets
    "HardcodedSecret": 80,
    "MongoURI": 85,

    # 🐞 Bugs
    "DivisionByZero": 70,
    "NoneComparison": 50,
    "InfiniteLoop": 65,
    "IndexOutOfBounds": 70,
    "EmptyExcept": 60,
    "BroadException": 60,
}

# -------------------------
# 🔥 SEVERITY WEIGHTS
# -------------------------
SEVERITY_WEIGHTS = {
    "CRITICAL": 15,
    "HIGH": 10,
    "MEDIUM": 6,
    "LOW": 3
}

# -------------------------
# 🔥 CONFIDENCE FUNCTION
# -------------------------
def compute_confidence(issue_type, depth=1):

    base = BASE_CONFIDENCE.get(issue_type, 50)

    # increase with depth
    confidence = base + (depth * 3)

    # clamp between 0–100
    confidence = max(0, min(100, confidence))

    return confidence


# -------------------------
# 🔥 FINAL SCORE FUNCTION
# -------------------------
def calculate_score(issues):

    if not issues:
        return 100

    total_penalty = 0

    for issue in issues:
        severity = issue.get("severity", "MEDIUM")
        confidence = issue.get("confidence", 50)

        base_weight = SEVERITY_WEIGHTS.get(severity, 20)

        # 🔥 FIXED DAMPING
        penalty = base_weight * (confidence / 100) * (1 / (1 + total_penalty / 200))

        total_penalty += penalty

    # cap
    total_penalty = min(total_penalty, 90)

    final_score = 100 - total_penalty
    final_score = max(0, min(100, final_score))

    return round(final_score, 2)