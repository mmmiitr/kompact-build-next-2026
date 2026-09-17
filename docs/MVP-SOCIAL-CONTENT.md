# MVP — Social Media Content Helper (LOCKED for Phase 1)

**Status:** GO — Phase 1 ship target  
**Date locked:** 2026-09-17 (IST)  
**Hackathon:** [ZIROH LABS Build Next 2026 / Kompact AI](https://www.ziroh.com/hackathon)  
**Deadline Phase 1:** 2026-09-18  
**Tracking:** `krantikaridev/self` #66  
**Repo:** https://github.com/mmmiitr/kompact-build-next-2026

## One-liner

Upload a **short video** + a **prompt** → get a **publish-ready pack**: title, captions, hashtags, description, and trim suggestions.

## What this is / is not

| Is | Is not |
| --- | --- |
| Creator workflow helper for Reels / Shorts / TikTok-style clips | Kabootri (or any) social **upload** / posting client |
| OpenAI-compatible LLM client (`BASE_URL` / `API_KEY` / `MODEL`) | Hard-wired to one cloud vendor |
| Metadata-aware (duration via ffprobe when present) | Full multimodal video understanding in Phase 1 |
| Runnable offline with labeled **MOCK** packs | Dependent on paid API for demo |

## Why this product (vs earlier brainstorm)

Earlier analysis kept GazetteApply / SME Policy Copilot open (`docs/PHASE1-ANALYSIS.md`). For the remaining calendar, Madan locked a **sharper, demoable creator loop**:

1. Clear before/after: blank form → structured publish pack JSON + UI.
2. Real-world impact: India creators and SMEs waste hours rewriting captions/hashtags per platform.
3. Kompact-ready: same chat-completions client; Phase 2 swaps `BASE_URL` to Kompact CPU runtime without rewriting the app.
4. Honest scope: no invented posting integrations; no prize claims.

## CPU / Kompact future narrative

Phase 1 runs against any OpenAI-compatible endpoint (or MOCK with empty `API_KEY`).

Phase 2 (if Top 20) story:

- Point `BASE_URL` at Kompact CPU inference; keep prompts and JSON schema identical.
- Caption/hashtag generation is a **narrow, high-frequency** workload — fits CPU-first cost story for creators and agencies who cannot afford GPU tax per draft.
- Optional later: on-device / edge summarization of trim cues; still no requirement to post on behalf of the user.

Sustainable AI angle (for judges): **cheaper iteration on copy**, not bigger models. Creators iterate 10–20 packs per day; CPU inference economics matter.

## Architecture (Phase 1)

```
Browser (static index.html)
    │ multipart: video + prompt
    ▼
FastAPI  POST /api/publish-pack
    ├─ save temp file
    ├─ ffprobe duration (or size-based stub)
    ├─ if API_KEY empty → deterministic MOCK pack (labeled)
    └─ else → OpenAI-compatible chat.completions → JSON pack
```

Env boundary (Phase 2 swap surface):

| Variable | Role |
| --- | --- |
| `BASE_URL` | OpenAI-compatible API root (e.g. `https://api.openai.com/v1` or Kompact later) |
| `API_KEY` | Bearer token; empty → MOCK |
| `MODEL` | Model id string |

## API

### `POST /api/publish-pack`

- Form fields: `video` (file), `prompt` (string)
- Response JSON: `mode` (`MOCK`|`LLM`), `title`, `captions[]`, `hashtags[]`, `description`, `trim_suggestions[]`, `video` metadata, `prompt`, optional `model`

### `GET /health`

Config echo without secrets (`has_api_key` boolean only).

### `GET /`

Static upload UI.

## Non-goals (Phase 1)

- Auto-posting to X / Instagram / YouTube / Kabootri
- Fine-tuned video vision models
- User accounts / persistence
- Claiming production client deployments or prize outcomes

## Related docs

- [`PHASE1-ANALYSIS.md`](./PHASE1-ANALYSIS.md) — earlier option matrix (historical)
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — early agentic draft (superseded for Phase 1 product; LLM client pattern still applies)
- [`SUBMISSION.md`](./SUBMISSION.md) — paste-ready Phase 1 entry text
