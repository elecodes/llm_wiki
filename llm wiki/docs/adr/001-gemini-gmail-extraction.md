# ADR 1: Automated Knowledge Extraction from Gmail using Gemini

## Status
Accepted

## Context
The LLM Wiki project aims to maintain a curated knowledge base of tennis-related information. 
The primary source of truth is Gmail communications (inquiries, registrations, rates). 
Manually extracting this data into Markdown files is tedious and prone to missing details (like specific fees or availability slots).

## Decision
We will use a Python-based synchronization system (`scripts/sync_emails.py`) that:
1. Connects to the Gmail API to fetch relevant messages.
2. Uses the **Gemini 2.5-flash** model to perform "Knowledge Extraction".
3. Generates structured Markdown files in a `wiki_vault/` directory.
4. Uses a "Source" metadata pattern to link curated wiki pages to their raw vault counterparts.

## Rationale
- **Gemini 2.5-flash**: Selected for its speed, large context window (for long email threads), and cost-effectiveness.
- **Vault/Wiki Split**: Separating raw extractions (`wiki_vault`) from curated content (`wiki`) ensures that the master pages remain clean while preserving the original context for verification.
- **Python**: Provides robust integration with the Google Cloud ecosystem (Gmail API).

## Consequences
- Requires a valid `credentials.json` and OAuth flow.
- The wiki becomes "alive" and reflects real-world data changes within minutes.
- Maintenance involves reviewing the vault and updating master pages.
