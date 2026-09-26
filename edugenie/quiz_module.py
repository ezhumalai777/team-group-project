import os
import re
import json
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def clean_json_block(text: str) -> str:
    """Removes Markdown ```json code fences as specified in EduGenie documentation."""
    return re.sub(r"```(?:json)?\s*(.*?)\s*```", r"\1", text, flags=re.DOTALL).strip()

def generate_quiz(text: str) -> list:
    """
    Quiz Generation Module (Milestone 2, Activity 2.1).
    Generates 3 multiple-choice questions with 4 options each and the correct answer.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return [{
                "question": "Gemini API key is not configured.",
                "options": ["Set GEMINI_API_KEY in .env", "Get free key from Google AI Studio", "Click Key icon in EduGenie header", "All of the above"],
                "answer": "All of the above"
            }]

        prompt = f"""You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""
        quiz_text = generate_with_gemini(prompt, preferred_model="gemini-1.5-pro")
        
        # Clean markdown code blocks if any
        cleaned_text = clean_json_block(quiz_text)

        # Parse JSON
        try:
            quiz_data = json.loads(cleaned_text)
            if isinstance(quiz_data, list):
                return quiz_data
            elif isinstance(quiz_data, dict) and "quiz" in quiz_data:
                return quiz_data["quiz"]
        except json.JSONDecodeError:
            match = re.search(r"\[\s*\{.*\}\s*\]", cleaned_text, re.DOTALL)
            if match:
                return json.loads(match.group(0))

        return [{"error": "Failed to parse quiz response into JSON format", "raw": quiz_text}]
    except Exception as e:
        return [{"error": f"Error in Quiz generation: {str(e)}"}]
