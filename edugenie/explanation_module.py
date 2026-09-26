import os
from dotenv import load_dotenv

load_dotenv()

# Global holders for local model (lazy loaded to prevent blocking FastAPI startup)
explain_tokenizer = None
explain_model = None
_local_model_loaded = False
_local_model_failed = False

def _get_local_model():
    """Lazily load the LaMini-Flan-T5-783M model as specified in EduGenie architecture."""
    global explain_tokenizer, explain_model, _local_model_loaded, _local_model_failed
    if _local_model_loaded:
        return explain_tokenizer, explain_model
    if _local_model_failed:
        return None, None

    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch
        print("Loading local explanation model: MBZUAI/LaMini-Flan-T5-783M...")
        explain_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        explain_model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
        _local_model_loaded = True
        return explain_tokenizer, explain_model
    except Exception as e:
        print(f"Notice: Local model could not be loaded ({e}). Using Gemini for explanation.")
        _local_model_failed = True
        return None, None

def explain_topic(topic: str) -> str:
    """
    Explains the concept in a simple and clear way for a school student.
    Uses MBZUAI/LaMini-Flan-T5-783M locally when available, with intelligent Gemini fallback.
    """
    tok, model = _get_local_model()
    if tok is not None and model is not None:
        try:
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = tok(input_text, return_tensors="pt")
            outputs = model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = tok.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"Error during local model inference: {e}. Falling back to Gemini.")

    # Fallback to Gemini with the exact educational instruction
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return f"The concept '{topic}' is fundamental in learning. Please configure your GEMINI_API_KEY in .env to get full AI explanations."
        genai.configure(api_key=api_key)

        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student. Keep it concise, friendly, and engaging."
        try:
            gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            gemini_model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Explanation: {e}"
