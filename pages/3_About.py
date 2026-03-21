import streamlit as st

st.title("ℹ️ About This Project")

# -------------------------
# INTRO
# -------------------------
st.markdown("""
## 🚀 AI Code Verification & Automated Repair System

A system that automatically **analyzes, detects, and fixes issues in Python code**.
""")

st.divider()

# -------------------------
# PROBLEM
# -------------------------
st.subheader("🎯 Problem Statement")

st.markdown("""
Modern AI tools (ChatGPT, Copilot) generate code that:

- May contain bugs ❌  
- May contain security vulnerabilities ❌  
- Is often blindly trusted ❌  

👉 There is no strong system that verifies and fixes such code automatically.
""")

st.divider()

# -------------------------
# SOLUTION
# -------------------------
st.subheader("💡 Solution")

st.markdown("""
This system provides:

- 🔍 Bug Detection  
- 🔐 Security Vulnerability Detection  
- 🔥 Taint Analysis (tracks user input)  
- 🛠️ Automated Fix Suggestions  
- 📊 Risk Scoring System  
""")

st.divider()

# -------------------------
# SECURITY TYPES
# -------------------------
st.subheader("🔐 Security Vulnerabilities Detected")

st.markdown("""
The system detects the following security risks:

- ⚠️ **Eval Injection** (unsafe use of eval with user input)  
- ⚠️ **Exec Injection**  
- ⚠️ **Command Injection** (`os.system`)  
- ⚠️ **SQL Injection** (string concatenation in queries)  
- ⚠️ **Path Traversal** (unsafe file access using user input)  
- ⚠️ **Unsafe Deserialization** (`pickle.loads`)  
- ⚠️ **Hardcoded Secrets** (passwords, API keys)  
- ⚠️ **Broad Exception Handling**  
- ⚠️ **Empty Except Blocks**  
""")

st.divider()

# -------------------------
# PIPELINE
# -------------------------
st.subheader("⚙️ System Pipeline")

st.code("""
User Code
   ↓
AST Parsing
   ↓
Bug Detection
   ↓
Security Analysis (Taint Tracking)
   ↓
Repair Generation
   ↓
Verification
   ↓
Scoring System
""")

st.divider()

# -------------------------
# FEATURES
# -------------------------
st.subheader("📊 Key Features")

st.markdown("""
- Multi-page Streamlit application  
- Real-time code analysis  
- Before vs After scoring  
- Modular architecture  
- Extensible for AI-based repair  
""")

st.divider()

# -------------------------
# TECH STACK
# -------------------------
st.subheader("🧠 Technologies Used")

st.markdown("""
- Python  
- AST (Abstract Syntax Tree)  
- Static Code Analysis  
- Streamlit (UI)  
- SQLite (planned for users/history)  
""")

st.divider()

# -------------------------
# RESEARCH
# -------------------------
st.subheader("🔬 Concept")

st.markdown("""
This project explores the idea of:

> **Verification and Automated Repair of AI-Generated Code**

Goal:
- Improve trust in AI-generated code  
- Combine static analysis with automated fixing  
""")