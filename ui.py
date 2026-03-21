import streamlit as st
from app import analyze_code
from repair.ai_repair import AIRepair

# PAGE CONFIG (FULL WIDTH)
st.set_page_config(
    page_title="AI Code Repair",
    layout="wide"
)
st.markdown("""
<style>

/* REMOVE STREAMLIT HEADER */
header {visibility: hidden;}

/* REMOVE HAMBURGER MENU */
#MainMenu {visibility: hidden;}

/* REMOVE FOOTER */
footer {visibility: hidden;}

/* OPTIONAL: REMOVE DEPLOY BUTTON SPACE */
[data-testid="stToolbar"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# PREMIUM DARK UI CSS
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
h1, h1 * {
    font-size: 5rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-top: -1.5rem !important;
    display: block !important;
    padding-bottom: 5px !important;
    background-image: linear-gradient(90deg, #5227FF, #FF9FFC, #B19EEF, #5227FF) !important;
    background-size: 200% auto !important;
    color: transparent !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: gradientFlow 4s linear infinite;
}

@keyframes gradientFlow {
    to {
        background-position: 200% center;
    }
}

/* ===== SUBTITLE ===== */
.subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 25px;
    font-size: 18px;
}

/* ===== INPUT BOX ===== */
div[data-baseweb="textarea"] {
    background-color: #020617 !important;
    border-radius: 12px !important;
    border: 1px solid #1e293b !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5) !important;
    padding: 5px !important;
    transition: all 0.3s ease-in-out !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #22c55e !important;
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.4) !important;
    outline: none !important;
}

div[data-baseweb="textarea"] * {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-baseweb="textarea"] textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    font-family: 'Courier New', monospace !important;
    padding: 10px !important;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #01c1ba, #06d64d);
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
    box-shadow: 0 0 12px rgba(6, 214, 77, 0.5);
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

# HEADER
st.title("AI Code Verification & Repair")
st.markdown('<div class="subtitle">Detect • Fix • Secure AI-generated code</div>', unsafe_allow_html=True)

st.divider()

# SMALL UX IMPROVEMENT
st.info("Paste Python code and click Analyze to detect bugs and vulnerabilities")

# INPUT
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px; border-bottom: 1px solid #1e293b; padding-bottom: 15px;">
    <div style="background: linear-gradient(90deg, #3b82f6, #6366f1); padding: 6px 12px; border-radius: 8px; color: white; font-weight: 800; font-family: 'Courier New', monospace; font-size: 16px; box-shadow: 0 0 12px rgba(99,102,241,0.6);">
        &lt;/&gt;
    </div>
    <h3 style="color: #f8fafc; font-weight: 600; margin: 0; font-size: 22px; letter-spacing: 0.5px;">Input Source Code</h3>
</div>
""", unsafe_allow_html=True)

code = st.text_area("hidden_label", placeholder="Paste your Python code here...", height=320, label_visibility="collapsed")

error_placeholder = st.empty()

run = st.button("Analyze Code")

# ANALYSIS
if run:
    if not code.strip():
        st.markdown("""<style>
        div[data-baseweb="textarea"] {
            border-color: #ef4444 !important;
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.6) !important;
        }
        </style>""", unsafe_allow_html=True)
        error_placeholder.error("Please paste some code before running the analysis.")
        st.stop()

    with st.spinner("Analyzing code..."):
        data = analyze_code(code)

    if "error" in data:
        st.error(data["error"])
    else:
        st.divider()

        # ISSUES
        st.subheader("Issues Detected")

        for issue in data["issues"]:
            sev = issue["severity"]

            if sev == "HIGH":
                st.error(f"{issue['issue']['type']} -> {issue['issue']['message']}")
            elif sev == "MEDIUM":
                st.warning(f"{issue['issue']['type']} -> {issue['issue']['message']}")
            else:
                st.info(f"{issue['issue']['type']} -> {issue['issue']['message']}")

            st.write("Fix:", issue["fix"])
            st.write("Confidence:", issue.get("confidence", "N/A"), "%")

            # OPTIONAL AI FIX
            try:
                ai = AIRepair()
                ai_suggestion = ai.generate_fix(code, issue)

                if ai_suggestion:
                    st.success("AI Suggestion:")
                    st.write(ai_suggestion)
                else:
                    st.info("AI suggestion not available")

            except:
                st.info("AI suggestion not available")

            st.write("---")

        # FIXED CODE
        st.subheader("Fixed Code")
        st.code(data["fixed_code"], language="python")

        # SCORE
        st.subheader("Score Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Original Score", data["original_score"])
        col2.metric("Fixed Score", data["fixed_score"])
        col3.metric("Improvement", data["fixed_score"] - data["original_score"])

        # VALIDATION
        st.subheader("Verification")
        st.success(data["syntax_check"])
        st.info(data["validation"])