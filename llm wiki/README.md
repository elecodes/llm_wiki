# 🎾 Tennis Academy Knowledge Base (LLM Wiki)

An automated, privacy-first knowledge extraction system that transforms raw institutional communications (emails, newsletters) into a structured, searchable, and anonymized knowledge base.

## 🚀 Overview
This project solves the problem of "hidden knowledge" in email threads. It uses a custom Python pipeline to extract pricing, programs, locations, and operational details from raw email data, ensuring all personal identifiable information (PII) is removed before publication.

### Key Features
- **Automated Extraction**: Parses raw data and synthesizes it into structured Markdown using Gemini 2.5-Flash.
- **PII Sanitization**: Multi-layer anonymization using Regex patterns and LLM verification.
- **Obsidian Integration**: Generates Wiki-style links and indices for seamless navigation.

## 🧠 Tech Stack
- **Core**: Python 3.x
- **LLM**: Google Gemini 2.5-Flash
- **Storage**: Markdown (Obsidian-ready)

## 📂 Project Structure
```text
llm wiki/
├── wiki/            # The generated knowledge base
├── wiki_vault/      # Raw AI extractions from sources (Gmail, etc.)
├── scripts/         # Extraction and sanitization logic
├── docs/            # Project documentation (ADRs, Playbooks)
├── raw/             # Legacy raw source material
└── templates/       # Markdown templates for consistency
```

## 🛠️ Setup & Usage
1. `pip install -r requirements.txt`
2. Configure API keys in `.env`.
3. Run `python scripts/sync_emails.py`.

---
*Developed as part of the [elecodes](https://github.com/elecodes) portfolio.*
