# Expert review — 2026-09-17 (IST)

Reviewer: Grok (executor pass)  
Repo: https://github.com/mmmiitr/kompact-build-next-2026  
Prompt used: `docs/EXPERT-REVIEW-PROMPT.md`  
Baseline commit reviewed conceptually: `35d3685` (Phase 1 Social Content Helper MVP)  
Product lock: Social Content Helper (not GazetteApply; not Kabootri uploader)

---

## 1. Executive blunt take

This is a **real, runnable Phase 1 skeleton** — FastAPI, static UI, MOCK path, OpenAI-compatible client — not vapor. That is the good news.

The bad news: as shipped at `35d3685`, the video upload is mostly **theater**. The model (and MOCK) see filename + coarse duration (+ size). A judge who opens `app/main.py` will correctly ask: *why upload a video at all?* Without a crisp honesty line (“metadata-first; transcript later”) and richer probe meta, this reads as a **caption bot with an upload button**. Differentiation vs “paste a prompt into ChatGPT” is thin.

Demo path was incomplete: no sample clip, no one-command smoke, dotenv not auto-loaded, LLM JSON parse fragile, UI missing copy-to-clipboard (creators live on paste), submission checklist thin, ARCHITECTURE still light vs social MVP. Kompact/CPU story is **honest if understated** — env swap is real — but it does not rescue a shallow demo.

**Keep**, with P0/P1 landed before portal submit. Do not pivot product this late. Do not invent vision/Whisper overnight; **own the metadata-first claim** and make the demo airtight.

---

## 2. Scores (1–5)

| Rubric | Score | Notes |
| --- | --- | --- |
| Phase-1 credibility | **3.5** | Code runs; MOCK works; shippable before 2026-09-18. Gaps: smoke script, dotenv, judge checklist. |
| Kompact / CPU honesty | **4** | No fake Kompact SDK. `BASE_URL` swap is credible. Caption drafts fit CPU-first economics. Don’t overclaim multimodal on CPU. |
| Demo clarity | **2.5** → target **4** after P0/P1 | UI exists but copy/meta/MOCK clarity + smoke/demo script were missing at baseline. |
| Competitive differentiation | **2.5** | Highest risk. Without honesty + richer meta + roadmap, looks like caption spam. Tool-not-uploader is a real but soft differentiator. |
| Security & hygiene | **3.5** | Temp file cleanup, 80MB cap, health hides secrets. No auth (fine for demo). Upload still accepts arbitrary bytes labeled video. |
| Top-20 vs reject | **3** | Credible keep if demo + docs tightened; reject risk if judges feel “upload theater.” |

---

## 3. Findings (verified against tree at baseline)

### Critical / high

1. **Video mostly unused** — `probe_duration` only; LLM user prompt used filename/duration/size. Width/height/codec unused. Strong “caption bot + upload theater” risk.
2. **No sample clip / one-command demo** — judges must bring their own file; friction kills.
3. **dotenv not auto-loaded** — `.env.example` exists; README told users to `export $(grep …)`; easy footgun.
4. **LLM JSON parsing fragile** — fence strip + `json.loads` only; no `response_format: json_object`; no object recovery.
5. **UI: no copy buttons** — publish packs that can’t be pasted are half a product.
6. **Submission/demo checklist thin** — `SUBMISSION.md` had a 4-bullet demo note; insufficient for judges.
7. **ARCHITECTURE.md thin** — correct direction but under-specified vs social MVP (probe, MOCK, env boundary).

### Medium

8. MOCK badge easy to miss; no video meta panel in UI.
9. README understated metadata-first honesty and Kabootri non-goal (present but buryable).
10. No Whisper/transcript — fine for Phase 1 **if said out loud**; fatal if implied as “understands your video.”

---

## 4. Prioritized fixes

### P0 — before portal / judge demo

| # | Fix |
| --- | --- |
| P0.1 | Auto-load dotenv in `app/main.py` when `python-dotenv` present; add to `requirements.txt` |
| P0.2 | Enrich ffprobe meta: duration, width, height, codec; pass into MOCK + LLM prompts; show in UI |
| P0.3 | LLM: request `response_format: json_object` when possible; safer JSON extract/recovery; retry without format on 400/422 |
| P0.4 | UI: copy buttons (title/captions/hashtags/description/JSON); video meta strip; loud MOCK badge |
| P0.5 | `scripts/demo_smoke.sh` — health + publish-pack with ffmpeg lavfi sample (or clear skip) |
| P0.6 | `docs/DEMO-SCRIPT.md` 2–3 min judge script + checklist |
| P0.7 | Tighten `SUBMISSION.md` + `README.md`: metadata-first honesty; Whisper/transcript roadmap; not Kabootri uploader |

### P1 — same week credibility

| # | Fix |
| --- | --- |
| P1.1 | Update `ARCHITECTURE.md` to match social MVP (probe → MOCK/LLM → pack; Phase 2 env swap) |
| P1.2 | Expert-review prompt + this review checked into `docs/` for Madan / external reviewers |
| P1.3 | Health endpoint echoes `ffprobe` availability + version |

### P2 — Phase 2 / later (do not fake in Phase 1)

| # | Fix |
| --- | --- |
| P2.1 | Optional Whisper / local transcript → feed LLM (still no auto-post) |
| P2.2 | Frame/thumbnail heuristics for trim suggestions |
| P2.3 | Multi-platform caption length presets (YT Shorts vs IG vs X) |
| P2.4 | Point `BASE_URL` at Kompact CPU when finalist runtime exists — **same schema** |

---

## 5. Keep / kill

**KEEP** — ship Social Content Helper; do not reopen GazetteApply this close to 2026-09-18.

Rationale: runnable MVP + honest Kompact env-swap story + clear non-uploader boundary. Kill only if Madan cannot tell the metadata-first story without blushing; then the product is dishonest, not merely thin.

---

## 6. Top-20 vs reject (signals only — no prize predictions)

**Helps Top-20 consideration**

- 90-second demo that works cold (smoke script + MOCK)
- Explicit metadata-first claim + visible probe meta
- Copy-to-clipboard creator UX
- Clean Kompact CPU narrative without fake integration
- Portal text that matches the repo

**Invite reject / ignore**

- Implying the model “watched” the video
- Broken clone→run path
- Confusing this with a social poster / Kabootri client
- Empty or mismatched submission vs README
- Overclaiming prizes, clients, or production deploy

---

## 7. Remediation status (same-day push)

P0.1–P0.7 and P1.1–P1.3 are incorporated in the follow-up commit on `main` that adds this file. Re-score demo clarity after verifying `./scripts/demo_smoke.sh` and a 2-minute UI take.

**Remaining risks after remediation**

- Still no transcript/vision — differentiation remains modest; honesty is the shield.
- Compat endpoints that reject `response_format` are handled via retry, but exotic gateways may still return prose.
- Smoke depends on `ffmpeg` for a real sample; without it, health-only path is documented.
- Madan must still submit on the ZIROH portal personally.

