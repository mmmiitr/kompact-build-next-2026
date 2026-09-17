# Architecture — Phase 1 Social Content Helper

Supersedes earlier GazetteApply / agentic drafts for the **shipped** Phase 1 product.
Historical option analysis remains in `PHASE1-ANALYSIS.md`.

## Honest scope

Phase 1 is **metadata-first**: filename + ffprobe fields (duration, width/height, codec when available) + creator prompt.
No Whisper transcript, no frame/vision model, no social posting (not Kabootri / not auto-post).

```
User (browser)
   │  multipart video + prompt
   ▼
Static UI (app/static/index.html)
   │  POST /api/publish-pack
   │  ← copy buttons for publish fields; MOCK/LLM badge; video meta strip
   ▼
FastAPI (app/main.py)
   ├─ load_dotenv() if python-dotenv installed
   ├─ temp store upload (≤80MB), delete after request
   ├─ probe_video(): ffprobe format+streams → duration, w×h, codec
   │                 else size-based duration stub
   ├─ API_KEY empty? → deterministic MOCK pack (labeled)
   └─ else → OpenAI-compatible POST {BASE_URL}/chat/completions
                response_format=json_object (retry without if rejected)
                → safer JSON extract → PublishPack
```

## Endpoints

| Method | Path | Role |
| --- | --- | --- |
| `GET` | `/` | Upload UI |
| `GET` | `/health` | Liveness; `has_api_key`, `base_url`, `model`, `ffprobe`, `version` (no secrets) |
| `POST` | `/api/publish-pack` | multipart `video` + `prompt` → `PublishPack` JSON |

## PublishPack shape

- `mode`: `MOCK` | `LLM`
- `title`, `captions[]`, `hashtags[]`, `description`
- `trim_suggestions[]` (`start_sec`, `end_sec`, `reason`)
- `video`: filename, size_bytes, content_type, duration_seconds, duration_source, width, height, codec, probe_source
- `prompt`, optional `model`

## Runtime swap (Phase 2 / Kompact)

Only env changes — application code and response schema stay the same:

```
BASE_URL=<kompact-or-other-openai-compat>
API_KEY=<token>
MODEL=<model-id>
```

Caption/hashtag drafting is a narrow, high-frequency workload suited to a **CPU-first** cost story once Kompact (or any compat) endpoint is available. Do not claim that integration ships in Phase 1.

## Demo / ops

- `scripts/demo_smoke.sh` — curl `/health` + `/api/publish-pack` with ffmpeg lavfi sample
- `docs/DEMO-SCRIPT.md` — 2–3 min judge script
- Empty `API_KEY` → offline MOCK (no network spend)

## Roadmap (not Phase 1)

- Optional Whisper / local transcript into the LLM prompt
- Better trim heuristics from audio/energy or thumbnails
- Still **no** auto-post to social networks
