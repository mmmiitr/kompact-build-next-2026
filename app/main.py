"""
Kompact Social Content Helper — Phase 1 MVP

Upload a short video + prompt → publish-ready pack
(title, captions, hashtags, description, trim suggestions).

OpenAI-compatible via BASE_URL / API_KEY / MODEL.
Empty API_KEY → deterministic MOCK pack (no network spend).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Kompact Social Content Helper",
    description="Upload short video + prompt → publish-ready social pack",
    version="0.1.0",
)


class VideoMeta(BaseModel):
    filename: str
    size_bytes: int
    content_type: str | None = None
    duration_seconds: float | None = None
    duration_source: str = "stub"


class PublishPack(BaseModel):
    mode: str = Field(description="MOCK or LLM")
    title: str
    captions: list[str]
    hashtags: list[str]
    description: str
    trim_suggestions: list[dict[str, Any]]
    video: VideoMeta
    prompt: str
    model: str | None = None


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def probe_duration(path: Path) -> tuple[float | None, str]:
    """Return (seconds, source). Prefer ffprobe; else stub from file size."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        try:
            result = subprocess.run(
                [
                    ffprobe,
                    "-v",
                    "quiet",
                    "-print_format",
                    "json",
                    "-show_format",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                dur = data.get("format", {}).get("duration")
                if dur is not None:
                    return float(dur), "ffprobe"
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError):
            pass

    # Stub: rough estimate ~1 MB/s for short clips (demo only)
    size = path.stat().st_size
    stub = max(3.0, min(90.0, size / (1024 * 1024)))
    return round(stub, 1), "stub"


def mock_pack(filename: str, prompt: str, meta: VideoMeta) -> PublishPack:
    """Deterministic pack from filename + prompt hash — no API spend."""
    stem = Path(filename).stem.replace("_", " ").replace("-", " ").strip() or "clip"
    seed = hashlib.sha256(f"{filename}|{prompt}".encode()).hexdigest()
    n = int(seed[:8], 16)

    topic = prompt.strip()[:80] if prompt.strip() else stem
    title = f"[MOCK] {topic[:60]} — quick take #{n % 97}"
    captions = [
        f"[MOCK] Hook: {topic} — watch till the end 👀",
        f"[MOCK] {stem}: what creators miss about this",
        f"[MOCK] Save this if you're building in public",
    ]
    tags = [
        "ContentCreator",
        "ShortForm",
        "IndiaCreators",
        "SustainableAI",
        "KompactReady",
    ]
    # Mix in prompt tokens as hashtags
    for tok in re.findall(r"[A-Za-z]{3,}", prompt)[:5]:
        tags.append(tok.capitalize())
    # Dedupe preserve order
    seen: set[str] = set()
    hashtags = []
    for t in tags:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            hashtags.append(t)

    dur = meta.duration_seconds or 15.0
    mid = max(2.0, dur * 0.35)
    end_cut = max(mid + 1.0, dur * 0.85)

    return PublishPack(
        mode="MOCK",
        title=title,
        captions=captions,
        hashtags=[f"#{h}" for h in hashtags[:12]],
        description=(
            f"[MOCK] Publish pack for «{stem}».\n\n"
            f"Creator prompt: {prompt or '(none)'}\n\n"
            "Generated without an API key for offline demo. "
            "Set API_KEY + BASE_URL + MODEL for LLM-backed packs. "
            "Swap BASE_URL later to Kompact CPU runtime — same client."
        ),
        trim_suggestions=[
            {
                "start_sec": 0.0,
                "end_sec": round(min(3.0, dur * 0.2), 1),
                "reason": "Keep a strong hook in the first 2–3s",
            },
            {
                "start_sec": round(mid, 1),
                "end_sec": round(min(mid + 5.0, dur), 1),
                "reason": "Peak moment / demo beat for the middle cut",
            },
            {
                "start_sec": round(max(0.0, end_cut - 4.0), 1),
                "end_sec": round(min(dur, end_cut), 1),
                "reason": "CTA / loop-friendly ending",
            },
        ],
        video=meta,
        prompt=prompt,
        model=None,
    )


async def llm_pack(filename: str, prompt: str, meta: VideoMeta) -> PublishPack:
    base = _env("BASE_URL", "https://api.openai.com/v1").rstrip("/")
    api_key = _env("API_KEY")
    model = _env("MODEL", "gpt-4o-mini")

    system = (
        "You are a social media content strategist for short-form video "
        "(Reels/Shorts/TikTok). Return ONLY valid JSON with keys: "
        "title (string), captions (array of 3 strings), hashtags (array of "
        "8-12 strings starting with #), description (string, 2-4 sentences), "
        "trim_suggestions (array of objects with start_sec, end_sec, reason). "
        "Be concrete and India-creator friendly. No markdown fences."
    )
    user = (
        f"Video filename: {filename}\n"
        f"Duration seconds: {meta.duration_seconds} (source={meta.duration_source})\n"
        f"Size bytes: {meta.size_bytes}\n"
        f"Creator prompt: {prompt or '(none — invent a useful angle)'}\n"
        "Produce a publish-ready pack."
    )

    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            payload = resp.json()
            content = payload["choices"][0]["message"]["content"]
    except Exception as exc:  # noqa: BLE001 — surface as HTTP for demo UX
        raise HTTPException(
            status_code=502,
            detail=f"LLM call failed ({type(exc).__name__}): {exc}",
        ) from exc

    # Strip optional fences
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM returned non-JSON: {text[:400]}",
        ) from exc

    return PublishPack(
        mode="LLM",
        title=str(data.get("title", "Untitled")),
        captions=[str(c) for c in data.get("captions", [])][:5] or ["(no caption)"],
        hashtags=[str(h) if str(h).startswith("#") else f"#{h}" for h in data.get("hashtags", [])][
            :15
        ],
        description=str(data.get("description", "")),
        trim_suggestions=list(data.get("trim_suggestions", []))[:5],
        video=meta,
        prompt=prompt,
        model=model,
    )


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "ok": True,
        "has_api_key": bool(_env("API_KEY")),
        "base_url": _env("BASE_URL", "https://api.openai.com/v1"),
        "model": _env("MODEL", "gpt-4o-mini"),
    }


@app.post("/api/publish-pack", response_model=PublishPack)
async def publish_pack(
    video: UploadFile = File(..., description="Short video file"),
    prompt: str = Form("", description="Creator intent / angle"),
) -> PublishPack:
    if not video.filename:
        raise HTTPException(status_code=400, detail="video filename required")

    suffix = Path(video.filename).suffix or ".bin"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = Path(tmp.name)
        raw = await video.read()
        if not raw:
            raise HTTPException(status_code=400, detail="empty video upload")
        if len(raw) > 80 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="video too large (max 80MB demo)")
        tmp.write(raw)

    try:
        duration, source = probe_duration(tmp_path)
        meta = VideoMeta(
            filename=video.filename,
            size_bytes=len(raw),
            content_type=video.content_type,
            duration_seconds=duration,
            duration_source=source,
        )

        if not _env("API_KEY"):
            return mock_pack(video.filename, prompt, meta)
        return await llm_pack(video.filename, prompt, meta)
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass


@app.get("/")
async def index() -> FileResponse:
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html missing")
    return FileResponse(index_path)


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
