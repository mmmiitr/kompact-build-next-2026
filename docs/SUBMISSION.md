# Phase 1 submission draft — Madan Meena

**Paste-ready text for the ZIROH / Kompact Build Next 2026 portal.**  
Deadline: **2026-09-18**. Madan registers and submits on the portal (agent does not click apply).

Portal: follow links from https://www.ziroh.com/hackathon (exact form fields may vary — adapt labels below).

Do **not** invent prize outcomes, Top-20 guarantees, or client production claims.

---

## Project title

Social Content Helper — publish-ready packs from short video + prompt

## Team

- Madan Meena (solo) — India, working professional
- GitHub: https://github.com/mmmiitr
- Repo: https://github.com/mmmiitr/kompact-build-next-2026

## One-line pitch

Creators upload a short video and a prompt; the app returns a publish-ready pack — title, captions, hashtags, description, and trim suggestions — via an OpenAI-compatible API that can later point at Kompact CPU runtime.

## Problem

Short-form creators and small Indian businesses spend disproportionate time rewriting titles, captions, and hashtags for each platform. Most “AI social” tools either auto-post (risky, out of scope) or require GPU-heavy video understanding before any useful copy appears. We need a **fast, cheap draft loop** that works with ordinary inference endpoints.

## Solution (what we built)

A minimal FastAPI + static UI MVP:

1. Upload short video + creative prompt.
2. Read lightweight video metadata (duration via `ffprobe` when available).
3. Generate a structured **publish pack** with an OpenAI-compatible chat client (`BASE_URL` / `API_KEY` / `MODEL`).
4. If no API key is set, return a deterministic **MOCK** pack clearly labeled — so judges can run the demo offline.

This is a **content helper**, not a social uploader (not Kabootri / not auto-post).

## Real-world impact

- Speeds caption/hashtag drafting for indie creators, educators, and SME marketers in India.
- Encourages iteration without locking the stack to one cloud GPU vendor.
- Keeps human review in the loop: the tool drafts; the creator publishes.

## Sustainable / CPU-first / Kompact path

Phase 1 uses any OpenAI-compatible endpoint. Phase 2 (finalist runtime) story: swap `BASE_URL` to Kompact CPU inference — **same prompts and JSON schema**. Caption generation is a narrow, high-frequency workload where CPU-first cost and edge/cloud flexibility matter more than frontier multimodal models.

## How to run (for reviewers)

```bash
git clone https://github.com/mmmiitr/kompact-build-next-2026.git
cd kompact-build-next-2026
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Optional LLM:
# cp .env.example .env  # set BASE_URL, API_KEY, MODEL
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://127.0.0.1:8000 — upload a short clip, enter a prompt, generate pack.  
With empty `API_KEY`, response `mode` is `MOCK`.

Health check: `GET /health`  
API: `POST /api/publish-pack` (multipart: `video`, `prompt`)

## Tech stack

Python 3 · FastAPI · uvicorn · httpx · optional ffprobe · static HTML UI

## Demo notes (2–3 min video checklist)

1. Show empty `API_KEY` → MOCK pack labeled.
2. (Optional) Set key → LLM pack.
3. Show JSON fields: title, captions, hashtags, description, trim suggestions.
4. Point to env swap for Kompact later.

## Links

- Hackathon: https://www.ziroh.com/hackathon
- Repository: https://github.com/mmmiitr/kompact-build-next-2026
- Product note: `docs/MVP-SOCIAL-CONTENT.md`

## Eligibility reminder (self-check)

India-based working professional; team size 1; Phase 1 online project submission only.
