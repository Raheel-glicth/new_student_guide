# Project Audit

## Executive Read

This is a believable single-user MVP, not a production SaaS yet. The strongest parts are the clear feature scope, small Flask service layer, local SQLite persistence, and a frontend that exercises the full product loop. The weakest parts were the thin operational layer, missing frontend failure isolation, no request throttling, limited documentation about tradeoffs, and an accidental secret in `.env.example`.

## What Felt Fake

- The app had a polished surface but very little operational reality: no request IDs, no rate limits, no structured error handling, no documented constraints.
- The README described the happy path but did not explain why SQLite, local deterministic mentor logic, or Vercel serverless were chosen.
- The mentor sounded like an AI feature but was intentionally deterministic. That is fine, but it needed to be framed as a local coaching engine, not as full AI.
- Production deployment initially hid a serious issue: the frontend defaulted to `localhost:5000` in production unless `VITE_API_BASE_URL` was configured.
- A real API key appeared in `.env.example`. That is the highest-risk issue and would immediately hurt trust in review.

## What Felt Junior

- Error handling was mostly `try/catch` in UI state with generic messages.
- Backend validation lived in service code, but API responses did not carry stable error codes.
- No rate limiting on mentor or intake endpoints.
- No frontend error boundary.
- No loading skeleton for the primary workspace.
- No observability story. If a user reported a bug, there was no request ID to connect frontend failure to backend logs.
- SQLite indexes were minimal. Fine for an MVP, but the intent should be visible.

## What Felt Production-Ready

- The product scope is coherent: intake, recommendation, roadmap, progress, mentor.
- Service boundaries are simple and readable.
- SQLite schema uses stable task keys and idempotent progress updates.
- Flask app factory pattern is a good base.
- Vercel deployment now serves frontend and API from one domain.
- The UI has a clear activation path and meaningful empty states.

## What Would Expose AI Generation

- Too many perfect product claims without tradeoffs.
- No mention of deployment limitations, serverless SQLite limitations, or single-user constraints.
- No tests or observability.
- Inconsistent production behavior: local frontend talking to localhost after deployment.
- Generic "AI mentor" language without explaining the deterministic fallback.

## Risk Register

- `High`: Secret hygiene. Any real key committed locally must be rotated.
- `High`: Serverless SQLite persistence. `/tmp` works for demos but is ephemeral on Vercel.
- `Medium`: No auth. This is acceptable for a demo, not for real student data.
- `Medium`: In-memory rate limiting resets per process and does not protect distributed traffic.
- `Medium`: No automated CI gate yet.
- `Low`: Frontend state is local and pragmatic, but would become difficult if multi-user accounts, notifications, or collaboration are added.

## Recommended Next Iterations

- Move persistent storage to Postgres or Turso before real users.
- Add auth only when user accounts are truly needed.
- Add a small CI workflow for frontend build and backend service tests.
- Add analytics events for intake completion, roadmap generation, task update, and mentor use.
- Replace deterministic mentor with provider-backed AI behind the existing `MENTOR_PROVIDER` boundary.
