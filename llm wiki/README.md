# 🎾 Tennis Academy Knowledge Base (LLM Wiki)

An automated, privacy-first knowledge extraction system that transforms raw institutional communications (emails, newsletters) into a structured, searchable, and anonymized knowledge base.

## 🚀 Overview

This project solves the problem of "hidden knowledge" in email threads. It uses a custom Python pipeline to extract pricing, programs, locations, and operational details from raw email data, ensuring all personal identifiable information (PII) is removed before publication.

### Key Features

- **Automated Extraction**: Parses raw data and synthesizes it into structured Markdown.
- **PII Sanitization**: Multi-layer anonymization using Regex patterns and LLM verification to protect names, phones, and private data.
- **Obsidian Integration**: Generates Wiki-style links and indices for seamless navigation in Obsidian or any Markdown viewer.
- **Smart Indexing**: Automatically categorizes content into Programs, Pricing, Locations, and Customer Inquiries.

## 🧠 Architecture & Tech Stack

- **Core**: Python
- **LLM**: Google Gemini Pro (via LangChain)
- **Anonymization Engine**: Custom Regex-based pre-processor + LLM-based verification.
- **Frontend/Storage**: Obsidian-ready Markdown files.

## 📂 Project Structure

```text
llm wiki/
├── raw/           # Raw source material (sanitized during processing)
├── wiki/          # The generated knowledge base (Obsidion-ready)
│   ├── index.md   # Main entry point
│   └── ...        # Categorized knowledge pages
├── scripts/       # Extraction and sanitization logic
└── templates/     # Markdown templates for consistency
```

## 🛠️ Usage

1. Place raw data in `raw/`.
2. Run the processing script:
   ```bash
   python scripts/process_wiki.py
   ```
3. Open the `wiki/` folder in Obsidian to explore the Tennis Academy's collective knowledge.

---
*Developed as part of the [elecodes](https://github.com/elecodes) portfolio.*
