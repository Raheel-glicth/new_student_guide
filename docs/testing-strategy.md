# Testing Strategy

## Current Gate

- Frontend production build: `cd frontend && npm run build`
- Backend syntax check: `python -m py_compile ...`
- Manual API smoke test: health, intake, roadmap, progress, mentor

## Near-Term Automated Tests

- Unit test career scoring with representative student profiles.
- Unit test intake validation for missing fields and invalid answer values.
- Integration test `POST /api/intake` creates a roadmap.
- Integration test `POST /api/progress` is idempotent by `taskKey`.
- Frontend smoke test that the app renders, questionnaire advances, and empty states appear.

## CI Recommendation

Use GitHub Actions with two jobs:

- `frontend`: install dependencies and run `npm run build`.
- `backend`: install Python dependencies and run unit/integration tests against a temporary SQLite database.

## Why This Matters

The highest-risk business logic is not the UI. It is the scoring and roadmap/progress contract. If task keys change, progress history can silently break. Tests should protect those contracts before adding more product surface.
