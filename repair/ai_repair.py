from google import genai
from dotenv import load_dotenv
import os

load_dotenv()   # 🔥 THIS IS REQUIRED

class AIRepair:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:
            return f"AI suggestion unavailable ({str(e)})"