import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def review_code(code):

    prompt = f"""
You are an expert Python code reviewer.

Analyze the following Python code and provide:

1. Overall Code Quality Score (out of 10)
2. Bugs (if any)
3. Suggestions for Improvement
4. Best Practices
5. Time Complexity (if applicable)

Python Code:

{code}
"""

    response = model.generate_content(prompt)

    return response.text