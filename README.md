# 🔍 AI Code Verification & Automated Repair System

An intelligent Python-based system that analyzes code for bugs and security vulnerabilities, performs taint analysis, and automatically suggests fixes using AST transformations.

---

## 🚀 Features

### 🧠 Static Code Analysis
- Parses Python code using Abstract Syntax Tree (AST)
- Detects common bugs like:
  - Division by zero
  - Index errors

### 🔐 Security Vulnerability Detection
- Detects dangerous patterns such as:
  - `eval()` / `exec()`
  - `os.system()` usage
  - SQL Injection
  - Path Traversal
  - Unsafe Deserialization

### 🔥 Advanced Taint Analysis
- Tracks user input (`input()`)
- Propagates through variables and expressions
- Handles function-level data flow

### 🔧 Automated Repair System
- Suggests fixes using AST transformations
- Optional AI-based fix suggestions

### 📊 Scoring System (In Progress)
- Evaluates code quality based on severity and confidence

### 💻 Modern UI (Streamlit)
- Full-screen dashboard
- Issue detection with severity levels
- Confidence scoring
- Fixed code output
- Clean dark theme interface

---

## 🛠 Tech Stack

- Python
- AST (Abstract Syntax Tree)
- Streamlit
- Static Analysis Techniques
- Taint Analysis

---

## 🎯 Use Cases

- Secure AI-generated code
- Detect vulnerabilities in scripts
- Learn secure coding practices
- Developer productivity tool

---

## 🚀 Future Improvements

- Scoring and ranking system
- Multi-file analysis
- Report generation (PDF/JSON)
- Code highlighting for vulnerabilities

---

## 📌 Author

Developed as a security-focused AI code analysis tool.