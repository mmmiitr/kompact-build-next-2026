# Expert review — HEAD pass (2026-09-17 IST)

Reviewer: Grok planning thread (this chat stays the review thread)  
Repo reviewed: https://github.com/mmmiitr/kompact-build-next-2026  
Commit: **`1fab761`** (2026-09-17T05:43Z)  
Not a rescore of `35d3685`. Earlier review: `docs/EXPERT-REVIEW-2026-09-17.md` in that repo.  
Tracking: `krantikaridev/self` #66  
Product lock: Social Content Helper (not GazetteApply; not Kabootri uploader)

Copy this file into the product repo as `docs/EXPERT-REVIEW-2026-09-17-HEAD.md` when applying the Cline plan.

---

## 1. Executive blunt take

**Keep and submit.** Do not kill. Do not pivot back to GazetteApply / SME RAG overnight.

The app is real code: FastAPI + static UI + MOCK path + OpenAI-compat client. A judge can clone, run MOCK, and see a pack. Honesty is loud (README, UI subtitle, MOCK badge, LLM system prompt).

What is not fixed: the video is still barely used. `probe_video()` reads duration / w×h / codec; MOCK trims are duration ratios; the model never sees pixels or audio. Acceptable if said out loud. Fatal if the portal pitch sounds like “the AI watches your reel.”

Category risk vs ZIROH’s page: they asked for agents, RAG, and predictive apps; this is one `chat/completions` call wrapped in an upload form. CPU/`BASE_URL` swap is honest and not overclaimed.

GitHub **About** still says “Phase 1 placeholder (analysis only)” — first thing a reviewer reads; contradicts README. Fix before paste.

---

## 2. Scores (HEAD `1fab761`)

| Rubric | Score | Evidence |
| --- | --- | --- |
| Phase-1 credibility | **4** | Runnable tree. Claims match code. Gaps: no tests, no demo recording, stale GitHub About, `docs/PHASE1-ANALYSIS.md` still reads like GazetteApply. |
| Kompact / CPU honesty | **4.5** | No fake SDK. Env = `BASE_URL` / `API_KEY` / `MODEL`. Docs say no live Kompact deploy. |
| Demo clarity | **4** | `docs/DEMO-SCRIPT.md` + smoke + MOCK badge + copy buttons. Smoke without ffmpeg is health-only. |
| Competitive differentiation | **2.5** | Structured pack + duration trims + human-paste. Video bytes discarded after probe. MOCK tags `#KompactReady` / `#SustainableAI` look canned. |
| Security & hygiene | **4** | `.env` gitignored; 80MB cap; temp unlink; health hides secrets. Residual: any bytes as video; incomplete MIT; unused `pydantic-settings`. |
| Top-20 vs reject | **3** | Submit-able. Not Top-20-shaped on category fit. No prize claim. |

---

## 3. Prioritized fixes

See `placement/notes/KOMPACT-CLINE-PLAN.md` for executor steps.

### P0 — before portal / judge demo
1. Change GitHub About (Madan-only in UI).
2. Banner `docs/PHASE1-ANALYSIS.md` SUPERSEDED.
3. Portal text = `docs/SUBMISSION.md` only. Not agent/RAG/watched-the-video.
4. Run `START_SERVER=1 ./scripts/demo_smoke.sh` on the demo machine.
5. Record 2–3 min take from `docs/DEMO-SCRIPT.md` (not in git).

### P1 — same-week code
1. Platform length hints in pack / LLM prompt.
2. Stop stuffing `#KompactReady` / `#SustainableAI` into every MOCK pack.
3. Reject obviously non-video uploads.
4. Two fixture prompts in DEMO-SCRIPT.
5. Full MIT body in LICENSE.
6. Drop unused `pydantic-settings`.
7. One sentence: narrow generation tool, not an agent loop.

### P2 — do not fake before Friday
Whisper / energy trims / live Kompact BASE_URL / Kabootri upload = out.

---

## 4. Keep / kill

**KEEP — submit Social Content Helper plus P0 hygiene.**

Rationale: runnable, honest, env-swappable. Thursday pivot to GazetteApply ships analysis again.

---

## 5. Top-20 vs reject signals (no prize prediction)

**Helps:** cold clone → MOCK; visible probe meta; copy buttons; env swap matched by code; portal paste matches HEAD.

**Bounces:** stale About; implied vision/Whisper/auto-post; calling this an agent/RAG/predictive system; two products in `docs/` with no banner; prize/client/Kompact-deployed claims.
