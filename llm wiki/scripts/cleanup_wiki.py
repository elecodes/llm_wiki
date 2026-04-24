import os
import sys
import shutil
from collections import defaultdict

# Add lib directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))
from exporter import ObsidianExporter

def cleanup(wiki_dir):
    exporter = ObsidianExporter(wiki_dir)
    files = [f for f in os.listdir(wiki_dir) if f.endswith('.md')]
    
    # Map target base name -> list of entries
    groups = defaultdict(list)
    
    print(f"Scanning {len(files)} files in {wiki_dir}...")
    
    for filename in files:
        path = os.path.join(wiki_dir, filename)
        # Extract title from filename (strip .md)
        title = filename[:-3]
        target_base = exporter.normalize_title(title)
        if not target_base:
            target_base = "untitled"
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        groups[target_base].append({
            'original_filename': filename,
            'original_path': path,
            'content': content
        })

    actions = [] # list of (type, src, dst)
    
    for target_base, entries in groups.items():
        processed_contents = []
        # Sort to keep things stable
        entries.sort(key=lambda x: x['original_filename'])
        
        for entry in entries:
            is_duplicate = False
            for prev_content in processed_contents:
                if entry['content'] == prev_content:
                    is_duplicate = True
                    break
            
            if is_duplicate:
                actions.append(('delete', entry['original_path'], None))
                continue
            
            # Not a duplicate, determine final name
            suffix = f"-({len(processed_contents)})" if processed_contents else ""
            final_filename = f"{target_base}{suffix}.md"
            final_path = os.path.join(wiki_dir, final_filename)
            
            if entry['original_path'] != final_path:
                actions.append(('rename', entry['original_path'], final_path))
            
            processed_contents.append(entry['content'])

    # Execute actions
    print(f"Found {len(actions)} actions to perform.")
    
    # 1. Deletions
    for action_type, src, _ in actions:
        if action_type == 'delete':
            print(f"  [DELETE] {os.path.basename(src)}")
            os.remove(src)
            
    # 2. Renames (using intermediate names to avoid collisions)
    rename_queue = [a for a in actions if a[0] == 'rename']
    
    # Check if any rename target already exists (and is not about to be deleted or renamed itself)
    # Actually, the simplest way is to rename everything to a .tmp extension first
    tmp_renames = []
    for i, (_, src, dst) in enumerate(rename_queue):
        if not os.path.exists(src): continue # Might have been deleted if it was a duplicate (but our logic separates them)
        tmp_path = src + f".{i}.tmp"
        os.rename(src, tmp_path)
        tmp_renames.append((tmp_path, dst))
        
    for tmp_path, dst in tmp_renames:
        print(f"  [RENAME] {os.path.basename(tmp_path).split('.md')[0]}.md -> {os.path.basename(dst)}")
        if os.path.exists(dst):
            # This shouldn't happen if our logic is correct, but let's be safe
            print(f"  [WARNING] Target {os.path.basename(dst)} already exists. Overwriting.")
        os.rename(tmp_path, dst)

    print("Cleanup complete.")

if __name__ == "__main__":
    wiki_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../wiki'))
    if not os.path.exists(wiki_path):
        print(f"Error: {wiki_path} not found.")
        sys.exit(1)
    cleanup(wiki_path)
