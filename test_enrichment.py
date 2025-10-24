"""
Simple test script to verify Gemini enrichment works.
Run: python test_enrichment.py
"""
import os
from llm_enrich import enrich_text

# Sample OCR text with errors
test_text = """
Helo Wrld!

Ths is a tst of the OCR systm. It shuld fix obvius erors.
The qick brown fox jumps ovr the lazy dog.
"""

print("=" * 60)
print("Testing Gemini AI Text Enrichment")
print("=" * 60)

# Check if API key is set
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("\n⚠️  GEMINI_API_KEY not set!")
    print("Set it with: $env:GEMINI_API_KEY = 'your_key_here'")
    print("Get key from: https://makersuite.google.com/app/apikey")
else:
    print(f"\n✅ GEMINI_API_KEY is set (length: {len(api_key)})")

print("\n" + "-" * 60)
print("ORIGINAL TEXT:")
print("-" * 60)
print(test_text)

print("\n" + "-" * 60)
print("ENRICHING WITH GEMINI...")
print("-" * 60)

enriched = enrich_text(test_text, model="gemini-2.5-flash")

print("\n" + "-" * 60)
print("ENRICHED TEXT:")
print("-" * 60)
print(enriched)
print("\n" + "=" * 60)

if enriched == test_text:
    print("⚠️  Text unchanged - check your API key or network")
else:
    print("✅ Enrichment successful!")
