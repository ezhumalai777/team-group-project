import os
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def answer_question_with_gemini(question: str) -> str:
    """
    Q&A Module powered by Google Gemini (Milestone 2, Activity 2.1).
    Answers general knowledge and academic questions concisely and accurately.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key not set. Please set GEMINI_API_KEY in your .env file or click the Key icon in the top right."
        
        answer = generate_with_gemini(question, preferred_model="gemini-1.5-pro")
        return answer
    except Exception as e:
        return f"⚠️ Error in QnA: {e}"
