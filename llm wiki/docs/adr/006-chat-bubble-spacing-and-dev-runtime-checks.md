# ADR 006: Chat Bubble Spacing and Dev Runtime Checks

## Status
Accepted

## Context
The chat UI required iterative spacing adjustments to improve readability and perceived visual balance. During this work, repeated `ERR_CONNECTION_REFUSED` errors occurred in the frontend when querying `:8000/api/query`, caused by the backend not running on port 8000.

## Decision
We decided to:
1. Apply explicit bubble spacing and text alignment tweaks in the chat view to make message content visually balanced.
2. Document a two-terminal development workflow (backend + frontend) as the standard local runtime pattern.
3. Treat `ERR_CONNECTION_REFUSED` on `:8000/api/query` as a backend runtime check first, not a frontend styling issue.
4. Document hard refresh (`Cmd+Shift+R`) as a practical step when Vite HMR does not immediately reflect visual CSS/layout tweaks.

## Consequences
- Chat message readability and spacing consistency are improved.
- Developers have a clearer startup sequence and faster diagnosis path for API connectivity issues.
- Runtime diagnosis is more predictable: verify backend health before investigating frontend request code.
