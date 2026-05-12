# Interview Guide

## Architecture Explanation

Student Decisoom is a full-stack student career planning MVP. The frontend is a React/Vite workspace that guides a student through intake, shows a recommended track, renders a six-week roadmap, tracks progress, and lets the student ask a local mentor engine for next-step guidance.

The backend is Flask with an app factory, route modules, service modules, and SQLite persistence. Routes stay thin. Services own scoring, roadmap generation, progress merging, and mentor responses. Vercel hosts a serverless Flask entrypoint that serves both `/api/*` and the built frontend.

## Why This Stack

- React/Vite: fast iteration and easy deployment for a frontend-heavy MVP.
- Flask: small API surface, low ceremony, simple service boundaries.
- SQLite: no external database required for demos and local development.
- Vercel: easy portfolio deployment and one public URL.

## Important Tradeoffs

- SQLite is intentionally temporary. It is excellent for local demos, weak for serverless persistence.
- No auth yet because the product is single-user. Adding auth before validating the workflow would create fake complexity.
- The mentor is deterministic. This makes it reliable and cheap, but less powerful than a real AI provider.
- Frontend state is local. That is fine for one workspace, but it should move into a dedicated state layer if accounts, teams, or background sync are added.

## Biggest Engineering Challenges

- Keeping the app realistic without overengineering it.
- Making the deployed frontend call the correct API in production.
- Preserving a clean boundary between deterministic career logic and future AI-provider logic.
- Making progress updates idempotent through stable task keys.
- Explaining serverless storage limitations honestly.

## Scaling Strategy

1. Replace SQLite with Postgres or Turso.
2. Add user accounts and row-level ownership.
3. Move rate limiting to Redis or an API gateway.
4. Add analytics events around intake completion, roadmap generation, and task updates.
5. Add background jobs for roadmap regeneration and mentor summaries.
6. Add provider-backed mentor responses behind `MENTOR_PROVIDER`.

## Senior Interview Questions

- Why did you choose SQLite, and when would you migrate away from it?
- How do you prevent one student from reading another student's roadmap?
- What happens to data on Vercel serverless when the function restarts?
- Why is the mentor deterministic instead of LLM-backed?
- How would you test the scoring algorithm?
- How would you version the roadmap schema if tasks change after users start tracking progress?
- What would break first under 10,000 users?
- How would you make progress updates safe under concurrent requests?
- How would you add analytics without polluting product code?
- How would you monitor failed mentor requests in production?
- How would you explain this project without overselling it as a complete AI product?

## Honest Demo Script

"This is a single-user MVP designed to validate the student career planning loop. I intentionally kept the stack simple: React for the workspace, Flask for APIs, SQLite for local persistence, and deterministic mentor logic for predictable demos. The production hardening work includes request IDs, security headers, rate limiting, error boundaries, retry behavior, and deployment tradeoff documentation. The next real step would be persistent hosted storage and authentication."
