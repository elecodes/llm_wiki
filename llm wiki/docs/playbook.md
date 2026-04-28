# 📘 LLM Wiki Playbook

## 📥 Workflow
1. Add raw data to `raw/`.
2. Run `python scripts/sync_emails.py`.
3. Verify extraction in `wiki_vault/`.
4. Move validated content to `wiki/`.
5. **Consolidate & Cleanup**: Merge redundant files and delete obsolete raw/wiki pairs.

## 🧹 Privacy
- Redact all student names and phone numbers.
- Use the `cleanup_pii.py` script for automated sweeps.
- **Anonymization**: Replace PII with `[REDACTED]` or generic placeholders (e.g., `[STUDENT]`).

## 🛠 Troubleshooting

### Backend Hanging on Startup
If the `chat_server.py` hangs during import (specifically when importing `google.generativeai`), it is often due to a corrupted virtual environment or gRPC conflicts on macOS.
**Solution**:
1. Stop any running python processes.
2. Delete the `.venv` directory.
3. Recreate it: `python3 -m venv .venv`.
4. Reinstall dependencies: `pip install -r requirements.txt`.

### Frontend Connection Errors
If you see `ERR_CONNECTION_REFUSED` in the browser console, ensure the FastAPI server is running on port 8000.

### Local Dev Startup Order
Use two terminals and start backend first:
1. `cd "llm wiki" && source .venv/bin/activate && python scripts/chat_server.py`
2. `cd "llm wiki/chat-ui" && npm run dev`

If the frontend shows `:8000/api/query net::ERR_CONNECTION_REFUSED`, backend is down or failed to bind.

### UI Spacing Changes Not Showing
If chat spacing updates are not visible even after code changes, force a browser hard refresh with `Cmd+Shift+R`.
