from google import genai
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# 🔑 Get API key (works locally + cloud)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]


class AIRepair:

    def __init__(self):
        self.client = genai.Client(api_key=api_key)   # ✅ FIXED

    def generate_fix(self, code, issue):
        try:
            prompt = f"""
You are a secure Python code repair assistant.

Fix the issue in the code.

Code:
{code}

Issue:
{issue}

Return:
1. Fixed code
2. Short explanation
"""

            response = self.client.models.generate_content(
                model="gemma-3-4b-it",
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"AI suggestion unavailable ({str(e)})"