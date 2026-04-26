import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, 
  BookOpen, 
  MessageSquare, 
  Plus, 
  ChevronRight, 
  Search, 
  Loader2, 
  FileText, 
  User, 
  Bot, 
  Zap, 
  BrainCircuit,
  Book
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000/api';

interface WikiLink {
  path: string;
  title: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: string[];
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Hello! I'm your **SF Tennis Kids Club** assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [wikiLinks, setWikiLinks] = useState<WikiLink[]>([]);
  const [selectedPage, setSelectedPage] = useState<string | null>(null);
  const [pageContent, setPageContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isAbsorbing, setIsAbsorbing] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchWikiIndex();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (selectedPage) {
      fetch(`${API_BASE}/wiki/${selectedPage}`)
        .then(res => res.json())
        .then(data => setPageContent(data.content))
        .catch(err => console.error("Error fetching page", err));
    }
  }, [selectedPage]);

  const fetchWikiIndex = async () => {
    try {
      const res = await fetch(`${API_BASE}/wiki`);
      const data = await res.json();
      // Simple parser for [display](link) or [[link]]
      const links: WikiLink[] = [];
      const lines = data.content.split('\n');
      lines.forEach((line: string) => {
        const match = line.match(/\[\[(.*?)(?:\|(.*?))?\]\]/);
        if (match) {
          const path = match[1].trim();
          const title = (match[2] || path).trim();
          links.push({ path, title });
        }
      });
      setWikiLinks(links);
    } catch (e) {
      console.error("Error fetching wiki index", e);
    }
  };

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, history: [...messages, userMessage] }),
      });
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer, citations: data.citations }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I lost power on the server. Should we try again?" }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAbsorb = async () => {
    setIsAbsorbing(true);
    try {
      const response = await fetch(`${API_BASE}/absorb`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: '', history: messages })
      });
      const data = await response.json();
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `### Knowledge Absorption Proposal\n\nI've analyzed our conversation and here is a new entry for the Wiki:\n\n---\n${data.proposal}\n---\n\nWould you like to save this?` 
      }]);
    } catch (error) {
      console.error('Absorb failed', error);
    } finally {
      setIsAbsorbing(false);
    }
  };

  const processWikiLinks = (text: string) => {
    return text.replace(/\[\[(.*?)(?:\|(.*?))?\]\]/g, (_, link, display) => {
      const d = (display || link).trim();
      return `**${d}**`; // Simple bold for now to avoid markdown link issues in chat
    });
  };

  return (
    <div 
      style={{ padding: '1.5rem', gap: '1.5rem' }}
      className="flex h-screen bg-[#0a0c10] text-gray-200 font-sans selection:bg-blue-500/30 overflow-hidden"
    >
      {/* Sidebar */}
      <aside 
        style={{ borderRadius: '1.5rem', height: '100%' }}
        className="w-80 border border-white/10 bg-[#0d1117] flex flex-col shadow-2xl overflow-hidden"
      >
        <div 
          style={{ paddingTop: '5rem', paddingBottom: '1.5rem', paddingLeft: '1.5rem', paddingRight: '1.5rem' }}
          className="border-b border-white/5"
        >
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-900/20">
              <Book className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-white tracking-tight">LLM Wiki</h1>
              <p className="text-[10px] uppercase tracking-widest text-blue-500 font-bold">Query Engine v2</p>
            </div>
          </div>
          
          <div className="space-y-1">
            <h2 className="text-[10px] uppercase tracking-widest text-gray-500 font-bold mb-3 px-2">Knowledge Base</h2>
            <div 
              style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}
              className="max-h-[calc(100vh-250px)] overflow-y-auto pr-2 custom-scrollbar"
            >
              {wikiLinks.map((link, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedPage(link.path)}
                  className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all flex items-center gap-3 group ${selectedPage === link.path ? 'bg-blue-600/10 text-blue-400 border border-blue-500/20' : 'hover:bg-white/5 text-gray-400 hover:text-white'}`}
                >
                  <FileText className={`w-4 h-4 ${selectedPage === link.path ? 'text-blue-400' : 'text-gray-600 group-hover:text-gray-400'}`} />
                  <span className="truncate">{link.title}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
        
        <div className="mt-auto p-6">
          <button 
            onClick={handleAbsorb}
            disabled={isAbsorbing || messages.length < 2}
            className="w-full px-4 py-3 bg-purple-600/10 hover:bg-purple-600/20 text-purple-400 rounded-xl text-sm font-bold transition-all flex items-center justify-center gap-3 border border-purple-500/20 disabled:opacity-30 uppercase tracking-widest"
          >
            <Zap className={`w-4 h-4 ${isAbsorbing ? 'animate-spin' : ''}`} />
            Absorb Insights
          </button>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden">
        {/* Header */}
        <header 
          style={{ paddingLeft: '3rem', paddingRight: '3rem' }}
          className="h-20 border-b border-white/5 flex items-center justify-between bg-[#0a0c10]/80 backdrop-blur-md sticky top-0 z-10"
        >
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-[11px] font-bold uppercase tracking-wider ${isProcessing ? 'bg-amber-500/10 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'}`}>
              <div className={`w-1.5 h-1.5 rounded-full ${isProcessing ? 'bg-amber-400 animate-pulse' : 'bg-emerald-400'}`} />
              {isProcessing ? 'Synthesizing...' : 'Idle'}
            </div>
            <div className="text-xs text-gray-500 font-medium">SF Tennis Kids Context</div>
          </div>
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-white/5 rounded-full transition-colors">
              <Search className="w-5 h-5 text-gray-500" />
            </button>
          </div>
        </header>

        {/* Messages */}
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto px-8 py-10 space-y-8 scroll-smooth custom-scrollbar"
        >
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center max-w-lg mx-auto text-center space-y-6">
              <div className="w-20 h-20 bg-blue-600/10 rounded-3xl flex items-center justify-center animate-pulse">
                <BrainCircuit className="w-10 h-10 text-blue-500" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">Ready to query the Wiki</h2>
                <p className="text-gray-500">Ask me anything about programs, pricing, or locations. I'll synthesize answers from the persistent knowledge base.</p>
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                key={i}
                className={`flex gap-6 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-gray-800 border border-white/10' : 'bg-blue-600 shadow-lg shadow-blue-900/20'}`}>
                  {msg.role === 'user' ? <User className="w-5 h-5 text-gray-400" /> : <Bot className="w-5 h-5 text-white" />}
                </div>
                <div className={`max-w-2xl space-y-3 ${msg.role === 'user' ? 'text-right' : ''}`}>
                  <div className={`inline-block p-5 rounded-2xl text-sm leading-relaxed ${msg.role === 'user' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'bg-[#11141b] border border-white/5'}`}>
                    <div className="markdown-content">
                      <ReactMarkdown>
                        {processWikiLinks(msg.content)}
                      </ReactMarkdown>
                    </div>
                    {msg.content.includes('### Knowledge Absorption Proposal') && (
                      <button 
                        onClick={async () => {
                          const lines = msg.content.split('\n');
                          const titleLine = lines.find(l => l.startsWith('# '));
                          const filename = titleLine ? titleLine.replace('# ', '').trim().toLowerCase().replace(/ /g, '-') : 'new-insight';
                          const content = msg.content.split('---')[1].trim();
                          
                          try {
                            const res = await fetch(`${API_BASE}/save`, {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({ filename, content })
                            });
                            if (res.ok) {
                              setMessages(prev => [...prev, { role: 'assistant', content: '✅ Saved successfully! The Wiki is getting smarter.' }]);
                              fetchWikiIndex();
                            }
                          } catch (e) {
                            console.error("Save failed", e);
                          }
                        }}
                        className="mt-4 w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold uppercase tracking-widest transition-all shadow-lg shadow-emerald-900/20"
                      >
                        Confirm and Save to Wiki
                      </button>
                    )}
                  </div>
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="flex flex-wrap gap-2 pt-1 justify-start">
                      {msg.citations.map((cite, j) => (
                        <button 
                          key={j}
                          onClick={() => setSelectedPage(cite)}
                          className="flex items-center gap-1.5 px-2.5 py-1.5 bg-white/5 hover:bg-white/10 border border-white/5 rounded-md text-[10px] text-gray-400 hover:text-white transition-all"
                        >
                          <BookOpen className="w-3 h-3 text-blue-400" />
                          {cite}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            ))
          )}
        </div>

        {/* Input */}
        <div className="px-4 pb-10 pt-4 bg-gradient-to-t from-[#0a0c10] via-[#0a0c10] to-transparent z-10">
          <form 
            onSubmit={handleSendMessage}
            style={{ marginBottom: '4rem', width: '100%' }}
            className="relative group"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about the club..."
              style={{ paddingLeft: '3.5rem' }}
              className="w-full bg-[#11141b] border border-white/10 rounded-2xl py-6 pr-44 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all text-base placeholder:text-gray-600 shadow-xl group-hover:border-white/20"
            />
            <div className="absolute right-3 top-3 bottom-3 flex items-center gap-2">
              <button 
                type="submit"
                disabled={!input.trim() || isProcessing}
                className="h-full px-6 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:hover:bg-blue-600 text-white rounded-xl transition-all shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2"
              >
                <span className="text-xs font-bold uppercase tracking-wider">Send</span>
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>
          <p className="text-center text-[10px] text-gray-600 mt-4 uppercase tracking-[0.2em] font-medium">
            Accumulated Knowledge Pattern • SF Tennis Kids v2.0
          </p>
        </div>

        {/* Wiki Preview Overlay */}
        <AnimatePresence>
          {selectedPage && (
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="absolute inset-y-0 right-0 w-[450px] bg-[#0d1117] border-l border-white/10 shadow-2xl z-20 flex flex-col"
            >
              <div className="p-6 border-b border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <BookOpen className="w-5 h-5 text-blue-400" />
                  <h3 className="font-bold text-white truncate max-w-[300px]">{selectedPage}</h3>
                </div>
                <button 
                  onClick={() => setSelectedPage(null)}
                  className="p-2 hover:bg-white/5 rounded-lg transition-colors"
                >
                  <ChevronRight className="w-5 h-5 text-gray-500" />
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-8 prose prose-invert prose-sm max-w-none custom-scrollbar">
                <ReactMarkdown>{pageContent}</ReactMarkdown>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
