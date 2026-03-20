# # utils/scorer.py

# BASE_CONFIDENCE = {
#     "EvalTainted": 90,
#     "EvalUsage": 50,
#     "ExecTainted": 90,
#     "ExecUsage": 50,
#     "CommandInjection": 85,
#     "SQLInjection": 75,
#     "PathTraversal": 70
# }

# SEVERITY_WEIGHTS = {
#     "CRITICAL": 40,
#     "HIGH": 30,
#     "MEDIUM": 20,
#     "LOW": 10
# }


# # -------------------------
# # 🔥 CONFIDENCE FUNCTION
# # -------------------------
# def compute_confidence(issue_type, depth=1):

#     base = BASE_CONFIDENCE.get(issue_type, 50)

#     # depth boost
#     confidence = base + depth * 3

#     # small penalty for weak cases
#     if issue_type == "EvalUsage":
#         confidence -= 10

#     # clamp
#     confidence = max(0, min(100, confidence))

#     return confidence


# # -------------------------
# # 🔥 FINAL SCORE FUNCTION
# # -------------------------
# def calculate_score(issues):

#     if not issues:
#         return 100

#     total_penalty = 0

#     for issue in issues:
#         severity = issue.get("severity", "MEDIUM")
#         confidence = issue.get("confidence", 50)

#         base_weight = SEVERITY_WEIGHTS.get(severity, 20)

#         # weighted penalty
#         penalty = base_weight * (confidence / 100)

#         total_penalty += penalty

#     final_score = 100 - total_penalty

#     final_score = max(0, min(100, final_score))

#     return round(final_score, 2)