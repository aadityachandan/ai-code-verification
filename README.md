    # 🚀 AI Code Verification & Automated Repair System
    
    <p align="center">
      <b>🔍 Detect • 🧠 Analyze • 🛠️ Repair • 🛡️ Secure Python Code</b><br>
      <i>AST-based static analysis with taint tracking and intelligent fixing</i>
    </p>
    
    ---
    
    ## 📌 Overview
    
    The **AI Code Verification & Automated Repair System** is a security-focused static analysis tool that detects **bugs, vulnerabilities, and unsafe coding patterns** in Python programs.
    
    Unlike traditional linters, this system performs **taint analysis**, allowing it to track how user input flows through code and identify real-world security threats.
    
    ---
    
    ## 🧠 Key Features
    
    ### 🔍 AST-Based Analysis
    - Uses Python Abstract Syntax Tree (AST)
    - No code execution → **safe by design**
    - Deep structural code understanding
    
    ---
    
    ### 🔥 Taint Analysis (Core Innovation)
    
    Tracks unsafe data flow from **source → propagation → sink**
    
    ```python
    a = input()
    b = a
    c = b
    eval(c)

✔ Identifies `c` as user-controlled<br>✔ Flags `eval(c)` as **critical vulnerability**
 
---
 

### 🛡️ Security Detection
 
🔴 Critical Vulnerabilities
 

*   `eval(user_input)`
     
*   `exec(user_input)`
     
*   `os.system(user_input)` → Command Injection
     
*   SQL Injection
     
*   Path Traversal
     
*   `pickle.loads(user_input)`
     

🟡 Risky Patterns
 

*   `eval(variable)`
     
*   Dynamic file paths
     
*   SQL query concatenation
     

---
 

### 🐞 Bug Detection
 

*   Division by zero
     
*   Infinite loops
     
*   Index out-of-bounds
     
*   Empty `except` blocks
     
*   Overly broad exception handling
     

---
 

### 🛠️ Automated Code Repair
 
❌ Vulnerable Code
 

    user_input = input()
    result = eval(user_input)

✅ Safe Fix
 

    import ast
    
    user_input = input()
    result = ast.literal_eval(user_input)

✔ Eliminates code execution risk<br>✔ Preserves functionality
 
---
 

### 📊 Risk Scoring System
 
Each issue is evaluated based on:
 

*   Severity
     
*   Confidence
     
*   Taint involvement
     

Example:
 

    Original Score: 12.53
    Fixed Score:    51.05
    Improvement:    +38.52

---
 

## 🎨 User Interface
 
Built using **Streamlit**
 

*   Interactive code editor
     
*   Real-time vulnerability detection
     
*   Fix suggestion panel
     
*   Risk score visualization
     
*   Clean dark-themed UI
     

---
 

## 🧱 Project Structure
 

    ai-code-verification-system/
    │
    ├── app.py                 # Core analyzer logic
    ├── ui.py                  # Streamlit UI
    │
    ├── detectors/             # Security + bug detection
    ├── repair/                # Fix generation
    ├── verifier/              # Patch validation
    ├── utils/
    │   └── scorer.py          # Risk scoring system
    │
    ├── examples/              # Sample vulnerable code
    ├── tests/                 # Testing scripts
    │
    ├── requirements.txt
    └── README.md

---
 

## ⚙️ Installation
 

    git clone https://github.com/your-username/ai-code-verification-system.git
    cd ai-code-verification-system
    pip install -r requirements.txt

---
 

## ▶️ Run the Application
 

    streamlit run ui.py

---
 

## 🧪 Example
 

    user_input = input()
    os.system(user_input)

👉 Detects **Command Injection**<br>👉 Suggests secure alternative
 
---
 

## 🚧 Upcoming Features
 

*   🔐 User Authentication (Login/Signup)
     
*   📊 User-specific History Tracking
     
*   🗄️ Database Integration (SQLite → PostgreSQL)
     
*   🌐 Deployment-ready backend
     
*   🧩 Multi-language support
     

---
 

## 💡 Why This Project is Unique
 
✔ Goes beyond syntax → understands **data flow**<br>✔ Combines **security analysis + automated repair**<br>✔ Detects real-world vulnerabilities<br>✔ Designed for scalability and future AI integration
 
---
 

## 👨‍💻 Author
 
**Aaditya Chandan**
 
---
 

## ⭐ Support
 
If you like this project:
 

*   ⭐ Star the repository
     
*   🍴 Fork it
     
*   🚀 Share it
     

---
 

## 🔥 Final Note
 
This is not just a bug detector.
 
👉 It is a **security-aware code intelligence system**.