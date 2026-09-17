# kompact-build-next-2026

**Phase 1 MVP (GO):** Social media **content helper** — upload short video + prompt → publish-ready pack (title, captions, hashtags, description, trim suggestions).

Hackathon: [ZIROH LABS Build Next 2026 / Kompact AI](https://www.ziroh.com/hackathon)  
Phase 1 deadline: **2026-09-18**  
Tracking: [`krantikaridev/self` #66](https://github.com/krantikaridev/self/issues/66)  
Product: [`docs/MVP-SOCIAL-CONTENT.md`](./docs/MVP-SOCIAL-CONTENT.md)  
Submission draft: [`docs/SUBMISSION.md`](./docs/SUBMISSION.md)

### Honest Phase 1 scope

- **Metadata-first:** filename + `ffprobe` meta (duration, width/height, codec when available) + creator prompt.
- **Not** full video understanding (no Whisper/transcript or vision in this build — roadmap later).
- OpenAI-compatible via `BASE_URL` / `API_KEY` / `MODEL`. Empty `API_KEY` → labeled **MOCK** packs.
- **Not** a Kabootri (or any) upload/posting client — the tool drafts; the creator publishes.

## Quick start

```bash
git clone https://github.com/mmmiitr/kompact-build-next-2026.git
cd kompact-build-next-2026
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000

### Optional LLM

```bash
cp .env.example .env
# edit BASE_URL, API_KEY, MODEL
# python-dotenv loads .env automatically on app import
uvicorn app.main:app --reload --port 8000
```

With **empty `API_KEY`**, `POST /api/publish-pack` returns a deterministic pack with `"mode": "MOCK"` (no network, no spend).

Optional: install `ffmpeg`/`ffprobe` for real duration/resolution/codec metadata; otherwise duration is a size-based stub (still labeled in the response).

### One-command smoke

```bash
# with server already running on :8000
./scripts/demo_smoke.sh
# or let the script start uvicorn briefly:
START_SERVER=1 ./scripts/demo_smoke.sh
```

### API

| Method | Path | Notes |
| --- | --- | --- |
| `GET` | `/` | Upload UI (copy buttons + video meta + MOCK/LLM badge) |
| `GET` | `/health` | Liveness + config flags (no secrets) |
| `POST` | `/api/publish-pack` | multipart: `video`, `prompt` → JSON pack |

## Docs

| Doc | Purpose |
| --- | --- |
| [`docs/MVP-SOCIAL-CONTENT.md`](./docs/MVP-SOCIAL-CONTENT.md) | Locked product + CPU/Kompact narrative |
| [`docs/SUBMISSION.md`](./docs/SUBMISSION.md) | Paste-ready Phase 1 portal text |
| [`docs/DEMO-SCRIPT.md`](./docs/DEMO-SCRIPT.md) | 2–3 min judge demo script |
| [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) | Current social MVP architecture |
| [`docs/EXPERT-REVIEW-PROMPT.md`](./docs/EXPERT-REVIEW-PROMPT.md) | Paste-ready external review prompt |
| [`docs/EXPERT-REVIEW-2026-09-17.md`](./docs/EXPERT-REVIEW-2026-09-17.md) | Blunt expert review + P0/P1 |
| [`docs/PHASE1-ANALYSIS.md`](./docs/PHASE1-ANALYSIS.md) | Earlier brainstorm / option matrix (historical) |

## License

MIT
