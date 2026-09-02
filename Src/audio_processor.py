"""
audio_processor.py

Utilities for validating, loading, and standardizing audio/video input
before it is sent to the speech-to-text pipeline.
"""

import os
import subprocess
import tempfile

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v"}


def validate_file(path: str):
    """Check whether a file exists and has a supported extension.

    Returns:
        (bool, str): (is_valid, message)
    """
    if not os.path.exists(path):
        return False, f"File not found: {path}"

    ext = os.path.splitext(path)[1].lower()
    if ext in SUPPORTED_AUDIO_EXTENSIONS or ext in SUPPORTED_VIDEO_EXTENSIONS:
        return True, "OK"
    return False, f"Unsupported file extension: {ext}"


def is_video(path: str) -> bool:
    return os.path.splitext(path)[1].lower() in SUPPORTED_VIDEO_EXTENSIONS


def convert_to_wav(input_path: str, output_path: str | None = None,
                    sample_rate: int = 16000) -> str:
    """Convert an audio or video file to 16kHz mono WAV using FFmpeg.

    This standardization step is required (or strongly recommended) by
    most speech-recognition models.

    Args:
        input_path: Path to the source audio/video file.
        output_path: Where to write the WAV file. Defaults to a temp file.
        sample_rate: Target sample rate in Hz.

    Returns:
        Path to the generated WAV file.
    """
    valid, msg = validate_file(input_path)
    if not valid:
        raise ValueError(msg)

    if output_path is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        output_path = tmp.name
        tmp.close()

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",              # mono
        "-ar", str(sample_rate), # sample rate
        "-vn",                    # drop video stream if present
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg conversion failed:\n{result.stderr}")

    return output_path


def get_audio_duration(path: str) -> float:
    """Return duration of an audio/video file in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed:\n{result.stderr}")
    return float(result.stdout.strip())
