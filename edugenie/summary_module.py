import os
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def summarize_text(text: str) -> str:
    """
    Summarization Module (Milestone 2, Activity 2.1).
    Summarizes long educational passages into concise, easy-to-understand versions.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key not set. Please set GEMINI_API_KEY in your .env file or via the Key icon."

        prompt = f"Summarize the following text in simple language:\n\n{text}"
        summary = generate_with_gemini(prompt, preferred_model="gemini-1.5-pro")
        return summary
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"
