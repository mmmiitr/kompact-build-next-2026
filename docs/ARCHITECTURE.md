# Architecture (draft — not implemented)

```
User → CLI/Web → Orchestrator (fixed stages)
                      ├─ parse_amendment (LLM JSON)
                      ├─ retrieve (vector / keyword)
                      ├─ apply_patch (LLM + deterministic diff)
                      └─ answer_question (RAG)
LLM traffic → OpenAI-compatible client → {Ollama | Cloud | Kompact later}
```

Phase 1 implements stages + fixtures. Phase 2 only changes the client target.
