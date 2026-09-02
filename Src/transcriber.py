"""
transcriber.py

Wraps ASR backends (Faster-Whisper preferred, OpenAI Whisper as fallback)
behind a single simple interface: transcribe(audio_path) -> str.
"""

from functools import lru_cache


@lru_cache(maxsize=1)
def _load_faster_whisper(model_size: str = "base"):
    from faster_whisper import WhisperModel
    return WhisperModel(model_size, device="cpu", compute_type="int8")


@lru_cache(maxsize=1)
def _load_openai_whisper(model_size: str = "base"):
    import whisper
    return whisper.load_model(model_size)


def transcribe_faster_whisper(audio_path: str, model_size: str = "base") -> dict:
    """Transcribe audio using Faster-Whisper (CTranslate2-optimized Whisper).

    Returns a dict with keys: text, language, segments, model.
    """
    model = _load_faster_whisper(model_size)
    segments, info = model.transcribe(audio_path, beam_size=1, vad_filter=True)
    segments = list(segments)
    text = " ".join(seg.text.strip() for seg in segments).strip()

    return {
        "model": f"faster-whisper-{model_size}",
        "text": text,
        "language": info.language,
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text.strip()}
            for seg in segments
        ],
    }


def transcribe_whisper(audio_path: str, model_size: str = "base") -> dict:
    """Transcribe audio using the original OpenAI Whisper implementation."""
    model = _load_openai_whisper(model_size)
    result = model.transcribe(audio_path)

    return {
        "model": f"whisper-{model_size}",
        "text": result.get("text", "").strip(),
        "language": result.get("language"),
        "segments": [
            {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
            for s in result.get("segments", [])
        ],
    }


def transcribe(audio_path: str, backend: str = "faster-whisper",
                model_size: str = "base") -> dict:
    """Single entry point used by the app and scripts.

    Args:
        audio_path: Path to a 16kHz mono WAV file (see audio_processor.convert_to_wav).
        backend: "faster-whisper" (default, faster/lighter) or "whisper".
        model_size: e.g. "tiny", "base", "small", "medium".
    """
    if backend == "faster-whisper":
        return transcribe_faster_whisper(audio_path, model_size)
    elif backend == "whisper":
        return transcribe_whisper(audio_path, model_size)
    else:
        raise ValueError(f"Unknown backend: {backend}")
