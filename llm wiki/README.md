# SF Tennis Kids Club Wiki & Chatbot

This project is an LLM-powered knowledge base for the SF Tennis Kids Club. It includes a Python-based RAG (Retrieval-Augmented Generation) backend and a React-based chat interface.

## Project Structure

- `wiki/`: Markdown files containing the club's knowledge base.
- `scripts/`: Python scripts for data processing and the chat server.
- `chat-ui/`: React + Vite frontend for the chatbot.

## Getting Started

### 1. Backend Setup

The backend uses FastAPI and Google's Gemini API.

1. Ensure you have Python 3.12+ installed.
2. Navigate to the root directory (`llm wiki/`).
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create a `scripts/.env` file with your `GEMINI_API_KEY`.
5. Start the server:
   ```bash
   python scripts/chat_server.py
   ```
   The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1. Navigate to `chat-ui/`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
   The UI will be available at `http://localhost:5173` (or `5174` if 5173 is busy).

## Troubleshooting

- **Backend hangs on import**: If the backend process hangs without output when starting, it's likely a corruption in the virtual environment. Delete the `.venv` folder and recreate it as described in the setup steps.
