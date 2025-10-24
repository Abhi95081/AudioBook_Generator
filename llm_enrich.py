from __future__ import annotations

import os
from typing import Optional

from utils import chunk_text

# Gemini API import; fall back gracefully if not available or no key.
try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - optional
    genai = None  # type: ignore


SYS_PROMPT = (
    "You are an expert audiobook editor. Rewrite this text for an engaging audiobook narration. "
    "Fix any OCR errors, improve sentence flow for spoken delivery, and make it listener-friendly. "
    "Keep the original meaning and key information intact, but optimize for natural speech patterns. "
    "Remove any artifacts like page numbers or formatting issues."
)


def enrich_text(text: str, model: Optional[str] = None, max_chars: int = 4000) -> str:
    """Enrich text via Google Gemini API.

    Args:
        text: Input text to enrich (from extracted .txt file)
        model: Gemini model name (default: gemini-pro)
        max_chars: Max chunk size for long documents

    Env vars:
        GEMINI_API_KEY: Your Google Gemini API key (required)
        GEMINI_MODEL: Model name override (optional, default: gemini-pro)

    Returns:
        Enriched text with OCR errors fixed, or original text if API unavailable.
    """
    text = text or ""
    if not text.strip():
        return text

    if genai is None:
        print("Warning: google-generativeai not installed. Returning original text.")
        return text

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Returning original text.")
        return text

    model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    try:
        genai.configure(api_key=api_key)
        gen_model = genai.GenerativeModel(model)
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini model: {e}")
        return text

    chunks = chunk_text(text, max_chars=max_chars)
    outputs = []
    
    for i, chunk in enumerate(chunks, 1):
        try:
            prompt = f"{SYS_PROMPT}\n\n{chunk}"
            response = gen_model.generate_content(prompt)
            enriched = response.text if response.text else chunk
            outputs.append(enriched)
            print(f"Enriched chunk {i}/{len(chunks)}")
        except Exception as e:
            print(f"Warning: Failed to enrich chunk {i}: {e}. Using original.")
            outputs.append(chunk)

    return "\n".join(outputs)
