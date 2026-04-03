# ✦ ARIA — AI-Powered Assistant Web Application

> **Adaptive Reasoning & Intelligence Assistant** — A production-grade conversational AI interface powered by Google Gemini.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-API-orange?style=flat-square)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## Overview

ARIA is a full-stack AI assistant web application that demonstrates end-to-end LLM integration with a polished, production-quality UI. It leverages Google's Gemini models for intelligent, context-aware responses across coding, analysis, writing, and reasoning tasks.

### Key Features

- **Multi-turn Conversations** — Full context window management; the model remembers your entire session
- **Model Selection** — Switch between `gemini-1.5-flash`, `gemini-1.5-pro`, and `gemini-2.0-flash-exp`
- **Customizable System Prompts** — Inject persona or task-specific instructions at runtime
- **Adjustable Parameters** — Fine-tune temperature and max tokens per session
- **Chat Export** — Download full conversation history as structured JSON
- **Professional Dark UI** — Custom CSS theme with animated message bubbles and live session stats

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | Streamlit + Custom CSS            |
| Backend    | Python 3.9+                       |
| LLM API    | Google Gemini (`google-generativeai`) |
| State Mgmt | Streamlit Session State           |
| Deployment | Streamlit Cloud / Docker          |

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/aria-ai-assistant.git
cd aria-ai-assistant

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Configuration

Enter your Gemini API key in the sidebar when the app loads. No `.env` file required — keys are handled securely in-memory during the session.

---

## Deployment (Streamlit Cloud)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `app.py` as the entry point
5. Deploy — no extra config needed

---

## Project Structure

```
aria-ai-assistant/
│
├── app.py              # Main application — UI + LLM logic
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## How It Works

1. **API Initialization** — User provides a Gemini API key; the app validates and configures the SDK
2. **Context Management** — Full message history is maintained in `st.session_state` and passed to the Gemini chat API on each turn
3. **Prompt Engineering** — System prompt is injected at the model level via `system_instruction`, allowing role and behavior customization without polluting the user-visible chat
4. **Response Rendering** — Model output is streamed and rendered inside styled bubble components with timestamps

---

## Author

**Abdurrahman Abdulazeez**  
📧 abdulitz95@gmail.com | 🌍 Kaduna, Nigeria  
Computer Science @ University of the People

---

## License

MIT — free to use, modify, and distribute.
