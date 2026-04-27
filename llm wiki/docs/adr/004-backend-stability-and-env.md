# ADR 004: Backend Stability and Environment Management

## Status
Accepted

## Context
During development, the backend server (`chat_server.py`) experienced systemic hangs during the import of the `google-generativeai` library. This prevented the server from binding to port 8000, causing connection refused errors in the frontend. Investigations revealed that the existing virtual environment (`.venv`) was in a corrupted or deadlocked state.

## Decision
We decided to:
1. Formalize the virtual environment recreation as the primary recovery mechanism for hanging imports.
2. Ensure that the `.venv` is excluded from version control but its recreation is documented in the README.
3. Use a clean install of dependencies to resolve library conflicts (specifically `grpcio` and `protobuf` versions).

## Consequences
- Developers may need to recreate their `.venv` if they experience similar hangs.
- Startup time for a fresh clone increases slightly due to dependency installation, but stability is significantly improved.
- The project structure remains clean as `.venv` is ignored by git.
