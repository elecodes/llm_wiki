# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-04-27

### Added
- **Model Fallback System**: Implemented automated rotation between Gemini models (`2.0-flash`, `2.5-flash`, `flash-lite`, etc.) to handle 429 quota errors gracefully.
- **Knowledge Absorption**: New UI feature in the Chat interface to "Absorb into Wiki". Allows generating structured Markdown from chat history and reviewing/editing it before saving to the wiki.
- **Premium UI Refinement**: 
  - Monospace rendering and "Source" badges for raw documents in the Wiki view.
  - "Dark Modern" theme (Obsidian-inspired) with glassmorphism and enhanced typography (Outfit/Inter).
  - New icons and polished layout for the Header and Search interfaces.
- **Proposed Wiki Update Modal**: Integrated a review step for AI-generated wiki updates.

### Fixed
- **Backend Stability**: Resolved environment-related hangs on macOS by refining the `.venv` setup guide.
- **API Model Mapping**: Fixed 404 errors by mapping `gemini-1.5-flash` to the correct `gemini-flash-latest` identifier.
- **Source Rendering**: Improved the readability of "raw" source documents by applying specific styling and badges.

### Changed
- Updated `QueryEngine` to handle multi-model generation and error retry logic.
- Standardized backend port to 8000 and improved Python path handling for library imports.
