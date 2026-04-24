import os
import re

class ObsidianExporter:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
            
    def normalize_title(self, title):
        """Normalizes title: lowercase, strip prefixes, replace spaces with hyphens."""
        # Strip prefixes like Re:, Fwd: and bracketed tags [TAG]
        title = re.sub(r'^(Re:\s*|Fwd:\s*|\[.*?\]\s*)+', '', title, flags=re.IGNORECASE).strip()
        # To lowercase and replace spaces/underscores with hyphens
        title = title.lower()
        title = re.sub(r'[\s_]+', '-', title)
        # Remove non-alphanumeric (except hyphens)
        title = re.sub(r'[^a-z0-9\-]', '', title)
        # Collapse multiple hyphens
        title = re.sub(r'-+', '-', title)
        return title.strip('-')

    def sanitize_filename(self, filename):
        """Removes characters that are invalid in filenames."""
        return self.normalize_title(filename)

    def export(self, data):
        """Saves structured data as a Markdown file in the vault."""
        title = data.get('title', 'Untitled')
        
        # Generate content first to compare if file exists
        tags_list = data.get('tags', [])
        tags_str = ", ".join([f"#{tag.replace(' ', '_')}" for tag in tags_list])
        
        body = f"""---
source: Gmail
tags: {tags_list}
summary: {data.get('summary', '')}
---
# {title}

{tags_str}

{data.get('markdown_content', '')}

---
*Key Points:*
"""
        for point in data.get('key_points', []):
            body += f"- {point}\n"
        new_content = body.strip()

        # Filename normalization
        normalized_name = self.normalize_title(title)
        if not normalized_name:
            normalized_name = "untitled"
            
        filename = normalized_name + ".md"
        filepath = os.path.join(self.vault_path, filename)
        
        # Handle duplicates and identical content
        counter = 1
        while os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                if f.read().strip() == new_content:
                    # Content is identical, skip creating a new file
                    return filepath
            
            # If content is different, try next numbered filename
            filename = f"{normalized_name}-({counter}).md"
            filepath = os.path.join(self.vault_path, filename)
            counter += 1
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return filepath
