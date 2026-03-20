import sys
import os

from analyzer.parser import parse_code
from detectors.bug_detector import BugDetector
from detectors.security_detector import SecurityDetector
from repair.repair_generator import RepairGenerator
from verifier.patch_verifier import PatchVerifier
from repair.ai_repair import AIRepair




# 🔷 Analyze single code block
def analyze_code(code):
    # Step 1: Parse code
    tree = parse_code(code)

    if tree is None:
        return {"error": "Syntax Error in code"}

    # Step 2: Bug detection
    bug_detector = BugDetector()
    bug_detector.visit(tree)

    # Step 3: Security detection
    security_detector = SecurityDetector()
    security_detector.visit(tree)

    # Combine issues
    all_issues = bug_detector.bugs + security_detector.issues

    # Step 4: Repair generator
    repair = RepairGenerator()

    # Step 5: Verifier
    verifier = PatchVerifier()
    #step 6: ai responserrrr
    ai_repair = AIRepair()

    results = []
    original_results = []
    fixed_code = code

    # 🔴 Process issues
    for issue in all_issues:
        fix_data = repair.generate_fix(issue)
        ai_suggestion = ai_repair.generate_fix(code, issue)

        # Store original issues (for score BEFORE fix)
        original_results.append({
            "issue": issue,
            "severity": fix_data["severity"]
        })

        # Store issue + fix (for display)
        results.append({
        "issue": issue,
        "fix": fix_data["fix"],
         "severity": fix_data["severity"],
         "confidence": fix_data["confidence"],
         "ai_suggestion": ai_suggestion
          
})

        # Apply fix cumulatively
        fixed_code = repair.apply_fix(fixed_code, issue)

    # 🔴 Verify AFTER all fixes
    syntax_ok, syntax_msg = verifier.verify_syntax(fixed_code)
    validation_ok, validation_msg = verifier.basic_validation(fixed_code)

    # 🔴 IMPORTANT: Re-analyze FIXED CODE (THIS FIXES YOUR BUG)
    fixed_tree = parse_code(fixed_code)

    fixed_results = []

    if fixed_tree:
        bug_detector_fixed = BugDetector()
        bug_detector_fixed.visit(fixed_tree)

        security_detector_fixed = SecurityDetector()
        security_detector_fixed.visit(fixed_tree)

        fixed_issues = bug_detector_fixed.bugs + security_detector_fixed.issues

        for issue in fixed_issues:
            fix_data = repair.generate_fix(issue)
            fixed_results.append({
                "issue": issue,
                "severity": fix_data["severity"],
                
            })

    # 🔴 Calculate scores
    original_score = calculate_score(original_results)
    fixed_score = calculate_score(fixed_results)

    # 🔴 Final return
    return {
        "issues": results,
        "fixed_code": fixed_code,
        "syntax_check": syntax_msg,
        "validation": validation_msg,
        "original_score": original_score,
        "fixed_score": fixed_score
    }


# 🔷 Scan entire folder
def scan_folder(folder_path):
    results = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    code = f.read()

                file_results = analyze_code(code)

                results.append((file_path, file_results))

    return results


# 🔷 Read file
def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


# 🔷 Score calculation
def calculate_score(results):
    score = 10

    for r in results:
        if "severity" not in r:
            continue

        if r["severity"] == "HIGH":
            score -= 3
        elif r["severity"] == "MEDIUM":
            score -= 2
        elif r["severity"] == "LOW":
            score -= 1

    return max(score, 0)


# 🔷 MAIN ENTRY
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python app.py <file.py or folder>")
        exit()

    path = sys.argv[1]

    # 🔥 FILE MODE
    if os.path.isfile(path):
        code = read_file(path)
        data = analyze_code(code)

        if "error" in data:
            print("Error:", data["error"])
            exit()

        print(f"\n🔍 Scanning File: {path}\n")

        # 🔴 Issues
        print("🚨 Issues Detected:\n")
        for r in data["issues"]:
            print("Issue:", r["issue"])
            print("Severity:", r["severity"])
            print("Fix:", r["fix"])
            print("Confidence:", str(r["confidence"]) + "%")   # 🔥 ADD THIS
            print("AI Suggestion:", r["ai_suggestion"])
            print("-" * 50)

        # 🔧 Fixed Code
        print("\n🔧 Final Fixed Code Preview:")
        print(data["fixed_code"][:200])
        print("-" * 50)

        # ✅ Verification
        print("Syntax Check:", data["syntax_check"])
        print("Validation:", data["validation"])

        # 📊 Scores
        print("\n📊 Score Comparison:")
        print(f"Original Score: {data['original_score']}/10")
        print(f"Fixed Score: {data['fixed_score']}/10")
        print(f"Improvement: +{data['fixed_score'] - data['original_score']} 🔥\n")

    # 🔥 FOLDER MODE
    elif os.path.isdir(path):
        print(f"\n📂 Scanning Folder: {path}\n")

        folder_results = scan_folder(path)

        for file_path, data in folder_results:
            print(f"\n📄 File: {file_path}\n")

            if "error" in data:
                print("Error:", data["error"])
                continue

            # 🔴 Issues
            for r in data["issues"]:
                print("Issue:", r["issue"])
                print("Severity:", r["severity"])
                print("Fix:", r["fix"])
                print("Confidence:", str(r["confidence"]) + "%")   # 🔥 ADD THIS
                print("AI Suggestion:", r["ai_suggestion"])
                print("-" * 50)

            # 🔧 Fixed Code
            print("\n🔧 Fixed Code Preview:")
            print(data["fixed_code"][:200])

            # ✅ Verification
            print("Syntax Check:", data["syntax_check"])
            print("Validation:", data["validation"])

            # 📊 Scores
            print(f"\nOriginal Score: {data['original_score']}/10")
            print(f"Fixed Score: {data['fixed_score']}/10")
            print(f"Improvement: +{data['fixed_score'] - data['original_score']} 🔥\n")

    else:
        print("Invalid path!")