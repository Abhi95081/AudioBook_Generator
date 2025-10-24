# LLM Enrichment Module - Multi-Provider Support

## Overview
The `llm_enrich.py` module now supports multiple LLM providers:
- **OpenAI** (GPT-4, GPT-3.5-turbo, etc.)
- **Google Gemini** (Gemini Pro)
- **Ollama** (local LLMs: Llama2, Mistral, etc.)
- **LM Studio** (local models via OpenAI-compatible API)

## How It Works
1. Input: extracted text from `.txt` file
2. Text is sent to your chosen LLM provider with a system prompt to rewrite/clean OCR errors
3. Output: enriched text saved back to `.txt` file

## Configuration

### Environment Variables

#### OpenAI
```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_MODEL = "gpt-4o-mini"  # or gpt-4, gpt-3.5-turbo
```

#### Google Gemini
```powershell
$env:GEMINI_API_KEY = "AIzaSyAa2vAQjxEFJMwowuN25BFbOTbjkfTn84U"
$env:GEMINI_MODEL = "gemini-pro"  # or gemini-1.5-pro
```

#### Ollama (Local)
1. Install Ollama: https://ollama.ai/
2. Pull a model: `ollama pull llama2`
3. Start server: `ollama serve` (runs on localhost:11434)
4. Set env vars:
```powershell
$env:OLLAMA_BASE_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama2"  # or mistral, codellama, etc.
```

#### LM Studio (Local)
1. Download LM Studio: https://lmstudio.ai/
2. Load a model in LM Studio
3. Start the server (default: localhost:1234)
4. Set env vars:
```powershell
$env:LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
$env:LMSTUDIO_MODEL = "local-model"  # name shown in LM Studio
```

## Usage Examples

### Auto-Detection (Recommended)
The module will automatically detect which provider to use based on available env vars:
```powershell
# Set your preferred provider's env vars, then:
.\.venv\Scripts\python.exe watch_uploads.py --enrich
```

### Explicit Provider Selection

#### Streamlit UI
1. Run: `.\.venv\Scripts\python.exe -m streamlit run app.py`
2. In sidebar: select provider dropdown (auto/openai/gemini/ollama/lmstudio)
3. Toggle "Use AI enrichment"
4. Upload file

#### CLI Single File
```powershell
# OpenAI
.\.venv\Scripts\python.exe process_file.py "test.pdf" --enrich --provider openai --model gpt-4o-mini

# Gemini
.\.venv\Scripts\python.exe process_file.py "test.pdf" --enrich --provider gemini --model gemini-pro

# Ollama
.\.venv\Scripts\python.exe process_file.py "test.pdf" --enrich --provider ollama --model llama2

# LM Studio
.\.venv\Scripts\python.exe process_file.py "test.pdf" --enrich --provider lmstudio --model local-model
```

#### CLI Folder Watcher
```powershell
# Gemini with auto-processing
.\.venv\Scripts\python.exe watch_uploads.py --enrich --provider gemini

# Ollama local (free, no API key needed!)
.\.venv\Scripts\python.exe watch_uploads.py --enrich --provider ollama --model mistral

# With TTS
.\.venv\Scripts\python.exe watch_uploads.py --enrich --provider gemini --tts pyttsx3
```

## System Prompt
The enrichment uses this prompt:
> "You are a helpful assistant. Improve clarity and fix obvious OCR errors without changing meaning. Keep the output concise but faithful."

You can customize this in `llm_enrich.py` by editing the `SYS_PROMPT` variable.

## Fallback Behavior
- If no API key is set or provider is unavailable, returns original text (no error)
- If one chunk fails, it continues with original chunk text
- Safe for production use

## Tips
- **Gemini**: Good balance of quality and cost, easy API key from Google AI Studio
- **Ollama**: Completely free, runs locally, good for privacy
- **LM Studio**: User-friendly local setup, great for experimenting
- **OpenAI**: Highest quality, costs per token

## Testing
To test without full extraction:
```python
from llm_enrich import enrich_text

# Test with auto-detection
result = enrich_text("Helo wrld! Ths is a tst.", provider="auto")
print(result)

# Test with specific provider
result = enrich_text("Helo wrld!", provider="gemini", model="gemini-pro")
print(result)
```
