# Architecture Decisions

## ADR-001: Keep React + Flask Instead of Rewriting

Decision: Keep the existing React/Vite frontend and Flask backend.

Why: The product is still in MVP validation. A rewrite to Next.js, TypeScript, or a full backend framework would add ceremony before the core workflow proves value.

Tradeoff: Some frontend state remains local and manual. That is acceptable while the app has one main workspace.

## ADR-002: SQLite for Local MVP, Not Real Multi-User Production

Decision: Use SQLite for local persistence and demo deployment.

Why: It keeps setup simple and makes the product easy to run in interviews or hackathons.

Tradeoff: Vercel serverless storage is ephemeral. Before real users, move data to Postgres, Turso, or another managed database.

## ADR-003: Deterministic Mentor First

Decision: The mentor is a local coaching engine instead of a live LLM call.

Why: It makes behavior predictable, cheap, and explainable. It also avoids shipping a fragile prompt-only feature too early.

Tradeoff: Advice is less flexible than a provider-backed LLM. The `MENTOR_PROVIDER` config keeps the path open for an OpenAI-backed implementation later.

## ADR-004: One-Domain Vercel Deployment

Decision: Serve the React build and Flask API from the same Vercel domain through `api/index.py`.

Why: It avoids CORS and production API-base mistakes. It also makes the demo easy to share.

Tradeoff: Static assets are served through Flask routing in the current Vercel setup. This is fine for a portfolio demo, but a larger app should use a CDN-first static build plus separate API service.

## ADR-005: Lightweight Observability

Decision: Add request IDs, timing logs, and security headers without adding a monitoring vendor yet.

Why: The project becomes debuggable without requiring paid infrastructure.

Tradeoff: Logs are still platform-dependent. A production app would ship logs to a provider and connect errors to frontend telemetry.

## ADR-006: In-Memory Rate Limiting

Decision: Add simple in-memory rate limiting for intake and mentor writes.

Why: It protects the demo from accidental spam and shows awareness of abuse surfaces.

Tradeoff: It is not distributed. Real production should use Redis, Upstash, or gateway-level rate limiting.
