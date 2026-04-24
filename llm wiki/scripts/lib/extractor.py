import os
import json
from pathlib import Path
from google import genai
from dotenv import load_dotenv

# Load .env relative to this file's location (llm wiki/scripts/.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class KnowledgeExtractor:
    def __init__(self, model_name="gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or .env file")
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_name
        
    def extract_knowledge(self, text):
        """Uses Gemini to extract structured knowledge and redact PII."""
        prompt = f"""
You are an expert knowledge management assistant. Your task is to transform a raw email into a structured knowledge base entry in Markdown format.

RAW EMAIL CONTENT:
---
{text}
---

INSTRUCTIONS:
1. TITLE: Create a descriptive title. IMPORTANT: Strip all email prefixes (Re:, Fwd:, etc.) and bracketed tags (e.g., [SF TENNIS]).
2. SUMMARY: Provide a concise summary (1-2 sentences) of the main knowledge or information.
3. KEY POINTS: Extract the most important facts, instructions, or insights as bullet points.
4. METADATA: Identify relevant tags or categories.
5. REDACTION (CRITICAL): 
   - Remove ALL personal names, specific office locations, or sensitive company-internal IDs not already handled.
   - Use generic placeholders like [NAME], [LOCATION], [ID].
   - Do NOT redact technical terms, project names, or general concepts.
6. FORMAT: Output ONLY valid JSON with the following structure:
{{
  "title": "Clean, descriptive title (no Re:, Fwd:, etc.)",
  "summary": "...",
  "key_points": ["...", "..."],
  "tags": ["...", "..."],
  "markdown_content": "The full synthesized knowledge in clean Markdown format"
}}

Ensure the 'markdown_content' is well-formatted, using headers, bold text, and lists where appropriate.
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            content = response.text
            
            # Basic cleanup if model returns markdown blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                content = content[start:end]
                
            return json.loads(content)
        except json.JSONDecodeError as je:
            print(f"JSON Decode Error: {je}")
            print(f"Raw content: {content}")
            return None
        except Exception as e:
            print(f"Error extracting knowledge: {e}")
            return None
