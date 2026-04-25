# ADR 003: Knowledge Consolidation and Redundancy Management

## Status
Accepted

## Context
As the knowledge base grows through automated extractions (Gmail syncs), redundant information often appears across multiple files (e.g., initial inquiry vs. reply thread, or multiple emails covering the same topic). Keeping these as separate files leads to "knowledge fragmentation" and makes maintenance difficult.

## Decision
We will proactively consolidate redundant information into single, well-structured "Master Pages". 

### Procedures:
1.  **Merge Overlap**: When multiple files cover the same topic, merge the most relevant and complete information into the primary page (usually the most recent or best-named one).
2.  **Delete Redundant Sources**: Once consolidated, both the redundant wiki pages AND their corresponding raw files (in `raw/`) should be deleted to maintain a clean "Source of Truth".
3.  **Update References**: All links in the `index.md`, `pricing.md`, `programs.md`, etc., must be updated to point to the consolidated page.
4.  **Audit Logs**: Every consolidation or deletion must be recorded in `wiki/log.md`.

## Rationale
- **Single Source of Truth (SSOT)**: Ensures that users and AI agents find the most accurate and up-to-date information in one place.
- **Reduced Noise**: Minimizes the volume of files to search and process, saving tokens and cognitive load.
- **Clean Lineage**: Removing redundant raw files prevents future re-extractions of already processed (and now obsolete) data.

## Consequences
- Requires active human or agent oversight to identify overlaps.
- The `index.md` requires frequent updates to reflect the consolidated structure.
- Some "raw" historical context may be lost if not properly summarized in the merged wiki page.
