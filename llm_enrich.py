from __future__ import annotations

import os
from typing import Optional

from utils import chunk_text

# Gemini API import; fall back gracefully if not available or no key.
try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - optional
    genai = None  # type: ignore


SYS_PROMPT = """You are an expert audiobook narrator.  
Your task is to transform the extracted text into listener-friendly audiobook-ready narration without leaving out details.  

Guidelines:
- Do NOT summarize or cut down the content. Keep all important details from the original.  
- Begin with a warm greeting such as: "Hello listeners, welcome...".
- Provide a short summary of what the listener will learn before diving into the content.
- Make it engaging and conversational, not just a direct copy.
- Rewrite the text so it flows naturally when spoken aloud.  
- Break down long or complex sentences into clear, shorter sentences.  
- Add natural pauses using "..." or line breaks for rhythm and engagement.  
- Remove raw Markdown symbols (#, *, -, etc.), but keep all information they represent.  
- Rewrite bullet points or lists into spoken style. For example: "First..., then..., finally...". 
- Expand abbreviations (e.g., "e.g." to "for example", "etc." to "and so on").  
- Maintain the same depth of information, just make it more engaging, warm, and listener-friendly.  

Here is the extracted content:
"""


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
