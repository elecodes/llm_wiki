import os
import re
import pathlib

WIKI_DIR = "/Users/elena/Documents/llm_wiki/llm wiki/wiki"

def normalize_title(title):
    """Normalizes a title to kebab-case for filenames."""
    # Remove email prefixes
    title = re.sub(r'^(Re|Fwd):\s*', '', title, flags=re.IGNORECASE)
    # Remove bracketed tags
    title = re.sub(r'\[.*?\]', '', title)
    # Lowercase and replace non-alphanumeric with hyphens
    normalized = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    return normalized

def fix_links_and_redact(content):
    """Fixes [[...]] links and performs final redaction pass."""
    
    # 1. Fix links
    def replace_link(match):
        old_title = match.group(1)
        normalized = normalize_title(old_title)
        return f"[[{normalized}]]"
    
    content = re.sub(r'\[\[(.*?)\]\]', replace_link, content)
    
    # 2. Redact known names (add more as discovered)
    names_to_redact = ['Caroline', 'Elena', 'SF Tennis']
    for name in names_to_redact:
        content = re.sub(rf'\b{name}\b', '[REDACTED]', content, flags=re.IGNORECASE)
    
    return content

def polish():
    wiki_path = pathlib.Path(WIKI_DIR)
    
    # First pass: Rename files
    for file_path in wiki_path.glob("*.md"):
        if file_path.name == "index.md" or file_path.name == "log.md":
            continue
            
        old_name = file_path.stem
        new_name = normalize_title(old_name)
        
        if old_name != new_name:
            new_path = file_path.with_name(f"{new_name}.md")
            print(f"Renaming: {file_path.name} -> {new_path.name}")
            # If target exists, merge or skip? Let's assume unique enough for now or overwrite if identical
            if new_path.exists():
                 print(f"Warning: {new_path.name} already exists. Overwriting.")
            file_path.rename(new_path)
            
    # Second pass: Update content
    for file_path in wiki_path.glob("*.md"):
        content = file_path.read_text()
        new_content = fix_links_and_redact(content)
        
        if content != new_content:
            print(f"Polishing content: {file_path.name}")
            file_path.write_text(new_content)

if __name__ == "__main__":
    polish()
