import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class KnowledgeExtractor:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)
        
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
            response = self.model.generate_content(prompt)
            # Try to find JSON block in response
            content = response.text
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content:
                # Basic fallback to extract from first { to last }
                start = content.find("{")
                end = content.rfind("}") + 1
                content = content[start:end]
                
            return json.loads(content)
        except Exception as e:
            print(f"Error extracting knowledge: {e}")
            return None
