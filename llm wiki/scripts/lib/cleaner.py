import re
from bs4 import BeautifulSoup

def clean_html(html_content):
    """Strips HTML tags and returns clean text."""
    if not html_content:
        return ""
    # Use lxml if available, otherwise fallback to html.parser
    try:
        soup = BeautifulSoup(html_content, 'lxml')
    except Exception:
        soup = BeautifulSoup(html_content, 'html.parser')
        
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    text = soup.get_text(separator='\n')
    
    # Lighter cleaning: strip leading/trailing whitespace from lines
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def remove_quoted_replies(text):
    """Removes common quoted reply patterns."""
    patterns = [
        r"(?m)^On\s+.*wrote:\s*$",
        r"(?m)^---\s*Original Message\s*---.*$",
        r"(?m)^From:\s+.*$",
        r"(?m)^Sent:\s+.*$",
        r"(?m)^To:\s+.*$",
        r"(?m)^Subject:\s+.*$",
        r"(?m)^>.*$" # Quoted lines starting with >
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE | re.IGNORECASE)
    
    return text

def remove_signatures(text):
    """Removes common email signature blocks."""
    signature_patterns = [
        r"(?m)^--\s*[\r\n]+.*$", # Standard signature dash
        r"(?m)^Sent from my.*$", # Mobile signatures
        r"(?m)^(Best regards|Cheers|Thanks|Sincerely|Kind regards|Atentamente|Saludos),.*$", # Closing phrases
    ]
    for pattern in signature_patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE | re.IGNORECASE | re.DOTALL)
    
    return text.strip()
