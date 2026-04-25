# Log

**Append-only record of all wiki operations**

---

## 2026-04-19

**Source added**: [[tennis-kids-lessons-and-summer-camps-san-francisco]] (raw/)

**Pages created**:

- [[sf-tennis-kids-club]] — Club overview
- [[programs]] — Age-grouped lesson programs
- [[summer-camps]] — Summer Camp 2026 details
- [[pricing]] — Current offers and Early Bird discount
- [[locations]] — SFSU campus location
- [[index]] — Updated table of contents

## 2026-04-19 (Email sync via Gmail)

**Emails synced from TO-WIKI label**:

- [[parent-and-me-classes]] — Min age 4, pricing ($82.50-$56.25), Spring season
- [[question-about-14-year-old-beginners]] — Grouped by age AND skill
- [[spots-are-filling-fast-sf-tennis-kids-summer-camp]] — Sibling 5%, Multi-week 5%, Refer 10%

**Wiki updated**:

- [[programs]] — Added Parent & Me details, teen grouping policy
- [[pricing]] — Added sibling, multi-week, refer-a-friend discounts
- [[index]] — Added source links to raw/

## 2026-04-20 (PII Sanitization & Workflow Update)

**Security Hardening**:
- Updated `sync_emails.py` with aggressive PII redaction (regex + LLM).
- Implemented `sanitize_filename` to prevent PII leakage in filenames.
- Cleaned up all existing files in `raw/` and `wiki/` using `cleanup_pii.py`.

**Workflow Adjustment**:
- Files in `raw/` now contain **sanitized raw context** (source).
- Files in `wiki/` now contain **curated extraction** (processed info).
- Updated `index.md` with new sanitized links.
- Adjusted `sync_emails.py` to save to both locations automatically.

## 2026-04-24 (Wiki Maintenance & Cleanup)

**Maintenance**:
- Created `docs/maintenance.md` with official procedures for updating/deleting Wikis and Raws.

**Cleanup**:
- Deleted `parent-and.md` (redundant question, info present in `re-parent-and.md`).
- Deleted `question-about-14-year-old-beginners-1.md` (empty/redacted placeholder).
- Updated `index.md` to remove links to deleted pages.
- Deleted `question-about-14-year-old-beginners.md` (invalid template/hallucinated file with incorrect $45 price).
- Cleaned up `pricing.md` sources to remove reference to the deleted file.

## 2026-04-25 (Maintenance)

**Cleanup**:
- Deleted `raw/Parent-and-Me-Classes.md` (redundant, info in `raw/Re-Parent-and-Me-Classes.md`).
- Updated `programs.md` to point to the correct wiki source `[[re-parent-and]]`.
- Deleted `wiki/ready-toon-the-tennis-courts-join.md` and `raw/Ready-to-Get--on-the-tennis-courts-Join-Ou.md` (redundant, info in `re-ready-toon-the-tennis-courts.md`).
- Updated `index.md` to remove the redundant link.
- Consolidated `re-question-about-14-year-old-beginners.md` and `re-question-about-14-year-old-beginners-1.md` into a single `Teenager Grouping Policy`.
- Updated `index.md` to reflect the new consolidated page title.