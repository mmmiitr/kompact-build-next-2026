# Architecture — Phase 1 Social Content Helper

Supersedes the earlier GazetteApply draft for the **shipped** Phase 1 product.
Historical option analysis remains in `PHASE1-ANALYSIS.md`.

```
User (browser)
   │  multipart video + prompt
   ▼
Static UI (app/static/index.html)
   │  POST /api/publish-pack
   ▼
FastAPI (app/main.py)
   ├─ temp store upload
   ├─ duration: ffprobe | size stub
   ├─ API_KEY empty? → deterministic MOCK pack
   └─ else → OpenAI-compatible POST {BASE_URL}/chat/completions
                → parse JSON → PublishPack
```

## Runtime swap (Phase 2)

Only env changes:

```
BASE_URL=<kompact-or-other-openai-compat>
API_KEY=<token>
MODEL=<model-id>
```

Application code and response schema stay the same.
