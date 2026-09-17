"""
Kompact Social Content Helper — Phase 1 MVP

Upload a short video + prompt → publish-ready pack
(title, captions, hashtags, description, trim suggestions).

OpenAI-compatible via BASE_URL / API_KEY / MODEL.
Empty API_KEY → deterministic MOCK pack (no network spend).

Honest Phase 1 scope: metadata-first (filename + ffprobe meta + prompt).
No transcript / Whisper / vision in this build — roadmap later.
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

# Load .env when python-dotenv is installed (optional; no hard dep crash)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(
    title="Kompact Social Content Helper",
    description=(
        "Upload short video + prompt → publish-ready social pack "
        "(metadata-first Phase 1; not a social uploader)"
    ),
    version="0.1.1",
)


class VideoMeta(BaseModel):
    filename: str
    size_bytes: int
    content_type: str | None = None
    duration_seconds: float | None = None
    duration_source: str = "stub"
    width: int | None = None
    height: int | None = None
    codec: str | None = None
    probe_source: str = "stub"


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


def probe_video(path: Path) -> dict[str, Any]:
    """
    Enrich video metadata via ffprobe when available.

    Returns dict with duration_seconds, duration_source, width, height,
    codec, probe_source. Falls back to size-based duration stub.
    """
    out: dict[str, Any] = {
        "duration_seconds": None,
        "duration_source": "stub",
        "width": None,
        "height": None,
        "codec": None,
        "probe_source": "stub",
    }

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
                    "-show_streams",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                fmt = data.get("format") or {}
                dur = fmt.get("duration")
                if dur is not None:
                    out["duration_seconds"] = float(dur)
                    out["duration_source"] = "ffprobe"
                    out["probe_source"] = "ffprobe"

                streams = data.get("streams") or []
                vstream = next(
                    (s for s in streams if s.get("codec_type") == "video"),
                    None,
                )
                if vstream:
                    w = vstream.get("width")
                    h = vstream.get("height")
                    if w is not None:
                        out["width"] = int(w)
                    if h is not None:
                        out["height"] = int(h)
                    codec = vstream.get("codec_name")
                    if codec:
                        out["codec"] = str(codec)
                    out["probe_source"] = "ffprobe"
                    # Some containers put duration only on stream
                    if out["duration_seconds"] is None:
                        sd = vstream.get("duration")
                        if sd is not None:
                            out["duration_seconds"] = float(sd)
                            out["duration_source"] = "ffprobe"
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError, TypeError):
            pass

    if out["duration_seconds"] is None:
        # Stub: rough estimate ~1 MB/s for short clips (demo only)
        size = path.stat().st_size
        stub = max(3.0, min(90.0, size / (1024 * 1024)))
        out["duration_seconds"] = round(stub, 1)
        out["duration_source"] = "stub"

    return out


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
    for tok in re.findall(r"[A-Za-z]{3,}", prompt)[:5]:
        tags.append(tok.capitalize())
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

    res_bits = []
    if meta.width and meta.height:
        res_bits.append(f"{meta.width}x{meta.height}")
    if meta.codec:
        res_bits.append(meta.codec)
    res_note = f" ({', '.join(res_bits)})" if res_bits else ""

    return PublishPack(
        mode="MOCK",
        title=title,
        captions=captions,
        hashtags=[f"#{h}" for h in hashtags[:12]],
        description=(
            f"[MOCK] Publish pack for «{stem}»{res_note}.\n\n"
            f"Creator prompt: {prompt or '(none)'}\n\n"
            f"Duration ~{dur}s (source={meta.duration_source}). "
            "Generated without an API key for offline demo. "
            "Set API_KEY + BASE_URL + MODEL for LLM-backed packs. "
            "Phase 1 is metadata-first (not full video understanding). "
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


def _extract_json_object(text: str) -> dict[str, Any]:
    """Parse JSON from LLM text; strip fences; recover first {...} if needed."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    # Recover first JSON object substring
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(cleaned[start : end + 1])
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError("no JSON object found", cleaned, 0)


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
        "Be concrete and India-creator friendly. No markdown fences. "
        "You only receive filename + lightweight probe metadata + the creator "
        "prompt — not a transcript or frame analysis. Do not invent spoken "
        "dialogue; ground copy in the prompt and metadata."
    )
    res = (
        f"{meta.width}x{meta.height}"
        if meta.width and meta.height
        else "unknown"
    )
    user = (
        f"Video filename: {filename}\n"
        f"Duration seconds: {meta.duration_seconds} "
        f"(source={meta.duration_source})\n"
        f"Resolution: {res}\n"
        f"Codec: {meta.codec or 'unknown'}\n"
        f"Probe: {meta.probe_source}\n"
        f"Size bytes: {meta.size_bytes}\n"
        f"Creator prompt: {prompt or '(none — invent a useful angle)'}\n"
        "Produce a publish-ready pack from metadata + prompt only."
    )

    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }
    # Prefer JSON mode when the endpoint supports it (OpenAI + many compat)
    body["response_format"] = {"type": "json_object"}

    async def _post(payload: dict[str, Any]) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            # Some OpenAI-compat servers reject response_format — retry without
            if resp.status_code in (400, 422) and "response_format" in payload:
                retry = {k: v for k, v in payload.items() if k != "response_format"}
                resp = await client.post(url, headers=headers, json=retry)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    try:
        content = await _post(body)
    except Exception as exc:  # noqa: BLE001 — surface as HTTP for demo UX
        raise HTTPException(
            status_code=502,
            detail=f"LLM call failed ({type(exc).__name__}): {exc}",
        ) from exc

    try:
        data = _extract_json_object(content)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM returned non-JSON: {content[:400]}",
        ) from exc

    return PublishPack(
        mode="LLM",
        title=str(data.get("title", "Untitled")),
        captions=[str(c) for c in data.get("captions", [])][:5] or ["(no caption)"],
        hashtags=[
            str(h) if str(h).startswith("#") else f"#{h}"
            for h in data.get("hashtags", [])
        ][:15],
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
        "ffprobe": bool(shutil.which("ffprobe")),
        "version": app.version,
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
        probed = probe_video(tmp_path)
        meta = VideoMeta(
            filename=video.filename,
            size_bytes=len(raw),
            content_type=video.content_type,
            duration_seconds=probed["duration_seconds"],
            duration_source=probed["duration_source"],
            width=probed["width"],
            height=probed["height"],
            codec=probed["codec"],
            probe_source=probed["probe_source"],
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
