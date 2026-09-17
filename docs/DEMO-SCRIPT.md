# Demo script — 2–3 minutes (judges / reviewers)

**Goal:** Show a real, honest Phase 1 loop: upload → publish pack → copy fields. No auto-post. No prize claims.

## Prep (30–60 s before recording)

```bash
cd kompact-build-next-2026
source .venv/bin/activate   # or create venv + pip install -r requirements.txt
# Leave API_KEY empty for MOCK (recommended first take)
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Optional one-shot smoke (separate terminal):

```bash
START_SERVER=0 ./scripts/demo_smoke.sh   # server already up
# or: START_SERVER=1 ./scripts/demo_smoke.sh
```

Have a short clip ready (any 5–30 s phone video), or use the ffmpeg sample from the smoke script.

## Script (≈150–180 s)

| Time | Say / show |
| --- | --- |
| 0:00–0:20 | “Social Content Helper for Build Next 2026. Creators upload a short video and a prompt; we return a publish-ready pack — title, captions, hashtags, description, trim suggestions. This is a **content helper**, not a Kabootri or Instagram uploader.” |
| 0:20–0:40 | Open http://127.0.0.1:8000. Point at the honesty line: **metadata-first Phase 1** (filename + ffprobe + prompt), not Whisper/vision yet. |
| 0:40–1:10 | Upload clip. Prompt example: *“30s tip for indie founders shipping on CPU budgets — India creators.”* Click **Generate publish pack**. |
| 1:10–1:40 | Show **MOCK** badge (or **LLM** if key set). Expand video meta (duration / resolution / codec when ffprobe present). Scroll title → captions → hashtags → description → trim suggestions. |
| 1:40–2:10 | Click **Copy** on hashtags and a caption. “Creator pastes into their own app — we never post.” |
| 2:10–2:40 | Mention: empty `API_KEY` → offline MOCK; with key → OpenAI-compatible LLM; Phase 2 story is **env swap** `BASE_URL` → Kompact CPU — same schema. Roadmap: transcript/Whisper later, still no auto-post. |
| 2:40–3:00 | Point to repo + `docs/SUBMISSION.md`. Stop. Do not claim Top-20 or prizes. |

## Checklist (judge-facing)

- [ ] Clone + `pip install -r requirements.txt` works
- [ ] `GET /health` returns `ok: true`
- [ ] Empty `API_KEY` → `mode: MOCK` clearly labeled in UI
- [ ] ffprobe installed → duration/width/height/codec in `video` meta (else stub duration noted)
- [ ] Copy buttons work for title / captions / hashtags / description
- [ ] Stated clearly: not a social uploader; metadata-first Phase 1

## Fixture prompts (same screenshot for two reviewers)

1. `30s tip for indie founders shipping on CPU budgets — India creators.`
2. `Hook for a Jaipur street-food reel aimed at weekend tourists.`

MOCK title is deterministic from filename + prompt hash. Use the same clip filename if comparing screenshots.

## Optional second take (LLM)

```bash
cp .env.example .env   # set API_KEY, BASE_URL, MODEL
# python-dotenv loads .env automatically when installed
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Show badge flip MOCK → LLM; same UI fields.
