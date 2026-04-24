import re

def anonymize_text(text):
    """Replaces PII with placeholders."""
    if not text:
        return ""
        
    # Email pattern
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    text = re.sub(email_pattern, '[EMAIL]', text)
    
    # Phone number pattern (basic, matches various common formats)
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    text = re.sub(phone_pattern, '[PHONE]', text)
    
    # Known names redaction
    names_to_redact = ['Caroline', 'Elena']
    for name in names_to_redact:
        text = re.sub(rf'\b{name}\b', '[REDACTED]', text, flags=re.IGNORECASE)
        
    return text
