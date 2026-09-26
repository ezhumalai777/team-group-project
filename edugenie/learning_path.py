import os
import traceback
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def get_learning_recommendations(topic: str) -> str:
    """
    Learning Path Module (Milestone 2, Activity 2.1).
    Generates personalized learning path with beginner to advanced concepts,
    timelines, topics, and curated resources.
    """
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, books).
Include beginner, intermediate, and advanced levels if needed.
"""
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "⚠️ Gemini API key not set. Please configure GEMINI_API_KEY in your .env file or header."

        recommendations = generate_with_gemini(prompt, preferred_model="gemini-1.5-pro")
        print("Gemini response received for topic:", topic)
        return recommendations
    except Exception as e:
        traceback.print_exc()
        return f"❌ Error occurred: {str(e)}"
