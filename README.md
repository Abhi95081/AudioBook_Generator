# OCR → Enrich → TTS (Streamlit)

A simple Streamlit app to:
- Extract text from files (txt, pdf, docx, images)
- Optionally clean/enrich with OpenAI
- Generate speech via pyttsx3 (offline) or gTTS (online)

## Features
- PDF text via pdfplumber, OCR fallback via pdf2image + Tesseract
- Image OCR via Tesseract
- DOCX via python-docx
- **Google Gemini AI** enrichment to rewrite/fix OCR errors
- Safe fallback if no API key (returns original text)
- Saves extracted text and audio to `outputs/`

## Requirements
- Python 3.10+
- Windows prerequisites for OCR on PDFs:
  - Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
  - Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases/
  - Add both to PATH. For Tesseract, the installer usually adds it. If not, set in code:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    ```

## Setup
1. Create and activate a virtual environment
2. Install dependencies
3. Get Gemini API key from: https://makersuite.google.com/app/apikey
4. Set `GEMINI_API_KEY` environment variable
5. Run the app

### Commands (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Set Tesseract path if needed
$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set Gemini API key (required for enrichment)
$env:GEMINI_API_KEY = "your_gemini_api_key_here"
$env:GEMINI_MODEL = "gemini-pro"  # Optional, defaults to gemini-pro

# Run Streamlit UI
.\.venv\Scripts\python.exe -m streamlit run app.py

# Or run CLI watcher (no browser, auto-process files dropped into uploads/)
.\.venv\Scripts\python.exe watch_uploads.py --enrich
```

## Usage

### Streamlit UI (Browser)
- Upload a file in the UI. If it is a scanned PDF, ensure Tesseract and Poppler are installed.
- Toggle "Use Gemini AI enrichment" in the sidebar.
- Choose TTS engine and generate audio.
- Files are saved under `outputs/text` and `outputs/audio`.

### CLI Single File
```powershell
.\.venv\Scripts\python.exe process_file.py "uploads\myfile.pdf" --enrich --model gemini-pro --tts pyttsx3
```

### CLI Folder Watcher (No Browser)
Drop files into `uploads/` and they're auto-processed:
```powershell
.\.venv\Scripts\python.exe watch_uploads.py --enrich --model gemini-pro
```
Press Ctrl+C to stop.

## Troubleshooting
- **Tesseract not found**: install Tesseract and ensure `tesseract.exe` is discoverable in PATH; or set `$env:TESSERACT_CMD`.
- **Poppler not found**: install Poppler and add `bin` directory to PATH, or set `$env:POPPLER_PATH`.
- **Gemini API errors**: enrich step falls back to original text if `GEMINI_API_KEY` is missing or invalid. Get your key from https://makersuite.google.com/app/apikey
- **pyttsx3 voices**: available voices depend on your system (SAPI5 on Windows). You may set `voice_id` in code.

## Notes
- This is a minimal demo. For large documents, consider chunking and streaming audio in segments.

## To Run This on Cmd Line
$env:GEMINI_API_KEY = "AIzaSyAa2vAQjxEFJMwowuN25BFbOTbjkfTn84U"; $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"; .\.venv\Scripts\python.exe watch_uploads.py --enrich
