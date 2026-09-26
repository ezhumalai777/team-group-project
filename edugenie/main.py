import os
from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, set_key

load_dotenv()

# Import the five core EduGenie modules as specified in architecture
from explanation_module import explain_topic
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie: Google Gemini Powered Learning Assistant",
    description="A lightweight AI-powered educational assistant built with FastAPI and Google Gemini.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and setup templates
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Root Endpoint: Serves the Web Interface
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    api_key_set = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    try:
        return templates.TemplateResponse(request=request, name="index.html", context={"api_key_set": api_key_set})
    except Exception:
        return templates.TemplateResponse("index.html", {"request": request, "api_key_set": api_key_set})


# 1. Q&A - GET API using Gemini (with POST support for flexibility)
@app.get("/qa")
async def answer_question(question: str = Query(..., description="The student query")):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

@app.post("/qa")
async def answer_question_post(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return JSONResponse(content={"error": "Please provide a question."}, status_code=400)
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# 2. Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

@app.get("/explain")
async def explain_get_api(topic: str = Query(...)):
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# 3. Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}

# 4. Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    print("Generated quiz:", quiz)  # DEBUG as in project spec
    return JSONResponse(content={"quiz": quiz})

# 5. Learning Recommendations - GET API (with POST support)
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

@app.post("/learn/recommendations")
async def learning_recommendation_post(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

# Helper endpoint to update or check API key dynamically
@app.get("/api/config")
async def get_config():
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    masked_key = f"{key[:6]}...{key[-4:]}" if len(key) > 10 else ("Configured" if key else "Not Configured")
    return {"configured": bool(key), "masked_key": masked_key}

@app.post("/api/config")
async def set_api_key(request: Request):
    data = await request.json()
    key = data.get("api_key", "").strip()
    if not key:
        return JSONResponse(content={"error": "API key cannot be empty"}, status_code=400)
    os.environ["GEMINI_API_KEY"] = key
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    try:
        set_key(env_path, "GEMINI_API_KEY", key)
    except Exception:
        with open(env_path, "a") as f:
            f.write(f"\nGEMINI_API_KEY={key}\n")
    return {"status": "success", "message": "API key successfully updated."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
