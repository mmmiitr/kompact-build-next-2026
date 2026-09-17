# Expert review prompt — paste-ready

Copy everything below the line into Grok Expert / any technical reviewer.

---

## Context

You are reviewing a **Phase 1 hackathon MVP** for ZIROH LABS Build Next 2026 / Kompact AI.

| Field | Value |
| --- | --- |
| Repo | https://github.com/mmmiitr/kompact-build-next-2026 |
| Product (LOCKED) | Social Content Helper — upload short video + prompt → publish-ready pack (title, captions, hashtags, description, trim suggestions) |
| Phase 1 deadline | **2026-09-18** |
| Tracking | `krantikaridev/self` #66 |
| Team | Madan Meena (solo) |
| Not in scope | Kabootri / any social **upload** or auto-post client; prize outcome claims |

**Honest Phase 1 claim:** metadata-first (filename + ffprobe meta + creator prompt). Not full multimodal video understanding. Empty `API_KEY` → labeled MOCK packs for offline demo. OpenAI-compatible client so Phase 2 can swap `BASE_URL` to Kompact CPU runtime.

## Files to read (in order)

1. `README.md` — quick start + honesty
2. `docs/MVP-SOCIAL-CONTENT.md` — product lock + CPU/Kompact narrative
3. `app/main.py` — FastAPI, probe, MOCK/LLM paths
4. `app/static/index.html` — upload UI
5. `docs/SUBMISSION.md` — portal paste draft
6. `docs/ARCHITECTURE.md` — current architecture
7. `docs/DEMO-SCRIPT.md` — 2–3 min judge script (if present)
8. `scripts/demo_smoke.sh` — one-command smoke (if present)

Optional historical: `docs/PHASE1-ANALYSIS.md` (brainstorm; superseded by social MVP lock).

## Evaluation rubric

Score each 1–5 and justify with file/line evidence. Be blunt.

### 1. Phase-1 credibility
Can a judge clone, run, and see a coherent demo before the deadline? Is the MVP real code vs vapor? Are claims matched by the tree?

### 2. Kompact / CPU narrative honesty
Is the “swap `BASE_URL` to Kompact CPU later” story credible and non-overclaimed? Does the workload fit CPU-first economics? Any GPU-theater or invented Kompact integration?

### 3. Demo clarity
Is the before→after obvious in ≤3 minutes? MOCK vs LLM labeling? One-command or checklist path for reviewers?

### 4. Competitive differentiation
Vs caption generators / CapCut templates / ChatGPT alone: what is distinct? Risk of looking like “upload theater + caption bot”?

### 5. Security & hygiene
Secrets handling, upload size limits, temp file cleanup, no auto-post credentials, env example hygiene.

### 6. Top-20 vs reject signals
**What would make this Top-20 material** (concrete, achievable before/just after Phase 1 — do not invent prize outcomes).  
**What would get this rejected** (red flags visible today).

## Deliverable format (required)

1. **Executive blunt take** (5–8 sentences): keep / kill / pivot?
2. **Scores** table for the six rubric items.
3. **Prioritized fixes**
   - **P0** — must fix before portal submit / judge demo
   - **P1** — strongly improve credibility this week
   - **P2** — Phase 2 / nice-to-have
4. **Keep / kill recommendation** with one-line rationale.
5. **Do not** invent prize placements, Top-20 guarantees, client logos, or production deployments that are not in the repo.

Review the **current tree as of the commit you are given**; cite paths.
