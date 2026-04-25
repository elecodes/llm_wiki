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
