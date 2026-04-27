import os
from pathlib import Path
import google.generativeai as genai
from google.api_core import exceptions
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env relative to this file's location (llm wiki/scripts/.env)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class QueryEngine:
    def __init__(self, models=None):
        """
        Initialize with a list of model names for fallback.
        Priority: gemini-2.0-flash -> gemini-2.5-flash -> gemini-1.5-flash -> gemini-flash-latest
        """
        # We put 2.0-flash first as it's the current sweet spot for performance/quota.
        self.models = models or [
            "models/gemini-2.0-flash", 
            "models/gemini-2.5-flash", 
            "models/gemini-flash-latest",
            "models/gemini-2.0-flash-lite",
            "models/gemini-flash-lite-latest"
        ]
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or .env file")
        genai.configure(api_key=api_key)
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

    def generate(self, prompt):
        """Generic generation with model fallback."""
        last_error = None
        for model_name in self.models:
            try:
                logger.info(f"Attempting generation with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response
            except (exceptions.ResourceExhausted, exceptions.ServiceUnavailable) as e:
                logger.warning(f"Model {model_name} unavailable or quota exhausted. Trying fallback...")
                last_error = e
                continue
            except Exception as e:
                # Also catch 429/ResourceExhausted if they appear in the error string
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str or "exhausted" in error_str:
                    logger.warning(f"Quota error detected for {model_name} (string match). Trying fallback...")
                    last_error = e
                    continue
                
                logger.error(f"Critical error with model {model_name}: {str(e)}")
                last_error = e
                continue
        
        # If we reach here, all models failed.
        raise last_error if last_error else Exception("All models failed to respond.")

    def query(self, user_query, chat_history=None):
        """Processes a user query against the wiki context with model fallback."""
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
        
        full_prompt = f"{system_instruction}\n\nUSER QUERY: {user_query}"
        
        try:
            response = self.generate(full_prompt)
            return response.text
        except Exception as e:
            return f"Error: All Gemini models are currently exhausted or unavailable. Details: {str(e)}"

