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
