from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

from utils import ensure_dirs, timestamped_filename, OUTPUT_AUDIO_DIR

# Optional deps
try:
    import pyttsx3  # type: ignore
except Exception:  # pragma: no cover - optional
    pyttsx3 = None

try:
    from gtts import gTTS  # type: ignore
except Exception:  # pragma: no cover - optional
    gTTS = None

# Coqui TTS (optional, heavy dependency)
try:
    from TTS.api import TTS as CoquiTTS  # type: ignore
except Exception:  # pragma: no cover - optional
    CoquiTTS = None  # type: ignore


EngineName = Literal["pyttsx3", "gtts", "coqui"]


def tts_synthesize(
    text: str,
    engine: EngineName = "pyttsx3",
    language: str = "en",
    rate: Optional[int] = None,
    voice_id: Optional[str] = None,
    basename: str = "speech",
) -> Path:
    """Synthesize speech and return saved audio path.

    - pyttsx3: offline, outputs WAV
    - gTTS: online, outputs MP3
    - coqui: offline neural TTS (Coqui), outputs WAV (requires coqui TTS + torch)
    """
    ensure_dirs()
    text = text or ""

    if engine == "pyttsx3":
        if pyttsx3 is None:
            raise RuntimeError("pyttsx3 not installed")
        eng = pyttsx3.init()
        if rate is not None:
            eng.setProperty("rate", rate)
        if voice_id is not None:
            eng.setProperty("voice", voice_id)
        out_path = OUTPUT_AUDIO_DIR / (timestamped_filename(basename, "pyttsx3") + ".wav")
        eng.save_to_file(text, str(out_path))
        eng.runAndWait()
        return out_path

    elif engine == "gtts":
        if gTTS is None:
            raise RuntimeError("gTTS not installed")
        tts = gTTS(text=text, lang=language)
        out_path = OUTPUT_AUDIO_DIR / (timestamped_filename(basename, "gtts") + ".mp3")
        tts.save(str(out_path))
        return out_path

    elif engine == "coqui":
        if CoquiTTS is None:
            raise RuntimeError(
                "Coqui TTS not installed. Install with: pip install TTS torch --extra-index-url https://download.pytorch.org/whl/cpu"
            )
        # Choose a small, widely available English model by default
        model_name = voice_id or "tts_models/en/ljspeech/tacotron2-DDC"
        try:
            tts = CoquiTTS(model_name=model_name, progress_bar=False)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Coqui TTS model '{model_name}': {e}")
        out_path = OUTPUT_AUDIO_DIR / (timestamped_filename(basename, "coqui") + ".wav")
        try:
            tts.tts_to_file(text=text, file_path=str(out_path))
        except Exception as e:
            raise RuntimeError(f"Coqui synthesis failed: {e}")
        return out_path

    else:
        raise ValueError(f"Unknown engine: {engine}")
