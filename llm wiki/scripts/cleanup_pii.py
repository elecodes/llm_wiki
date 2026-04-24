import os
import re

# Same hardened patterns as sync_emails.py
SENSITIVE_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,9}',
    'signature_block': r'(--\s*[\r\n]+.*|Sent from my.*|Best regards,.*|Cheers,.*|Thanks,.*|Sincerely,.*|Kind regards,.*|Atentamente,.*|Saludos,.*)',
    'names': r'(\b|_)(Abigail|John|Jane|Doe|Smith|Elena|Ken|Huang|[A-Z][a-z]+(\s|_)[A-Z][a-z]+)(\b|_)|(__[A-Z](\b|_))',
}

def sanitize_text(text):
    cleaned = re.sub(SENSITIVE_PATTERNS['email'], '[EMAIL]', text)
    cleaned = re.sub(SENSITIVE_PATTERNS['phone'], '[PHONE]', cleaned)
    cleaned = re.sub(SENSITIVE_PATTERNS['names'], '[REDACTED]', cleaned)
    cleaned = re.sub(SENSITIVE_PATTERNS['signature_block'], '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned.strip()

def sanitize_filename(filename):
    base, ext = os.path.splitext(filename)
    # Use the same logic as sync_emails.py
    cleaned = sanitize_text(base)
    cleaned = cleaned.replace('[EMAIL]', '').replace('[PHONE]', '').replace('[REDACTED]', '')
    cleaned = re.sub(r'[^\w\s-]', '', cleaned)
    cleaned = re.sub(r'\s+', '-', cleaned)
    return cleaned[:50].strip('-') + ext

def main():
    # Path to the raw directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.abspath(os.path.join(script_dir, '..', 'raw'))
    
    if not os.path.exists(raw_dir):
        print(f"Error: Directory {raw_dir} not found.")
        return

    print(f"Starting cleanup in: {raw_dir}")
    
    for filename in os.listdir(raw_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(raw_dir, filename)
            
            # 1. Sanitize Content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sanitized_content = sanitize_text(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            
            # 2. Sanitize Filename
            new_filename = sanitize_filename(filename)
            if new_filename != filename:
                new_file_path = os.path.join(raw_dir, new_filename)
                
                # Handle potential collisions
                if os.path.exists(new_file_path) and new_file_path != file_path:
                    new_filename = f"cleaned_{new_filename}"
                    new_file_path = os.path.join(raw_dir, new_filename)
                
                os.rename(file_path, new_file_path)
                print(f"✓ Renamed: {filename} -> {new_filename}")
            else:
                print(f"✓ Cleaned content: {filename}")

    print("\nCleanup complete!")

if __name__ == '__main__':
    main()
