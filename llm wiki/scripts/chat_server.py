import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
from lib.query import QueryEngine

app = FastAPI(title="LLM Wiki Chatbot API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

wiki_path = Path(__file__).parent.parent / "wiki"
engine = QueryEngine()

class QueryRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = []

class QueryResponse(BaseModel):
    answer: str
    citations: List[str]

@app.get("/api/wiki")
async def list_wiki_pages():
    """Returns a list of wiki pages from the index."""
    index_file = wiki_path / "index.md"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Wiki index not found")
    
    with open(index_file, "r") as f:
        content = f.read()
    return {"content": content}

@app.get("/api/wiki/{page_name}")
async def get_wiki_page(page_name: str):
    """Returns the content of a specific wiki page."""
    if not page_name.endswith(".md"):
        page_name += ".md"
    
    file_path = wiki_path / page_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Page {page_name} not found")
    
    with open(file_path, "r") as f:
        content = f.read()
    return {"name": page_name, "content": content}

@app.post("/api/query", response_model=QueryResponse)
async def query_wiki(request: QueryRequest):
    """Processes a user query and returns a synthesized answer."""
    try:
        answer = engine.query(request.query, request.history)
        # Basic citation extraction (looking for [[page-name]])
        import re
        citations = re.findall(r"\[\[(.*?)\]\]", answer)
        return QueryResponse(answer=answer, citations=list(set(citations)))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/absorb")
async def absorb_knowledge(request: QueryRequest):
    """Summarizes the chat history and proposes a wiki update."""
    try:
        # Prompt to synthesize history into a wiki-style summary
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in request.history])
        prompt = f"""
        Analyze the following chat history and extract any NEW knowledge or significant insights about SF Tennis Kids Club.
        Synthesize this into a structured Wiki page following the pattern:
        # Title
        **Summary**: ...
        **Sources**: Conversation with Assistant
        **Last updated**: Today
        ---
        Content...
        
        CHAT HISTORY:
        {history_text}
        
        Return ONLY the markdown content for the new or updated page.
        """
        
        response = engine.model.generate_content(prompt)
        # For now, we return the proposal. In a real scenario, we might save it directly.
        return {"proposal": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save")
async def save_page(request: dict):
    """Saves a new or updated wiki page."""
    try:
        filename = request.get("filename")
        content = request.get("content")
        if not filename or not content:
            raise HTTPException(status_code=400, detail="Missing filename or content")
        
        # Ensure it has .md extension
        if not filename.endswith(".md"):
            filename += ".md"
            
        path = os.path.join(WIKI_DIR, filename)
        with open(path, "w") as f:
            f.write(content)
            
        # Update index.md if it's a new file
        index_path = os.path.join(WIKI_DIR, "index.md")
        with open(index_path, "r") as f:
            index_content = f.read()
            
        if filename not in index_content:
            with open(index_path, "a") as f:
                f.write(f"\n- [[{filename}]]")
                
        return {"status": "success", "message": f"Saved {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
