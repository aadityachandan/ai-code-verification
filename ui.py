import streamlit as st
from app import analyze_code
from repair.ai_repair import AIRepair

# 🔥 PAGE CONFIG (FULL WIDTH)
st.set_page_config(
    page_title="AI Code Repair",
    page_icon="🔍",
    layout="wide"
)
st.markdown("""
<style>

/* ❌ REMOVE STREAMLIT HEADER */
header {visibility: hidden;}

/* ❌ REMOVE HAMBURGER MENU */
#MainMenu {visibility: hidden;}

/* ❌ REMOVE FOOTER */
footer {visibility: hidden;}

/* OPTIONAL: REMOVE DEPLOY BUTTON SPACE */
[data-testid="stToolbar"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# 🔥 PREMIUM DARK UI CSS
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
}

/* ===== FULL WIDTH ===== */
.block-container {
    max-width: 100% !important;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* ===== TITLE ===== */
h1 {
    text-align: center;
    color: #60a5fa;
}

/* ===== SUBTITLE ===== */
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 25px;
    font-size: 18px;
}

/* ===== INPUT BOX ===== */
textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
    box-shadow: 0 0 10px rgba(59,130,246,0.1);
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 12px rgba(99,102,241,0.5);
}

/* ===== SECTION SPACING ===== */
section {
    margin-bottom: 25px;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background-color: #020617;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #1e293b;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}

/* ===== CODE BLOCK ===== */
pre {
    background-color: #020617 !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b;
    box-shadow: inset 0 0 8px rgba(0,0,0,0.5);
}

/* ===== DIVIDER ===== */
hr {
    border: 1px solid #1e293b;
}

/* ===== ALERT COLORS ===== */
.stAlert-success {
    background-color: #022c22;
}

.stAlert-error {
    background-color: #2c0202;
}

.stAlert-warning {
    background-color: #2c1e02;
}

</style>
""", unsafe_allow_html=True)

# 🔥 HEADER
st.title("🔍 AI Code Verification & Repair")
st.markdown('<div class="subtitle">Detect • Fix • Secure AI-generated code</div>', unsafe_allow_html=True)

st.divider()

# 🔥 SMALL UX IMPROVEMENT
st.info("💡 Paste Python code and click Analyze to detect bugs and vulnerabilities")

# 🔥 INPUT
st.subheader("📝 Input Code")

code = st.text_area("Paste your Python code here", height=300)

run = st.button("🚀 Analyze Code")

# 🔥 ANALYSIS
if run and code.strip():

    with st.spinner("Analyzing code... 🔍"):
        data = analyze_code(code)

    if "error" in data:
        st.error(data["error"])
    else:
        st.divider()

        # 🚨 ISSUES
        st.subheader("🚨 Issues Detected")

        for issue in data["issues"]:
            sev = issue["severity"]

            if sev == "HIGH":
                st.error(f"{issue['issue']['type']} → {issue['issue']['message']}")
            elif sev == "MEDIUM":
                st.warning(f"{issue['issue']['type']} → {issue['issue']['message']}")
            else:
                st.info(f"{issue['issue']['type']} → {issue['issue']['message']}")

            st.write("🔧 Fix:", issue["fix"])
            st.write("📊 Confidence:", issue.get("confidence", "N/A"), "%")

            # 🤖 OPTIONAL AI FIX
            try:
                ai = AIRepair()
                ai_suggestion = ai.generate_fix(code, issue)

                if ai_suggestion:
                    st.success("🤖 AI Suggestion:")
                    st.write(ai_suggestion)
                else:
                    st.info("AI suggestion not available")

            except:
                st.info("AI suggestion not available")

            st.write("---")

        # 🔧 FIXED CODE
        st.subheader("🔧 Fixed Code")
        st.code(data["fixed_code"], language="python")

        # 📊 SCORE
        st.subheader("📊 Score Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Original Score", data["original_score"])
        col2.metric("Fixed Score", data["fixed_score"])
        col3.metric("Improvement", data["fixed_score"] - data["original_score"])

        # ✅ VALIDATION
        st.subheader("✅ Verification")
        st.success(data["syntax_check"])
        st.info(data["validation"])