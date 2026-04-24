import pytest
import sys
import os

# Add scripts directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.cleaner import clean_html, remove_quoted_replies
from lib.anonymizer import anonymize_text

def test_clean_html():
    html = "<html><body><h1>Hello</h1><p>World</p><script>alert('bad')</script></body></html>"
    cleaned = clean_html(html)
    assert "Hello" in cleaned
    assert "World" in cleaned
    assert "alert" not in cleaned

def test_remove_quoted_replies():
    text = "Important info\n\nOn Mon, Jan 1, 2024 at 10:00 AM User <user@example.com> wrote:\n> Quote here"
    cleaned = remove_quoted_replies(text)
    assert "Important info" in cleaned
    assert "On Mon" not in cleaned
    assert "Quote here" not in cleaned

def test_anonymize_basic():
    text = "My email is test@example.com and my phone is 555-123-4567."
    anonymized = anonymize_text(text)
    assert "[EMAIL]" in anonymized
    assert "[PHONE]" in anonymized
    assert "test@example.com" not in anonymized
    assert "555-123-4567" not in anonymized
