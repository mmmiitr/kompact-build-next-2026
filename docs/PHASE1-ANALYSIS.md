# Kompact / ZIROH Build Next — Phase 1 analysis

Date: **2026-09-14** (IST)  
Deadline Phase 1: **2026-09-18** (~4 days)  
Prize: ₹7.5L (3 × ₹2.5L memorial awards)  
Finalists: Top 20 announced ~**2026-09-24**; Phase 2 event ~**2026-09-26**  
Team: 1–5; India students + working professionals; online; free  
URL: https://www.ziroh.com/hackathon  
Issue: krantikaridev/self#66

## What judges actually need in Phase 1

From public page + issue notes:

| Fact | Implication |
| --- | --- |
| Phase 1 = project submission until 18 Sep | Ship a **credible demo + write + writeup**, not a finished product |
| Top 20 get exclusive Kompact CPU runtime | Phase 1 must be **runtime-swappable** (OpenAI-compatible client) |
| Wanted: agents, RAG, predictive apps with real-world impact | Prefer one sharp vertical over a kitchen-sink agent |
| Sustainable / CPU-first branding | Narrative: **cost, edge, India deploy without GPU tax** |
| Runtime specs only for finalists | Do **not** block Phase 1 on their SDK |

## Madan fit (honest)

**Strengths to lean on**
- Spoken-defensible **fixed agentic workflow** (parse → tool stages → apply) + RAG Q&A (Maruti lock language)
- .NET / Azure / Docker / Copilot-agents delivery story (KPMG path)
- India enterprise + compliance domain intuition
- Can solo a small Python or .NET scaffold fast

**Weaknesses / risks**
- Solo + job hunt + Mercor sit competing for hours
- 4 calendar days; prize-competitive bar for Top 20 is unclear
- No Kompact docs yet — architecture must stay OpenAI-compatible
- “Predictive” apps are less practiced for Madan than RAG/agentic docs

## Option matrix

### Option A — GazetteApply Lite (RECOMMENDED)

**One-liner:** Fixed agentic pipeline that applies textual amendments to a source document and returns revised draft + highlight-diff; RAG for Q&A across versions.

| | |
| --- | --- |
| Why it wins | Matches ZIROH agent+RAG ask; Madan’s strongest interview story; easy demo video; CPU narrative (“amendment apply on cheap inference”) |
| Phase 1 demo | Synthetic e-Gazette-like HTML + 3 canned amendments; FastAPI/Next thin UI; OpenAI-compatible LLM behind env `BASE_URL` |
| Phase 2 hook | Swap `BASE_URL`/model to Kompact runtime; keep tools identical |
| Effort (solo) | Spec 2h · scaffold 6–8h · eval/demo 4–6h · writeup/video 3–4h → **~16–22h** |
| Top-20 odds | **Best of our options** if demo is crisp and writeup sells CPU-future |
| Kill criteria | If cannot finish apply+diff+RAG Q&A by Wed night IST → cut UI, keep CLI |

### Option B — India SME Policy Copilot (RAG-only)

**One-liner:** Retrieval over public India MSME / compliance PDFs with citation UI and eval set.

| | |
| --- | --- |
| Why | Simple, sustainable-AI story, less moving parts |
| Risk | Crowded “RAG chatbot” category; weaker differentiation vs agentic |
| Effort | **10–14h** |
| Odds | Medium — needs excellent eval + domain packaging |

### Option C — CPU-first Retail Demand Agent

**One-liner:** Predictive demand + agent that proposes restock actions; aligns with ZIROH retail messaging.

| | |
| --- | --- |
| Why | Predictive + agent checkbox |
| Risk | Needs data + forecasting credibility Madan doesn’t have on tape; easy to look toy |
| Effort | **20–28h** |
| Odds | Lower for us in 4 days |

### Option D — Kompact-ready OpenAI Gateway shim only

**One-liner:** Multi-tenant OpenAI-compatible proxy with routing, quotas, OpenTelemetry stubs.

| | |
| --- | --- |
| Why | Flatters their runtime story |
| Risk | Looks like infra without “real-world impact” app; weak Phase 1 story |
| Effort | **8–12h** |
| Odds | Low alone; could be a **module inside A** |

## Recommended plan (pending expert review)

1. **Lock Option A** unless expert review vetoes.
2. Phase 1 deliverables checklist:
   - Public repo (this) with README, architecture diagram, MIT
   - Working CLI or minimal web: `amend` + `ask` commands
   - 5–10 synthetic fixtures + golden outputs
   - 2–3 min screen recording
   - 1-page impact note: problem → agentic stages → CPU/Kompact swap path → India impact
3. Explicit **OpenAI-compatible** boundary in code (`OPENAI_BASE_URL`, `OPENAI_API_KEY`, `MODEL`).
4. Spoken lock for any Maruti mention in writeup: agentic workflow / PoC→product / not production while there — or **avoid Maruti brand** and say “inspired by compliance amendment pipelines.”
5. Timebox: if not demoable by **2026-09-17 20:00 IST**, ship reduced CLI-only and still submit; if still broken, **SKIP** with reason on #66 (better than garbage entry).

## Estimate vs calendar

