# ADR 002: Project Structure

## Status
Accepted

## Context
We need a clear separation between raw input, automated extraction, and curated knowledge to maintain a clean and searchable wiki.

## Decision
Adopt the following directory structure:
- `/raw`: Immutable source files.
- `/scripts`: Logic for synchronization and processing.
- `/wiki_vault`: Interim stage for AI extractions.
- `/wiki`: Final curated knowledge.

## Consequences
- Clear data lineage.
- Prevents PII from leaking into the final wiki.
- Supports automated synchronization workflows.
