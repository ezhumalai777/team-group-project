import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_with_gemini(prompt: str, preferred_model: str = "gemini-1.5-pro") -> str:
    """
    Calls Google Gemini using the official google-generativeai SDK if installed,
    or falls back to the direct Gemini REST API via requests.
    Supports gemini-1.5-pro with automatic fallback to gemini-1.5-flash or gemini-2.0-flash.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google Gemini API key not found. Please set GEMINI_API_KEY in .env or via the web UI.")

    # 1. Attempt official google.generativeai SDK
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        models_to_try = [
            preferred_model if preferred_model.startswith("models/") else f"models/{preferred_model}",
            "models/gemini-1.5-pro",
            "models/gemini-1.5-flash",
            "models/gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash"
        ]
        
        last_err = None
        for m_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name=m_name)
                response = model.generate_content(prompt)
                if hasattr(response, "text") and response.text:
                    return response.text.strip()
                elif hasattr(response, "parts") and response.parts:
                    return response.parts[0].text.strip()
            except Exception as e:
                last_err = e
                continue
                
        # If SDK attempted all models and failed, try REST fallback
    except ImportError:
        pass
    except Exception as e:
        print(f"Notice: SDK call encountered ({e}), trying REST fallback...")

    # 2. Direct REST API Fallback (Fast, no heavy SDK required)
    models_to_try_rest = [
        preferred_model.replace("models/", ""),
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.0-flash"
    ]
    
    last_rest_err = None
    for model_name in models_to_try_rest:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=35)
            if res.status_code == 200:
                data = res.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()
            else:
                last_rest_err = f"HTTP {res.status_code}: {res.text}"
        except Exception as err:
            last_rest_err = str(err)
            continue

    raise RuntimeError(f"Could not generate content from Gemini API: {last_rest_err}")
