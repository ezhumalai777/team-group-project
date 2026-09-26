# EduGenie: Google Gemini Powered Learning Assistant 🎓✨

**EduGenie** is a lightweight, AI-powered educational assistant designed to simplify learning through generative AI. Designed for students of all academic levels, EduGenie provides concise Q&A answers, simplified concept explanations, dynamic quiz generation with automatic answer checking, text summarization, and personalized learning pathways.

Built as part of the **SmartBridge / SmartInternz** program.

---

## 🌟 Key Features

1. **Ask EduGenie a Question (Q&A Module - `/qa`)**
   - Answers academic and general questions concisely and accurately using Gemini 1.5 Pro.
   - Example: *"Which is the largest ocean?"*
2. **Concept Explanation Module (`/explain`)**
   - Breaks down complex academic concepts into simple, easily digestible language tailored for school students.
   - Example: *"Photosynthesis"*, *"Quantum Computing"*
3. **Summarization Module (`/summarize`)**
   - Summarizes long educational passages for quick revision while eliminating redundancy.
   - Example: *"The Industrial Revolution..."*
4. **Quiz Generation Module (`/quiz`)**
   - Automatically generates 3 Multiple Choice Questions (MCQs) with 4 options and answer verification.
   - Interactive UI provides instant feedback: `✅ Correct!` or `❌ Incorrect. Correct answer: ...`
   - Example: *"The Pythagoras Theorem"*, *"Solar System"*
5. **Learning Path Module (`/learn/recommendations`)**
   - Formulates a personalized, structured learning roadmap from Beginner to Advanced with timelines and recommended learning resources.
   - Example: *"SQL"*, *"Linear Regression"*

---

## 🏗️ Architecture & Technology Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI)
- **AI Models**:
  - **Google Gemini 1.5 Pro / Flash**: Q&A, Quizzes, Summaries, Learning Recommendations, Explanations.
  - **LaMini-Flan-T5-783M (local)**: Instruction-tuned Seq2Seq model for concept explanation with automatic cloud fallback.
- **Frontend**: HTML5, Vanilla CSS3, Jinja2 Templating, and JavaScript with interactive feedback.

---

## 📁 Project Folder Structure

```text
edugenie/
├── main.py                   # FastAPI application & REST API routing
├── explanation_module.py     # Concept explanation logic (LaMini-Flan-T5 / Gemini)
├── qna.py                    # Question-answering module (Gemini)
├── quiz_module.py            # MCQ quiz generation & JSON formatting
├── summary_module.py         # Passage summarization module
├── learning_path.py          # Structured learning path recommendations
├── gemini_helper.py          # Resilient dual-mode Gemini integration
├── templates/
│   └── index.html            # Responsive web UI with interactive forms & quiz runner
├── static/
│   └── style.css             # Modern stylesheet with clean aesthetics & responsive layout
├── .env                      # Local environment configuration
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A Google Gemini API Key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Installation

1. Clone or navigate to the repository directory:
   ```bash
   cd edugenie
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Google Gemini API Key:
   - Edit the `.env` file in the project root:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```
   - *Tip*: You can also set or update the key directly from the Web Interface by clicking the **API Key** badge in the top right header!

### 3. Running the Application

Launch the local development server:
```bash
uvicorn main:app --reload
```

Or run with Python launcher:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Input | Description |
| :--- | :---: | :--- | :--- |
| `/` | `GET` | — | Renders the EduGenie interactive web interface |
| `/qa` | `GET` / `POST` | `question` | Generates a concise answer to student query |
| `/explain` | `POST` / `GET` | `topic` | Provides simple concept explanation |
| `/summarize` | `POST` | `text` | Summarizes long paragraphs into key points |
| `/quiz` | `POST` | `text` | Generates 3 MCQs in JSON format with options and answers |
| `/learn/recommendations` | `GET` / `POST` | `topic` | Generates structured beginner-to-advanced learning path |
| `/api/config` | `GET` / `POST` | `api_key` | Checks or updates the Gemini API key configuration |

---

## 📝 Project Details

- **Project**: EduGenie - Google Gemini Powered Learning Assistant
- **Submitted by**: Tella Divya Sree
- **Mentor**: Siri
- **Organization**: SmartBridge / SmartInternz
