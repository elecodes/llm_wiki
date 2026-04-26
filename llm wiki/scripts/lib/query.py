import os
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env relative to this file's location (llm wiki/scripts/.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class QueryEngine:
    def __init__(self, model_name="gemini-2.5-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.wiki_path = Path(__file__).parent.parent.parent / "wiki"
        
    def _get_wiki_context(self):
        """Reads all markdown files in the wiki directory to provide context."""
        context = []
        for file in self.wiki_path.glob("*.md"):
            if file.name in ["index.md", "log.md"]:
                continue
            with open(file, "r") as f:
                content = f.read()
                context.append(f"FILE: {file.name}\n---\n{content}\n---")
        return "\n\n".join(context)

    def query(self, user_query, chat_history=None):
        """Processes a user query against the wiki context."""
        wiki_context = self._get_wiki_context()
        
        system_instruction = """
You are the Chatbot for the SF Tennis Kids Club Knowledge Base.
Your goal is to answer user questions using ONLY the provided Wiki context.

RULES:
1. CITATIONS: Every factual claim must be followed by a citation to the wiki page in the format [[page-name]].
2. UNCERTAINTY: If the answer is not in the wiki, state it clearly and suggest what the user might look for in the raw sources.
3. FORMAT: Use clean Markdown. Use bold for emphasis and lists for structured info.
4. TONE: Professional, helpful, and concise.
5. ABSORPTION: If the user provides new information or you reach a significant conclusion, explicitly mention that this should be "absorbed" into the wiki.

WIKI CONTEXT:
---
{context}
---
""".format(context=wiki_context)

        # For the older SDK, we use system_instruction in the model constructor or as a prefix
        # Here I'll use it as part of the prompt for simplicity if I can't reconstruct history easily
        
        full_prompt = f"{system_instruction}\n\nUSER QUERY: {user_query}"

        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error querying the wiki: {str(e)}"