| Window | Work |
| --- | --- |
| Mon 14 (today) | Analysis + placeholder (this doc) + expert review |
| Tue 15 | Spec freeze + scaffold + fixtures |
| Wed 16 | Core amend pipeline + RAG ask |
| Thu 17 | Eval, polish, video, writeup |
| Fri 18 | Submit before cutoff; buffer for portal pain |

**Total best-shot solo:** ~18–22 focused hours across 4 days.  
**With 1 teammate:** cut calendar risk; Madan remains solution owner.

## Submit / SKIP decision frame

Submit if: demo runs offline-ish, writeup clear, OpenAI-compat swap documented.  
SKIP if: <8h available before Thu, or only a README with no runnable path.

## Open questions for expert review

1. Confirm Option A vs B given 4-day solo constraint.
2. Python FastAPI vs .NET minimal API — which is faster for Madan this week?
3. Should Phase 1 avoid naming Maruti entirely?
4. Is a teammate available before Wed?
5. Exact Phase 1 submission portal fields (link not fully detailed on marketing page) — find form ASAP Tue.

## Sources

- https://www.ziroh.com/hackathon
- https://ziroh.com/ (Kompact positioning: CPU inference, RAG/agentic, OpenAI-compatible SDKs mentioned in search/FAQ snippets)
- self#66 body + comments


---

## Update 2026-09-14 evening — keep A + B open (Madan)

**Decision:** Do **not** lock a single option yet. Keep **A and B** both live. Brainstorm further. Create/implement **only after** settled + expert review. No rush — better a sharp Phase 1 than a half-baked Friday dump.

### A vs B side-by-side (deeper)

| Dimension | A GazetteApply Lite (agentic + RAG) | B India SME Policy Copilot (RAG-first) |
| --- | --- | --- |
| Core loop | parse → retrieve → apply → diff | retrieve → cite → answer |
| Demo wow | Visible before/after document | Solid Q&A with citations |
| Madan spoken defense | Strong (fixed agentic workflow) | Medium (domain RAG) |
| Build risk in 4 days | Higher (apply step is hard) | Lower |
| Crowd factor | Fewer “amendment agent” entries | Many “RAG chatbots” |
| Kompact Phase 2 story | Inference on apply + cheap models on parse | Inference on answer generation |
| Eval story | Golden amend fixtures + diff quality | Faithfulness / citation hit-rate |
| Failure mode | Apply invents text / breaks HTML | Generic answers / weak corpus |
| Cut-down path | CLI-only amend, drop web UI | PDF pack + CLI ask only |

**Hybrid AB (worth considering, still not locked):**  
Ship B’s RAG corpus + ask UI as the **floor**, and A’s amend pipeline as the **ceiling** behind a feature flag. Phase 1 writeup leads with whichever is more demoable by Thu. Shared OpenAI-compatible client either way.

### More options (brainstorm — none locked)

| ID | Name | One-liner | Why consider | Why maybe not |
| --- | --- | --- | --- | --- |
| A | GazetteApply Lite | Fixed agentic amendment + RAG | Best Madan fit | Apply quality risk |
| B | SME Policy Copilot | Cited RAG over public India policy PDFs | Fastest credible demo | Crowded category |
| C | Retail demand agent | Predict + propose restock | Matches ZIROH retail messaging | Weak data/cred for us |
| D | Gateway shim | OpenAI-compat proxy + OTel stubs | Flatters Kompact | Infra without impact |
| E | **Eval harness for CPU RAG** | Public benchmark + runner comparing “GPU-class” vs “CPU-budget” prompts/models via OpenAI-compat | Unique “sustainable AI” angle; judges may like measurement | Less “app”, more tooling |
| F | **Multilingual Bharat forms agent** | Agent fills/explains gov form fields from a PDF notice (Hindi+EN) | India impact; agentic | Scope creep / UX hard |
| G | **Contract redline assistant** | Diff two contract versions + risk bullets | Enterprise money story | Legal risk if overclaimed |
| H | **On-device meeting notes → actions** | Local-first summarizer + task extract | Edge/CPU narrative | Commodity |
| I | **AB hybrid** | B floor + A ceiling | De-risks calendar | Needs clear demo script so it doesn’t look unfocused |

### Brainstorm prompts for expert review (not answers yet)

1. Is Top-20 selection more **demo polish**, **problem novelty**, or **Kompact-readiness** narrative?
2. Should we avoid any Maruti/branded client language and use fully synthetic verticals?
3. Python FastAPI vs .NET minimal — which is less calendar risk for Madan this week?
4. Is Option E (eval harness) a stronger ZIROH fit than another chatbot, even if less flashy?
5. Solo vs add 1 teammate for writeup/video only?
6. Exact Phase 1 submission fields/portal — still unknown; find before locking scope.

### Settling criteria (use later — not today)

Lock only when **two** of these are true:
- Expert review picks a primary (A / B / I / other)
- Madan can defend the demo in 90 seconds without notes
- A runnable path fits remaining hours without killing Mercor/job queue

Until then: **notes only**. Placeholder repo stays analysis. No app code.

### Still open on #66
- Transfer repo `mmmiitr/kompact-build-next-2026` → `krantikaridev/` when convenient (cosmetic)
- Find submission portal details
