# SF Tennis Kids Club Wiki & Chatbot

This project is an LLM-powered knowledge base for the SF Tennis Kids Club. It includes a Python-based RAG (Retrieval-Augmented Generation) backend and a React-based chat interface.

## ✨ Key Features

- **RAG-Powered Chat**: Intelligent responses grounded in the club's specific knowledge base.
- **Knowledge Absorption**: Instantly turn chat conversations into structured Wiki pages with a built-in review modal.
- **Model Fallback System**: Automatic rotation between multiple Gemini models to bypass "Quota Exceeded" errors on the Free Tier.
- **Premium UI**: Dark-themed, modern interface with glassmorphism, responsive design, and source document highlighting.
- **Automated PII Cleanup**: Scripts to ensure student and parent privacy by sanitizing personal information.

## Project Structure

- `wiki/`: Markdown files containing the club's knowledge base.
- `scripts/`: Python scripts for data processing and the chat server.
- `chat-ui/`: React + Vite frontend for the chatbot.
- `docs/adr/`: Architecture Decision Records documenting key technical choices.

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
   The UI will be available at `http://localhost:5173`.

### 3. Run Backend + Frontend Together

Use two terminals while developing:

- Terminal A (backend):
  ```bash
  cd "llm wiki"
  source .venv/bin/activate
  python scripts/chat_server.py
  ```
- Terminal B (frontend):
  ```bash
  cd "llm wiki/chat-ui"
  npm run dev
  ```

## Troubleshooting

- **429 Quota Errors**: The system automatically attempts to switch models. If it fails, wait 60 seconds for the quota to reset.
- **Backend hangs on import**: If the backend process hangs when starting, delete the `.venv` folder and recreate it.
- **Connection Refused (`:8000/api/query`)**: The frontend is running, but the backend is not listening on port 8000. Start `python scripts/chat_server.py` from the project root with `.venv` activated.
- **UI changes not visible**: If Vite hot reload misses a visual tweak, do a hard refresh (`Cmd+Shift+R`) in the browser.
