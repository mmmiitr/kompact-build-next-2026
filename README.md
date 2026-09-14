# kompact-build-next-2026

**Status:** PLACEHOLDER — analysis only. Do not treat this as a submitted build.

Hackathon: [ZIROH LABS Build Next 2026 / Kompact AI](https://www.ziroh.com/hackathon)  
Parent tracking: `krantikaridev/self` issue **#66**  
Analysis note: see `docs/PHASE1-ANALYSIS.md` (also mirrored under `self/placement/notes/`).

## What this repo will become (after expert review)

Recommended direction (pending Madan + Grok expert sign-off):

**GazetteApply Lite** — a fixed **agentic workflow** (not a free-form ReAct agent) that:
1. Ingests a human-readable “amendment” instruction
2. Retrieves related rule/document chunks (RAG)
3. Applies changes to produce a revised HTML/Markdown draft + diff
4. Exposes an **OpenAI-compatible** chat/completions client so Phase 2 can swap the backend to **Kompact AI CPU runtime** without rewriting the app

Phase 1 does **not** require Kompact runtime access (finalists only). Phase 1 demo can use any OpenAI-compatible endpoint (local Ollama / cloud) behind the same client.

## Non-goals (until GO)

- No prize-hunting all-nighter without Madan GO
- No live trading, no secrets, no invented metrics
- No claiming Maruti production deploy — public demo uses synthetic docs only

## License

MIT (placeholder)
