import os
import argparse
from dotenv import load_dotenv

from lib.ingestion import GmailIngestor
from lib.cleaner import clean_html, remove_quoted_replies, remove_signatures
from lib.anonymizer import anonymize_text
from lib.extractor import KnowledgeExtractor
from lib.exporter import ObsidianExporter

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Sync Gmail messages to Obsidian Wiki")
    parser.add_argument("--limit", type=int, default=10, help="Max number of emails to process")
    parser.add_argument("--vault", type=str, default="../wiki_vault", help="Path to Obsidian vault")
    args = parser.parse_args()

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'credentials.json')
    token_path = os.path.join(script_dir, 'token.json')
    vault_path = os.path.join(script_dir, args.vault)

    print(f"🚀 Starting Sync...")
    print(f"📂 Vault: {vault_path}")

    # Initialize components
    try:
        ingestor = GmailIngestor(credentials_path, token_path)
        extractor = KnowledgeExtractor(model_name="gemini-1.5-flash")
        exporter = ObsidianExporter(vault_path)
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return

    # Labels
    target_label = "TO-WIKI"
    processed_label = "PROCESSED"

    target_label_id = ingestor.get_label_id(target_label)
    processed_label_id = ingestor.get_label_id(processed_label)

    if not target_label_id:
        print(f"⚠️ Label '{target_label}' not found in Gmail. Please create it.")
        return
    
    if not processed_label_id:
        print(f"⚠️ Label '{processed_label}' not found. You might want to create it to track history.")

    # Fetch messages
    messages = ingestor.list_messages(label_ids=[target_label_id], max_results=args.limit)
    
    if not messages:
        print("✅ No new messages to process.")
        return

    print(f"📥 Found {len(messages)} messages to process.")

    for i, msg_ref in enumerate(messages):
        msg_id = msg_ref['id']
        print(f"\n[{i+1}/{len(messages)}] Processing message {msg_id}...")
        
        try:
            # 1. Fetch content
            msg = ingestor.get_message_content(msg_id)
            print(f"   Subject: {msg['subject']}")
            
            # 2. Clean and Anonymize
            cleaned_body = clean_html(msg['body'])
            cleaned_body = remove_quoted_replies(cleaned_body)
            cleaned_body = remove_signatures(cleaned_body)
            anonymized_body = anonymize_text(cleaned_body)
            
            # 3. Extract Knowledge (LLM)
            print(f"   🧠 Extracting knowledge with Gemini...")
            # Combine subject and snippet for more context if body is short
            context_text = f"Subject: {msg['subject']}\n\n{anonymized_body}"
            knowledge = extractor.extract_knowledge(context_text)
            
            if not knowledge:
                print(f"   ❌ Failed to extract knowledge for {msg_id}. Skipping.")
                continue
                
            # 4. Export to Obsidian
            filepath = exporter.export(knowledge)
            print(f"   📄 Exported to: {os.path.basename(filepath)}")
            
            # 5. Update Gmail labels
            if processed_label_id:
                ingestor.modify_labels(
                    msg_id, 
                    add_label_ids=[processed_label_id], 
                    remove_label_ids=[target_label_id]
                )
                print(f"   🏷️ Labels updated (moved to {processed_label})")
            else:
                ingestor.modify_labels(
                    msg_id, 
                    remove_label_ids=[target_label_id]
                )
                print(f"   🏷️ Label '{target_label}' removed.")
                
        except Exception as e:
            print(f"   ❌ Error processing {msg_id}: {e}")

    print(f"\n✨ Sync completed.")

if __name__ == "__main__":
    main()