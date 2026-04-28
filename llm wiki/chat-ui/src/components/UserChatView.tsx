import React, { useState, useEffect, useRef } from 'react';
import { 
  Send, 
  BookOpen, 
  Search, 
  User, 
  Bot, 
  BrainCircuit,
  ChevronRight
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';
import WikiPageRenderer from './WikiPageRenderer';

const API_BASE = 'http://localhost:8000/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: string[];
}

function UserChatView() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "Hello! I'm your **SF Tennis Kids Club** assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [selectedPage, setSelectedPage] = useState<string | null>(null);
  const [pageContent, setPageContent] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

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
      
      // Filter out any "Absorb" proposals for normal users just in case
      const filteredAnswer = data.answer.split('### Knowledge Absorption Proposal')[0].trim();
      
      setMessages(prev => [...prev, { role: 'assistant', content: filteredAnswer, citations: data.citations }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I lost power on the server. Should we try again?" }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const processWikiLinks = (text: string) => {
    // Convert [[Page Name]] or [[Page Name|Display Text]] to [Display Text](wiki://Page Name)
    return text.replace(/\[\[(.*?)(?:\|(.*?))?\]\]/g, (_, link, display) => {
      const d = (display || link).trim();
      const l = link.trim();
      return `[${d}](wiki://${l})`; 
    });
  };

  return (
    <div className="flex h-screen bg-bg-main text-text-main font-sans selection:bg-accent-primary/30 overflow-hidden">
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden max-w-5xl mx-auto w-full shadow-2xl bg-bg-main/50 rounded-2xl">
        {/* Header */}
        <header 
          style={{ paddingLeft: '3rem', paddingRight: '3rem' }}
          className="h-20 border-b border-white/5 flex items-center justify-between bg-bg-main/80 backdrop-blur-md sticky top-0 z-10"
        >
          <div className="flex items-center gap-4">
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-[11px] font-bold uppercase tracking-wider ${isProcessing ? 'bg-accent-secondary/10 text-accent-secondary' : 'bg-emerald-500/10 text-emerald-400'}`}>
              <div className={`w-1.5 h-1.5 rounded-full ${isProcessing ? 'bg-accent-secondary animate-pulse' : 'bg-emerald-400'}`} />
              {isProcessing ? 'Synthesizing...' : 'Idle'}
            </div>
            <div className="text-xs text-text-muted font-medium">SF Tennis Kids Context</div>
          </div>
        </header>

        {/* Messages */}
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto px-8 pt-24 pb-10 space-y-8 scroll-smooth custom-scrollbar"
        >
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center max-w-lg mx-auto text-center space-y-6">
              <div className="w-20 h-20 bg-accent-primary/10 rounded-3xl flex items-center justify-center animate-pulse">
                <BrainCircuit className="w-10 h-10 text-accent-primary" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-2 tracking-tight">How can I help?</h2>
                <p className="text-text-muted max-w-sm mx-auto leading-relaxed">Ask me anything about programs, pricing, or locations. I'll synthesize answers from the persistent knowledge base.</p>
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
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-bg-muted border border-white/10' : 'bg-accent-primary shadow-lg shadow-accent-primary/20'}`}>
                  {msg.role === 'user' ? <User className="w-5 h-5 text-text-muted" /> : <Bot className="w-5 h-5 text-primary-fg" />}
                </div>
                <div className={`max-w-2xl space-y-3 ${msg.role === 'user' ? 'text-right' : ''}`}>
                  <div
                    style={{ padding: '18px 40px' }}
                    className={`chat-bubble inline-flex min-h-[68px] items-center rounded-2xl text-sm leading-relaxed ${msg.role === 'user' ? 'bg-accent-primary text-primary-fg shadow-lg shadow-accent-primary/20' : 'bg-bg-secondary border border-white/5'}`}
                  >
                    <div className="markdown-content">
                      <ReactMarkdown
                        components={{
                          a: ({ node, ...props }) => {
                            if (props.href?.startsWith('wiki://')) {
                              const page = props.href.replace('wiki://', '');
                              return (
                                <button 
                                  onClick={() => setSelectedPage(page)}
                                  className="text-accent-light hover:underline font-bold transition-colors cursor-pointer"
                                >
                                  {props.children}
                                </button>
                              );
                            }
                            return <a {...props} target="_blank" rel="noopener noreferrer" />;
                          }
                        }}
                      >
                        {processWikiLinks(msg.content)}
                      </ReactMarkdown>
                    </div>
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
        <div className="px-8 pb-10 pt-4 bg-gradient-to-t from-bg-main via-bg-main to-transparent z-10">
          <form 
            onSubmit={handleSendMessage}
            style={{ marginBottom: '2rem', width: '100%' }}
            className="relative group"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything about the club..."
              style={{ paddingLeft: '3.5rem' }}
              className="w-full bg-bg-secondary border border-white/10 rounded-2xl py-6 pr-44 focus:outline-none focus:ring-2 focus:ring-accent-primary/50 focus:border-accent-primary/50 transition-all text-base placeholder:text-text-muted/50 shadow-xl group-hover:border-white/20"
            />
            <div className="absolute right-3 top-3 bottom-3 flex items-center gap-2">
              <button 
                type="submit"
                disabled={!input.trim() || isProcessing}
                className="h-full px-6 bg-accent-primary hover:bg-accent-primary/80 disabled:opacity-50 text-primary-fg rounded-xl transition-all shadow-lg shadow-accent-primary/20 flex items-center justify-center gap-2"
              >
                <span className="text-xs font-bold uppercase tracking-wider">Send</span>
                <Send className="w-4 h-4" />
              </button>
            </div>
          </form>
          <p className="text-center text-[10px] text-text-muted/40 uppercase tracking-[0.3em] font-bold">
            SF Tennis Kids Assistant
          </p>
        </div>

        {/* Wiki Preview Overlay */}
        <AnimatePresence>
          {selectedPage && (
            <>
              {/* Backdrop */}
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setSelectedPage(null)}
                className="absolute inset-0 bg-bg-main/60 backdrop-blur-sm z-20"
              />
              
              <motion.div
                initial={{ x: '100%', opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: '100%', opacity: 0 }}
                transition={{ type: 'spring', damping: 25, stiffness: 200 }}
                className="absolute inset-y-0 right-0 w-full sm:w-[500px] bg-bg-muted border-l border-white/10 shadow-[0_0_50px_-12px_rgba(0,0,0,0.5)] z-30 flex flex-col"
              >
                {/* Overlay Header */}
                <div className="h-24 px-8 border-b border-white/5 flex items-center justify-between bg-bg-muted/80 backdrop-blur-md sticky top-0 z-10">
                  <div className="flex items-center gap-4 overflow-hidden">
                    <div className="w-12 h-12 rounded-2xl bg-accent-primary/20 flex items-center justify-center flex-shrink-0 border border-accent-primary/20">
                      <BookOpen className="w-6 h-6 text-accent-light" />
                    </div>
                    <div className="overflow-hidden">
                      <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-text-muted mb-0.5">Wiki Resource</p>
                      <h3 className="font-bold text-white text-xl truncate font-outfit">{selectedPage}</h3>
                    </div>
                  </div>
                  <button 
                    onClick={() => setSelectedPage(null)}
                    className="w-10 h-10 flex items-center justify-center hover:bg-white/5 rounded-xl transition-all border border-transparent hover:border-white/10 group"
                  >
                    <ChevronRight className="w-6 h-6 text-text-muted group-hover:text-white group-hover:translate-x-0.5 transition-all" />
                  </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto px-10 py-10 custom-scrollbar">
                  {pageContent ? (
                    <WikiPageRenderer 
                      content={pageContent} 
                      selectedPage={selectedPage}
                      onNavigate={(page) => setSelectedPage(page)} 
                    />
                  ) : (
                    <div className="h-full flex items-center justify-center">
                      <div className="w-8 h-8 border-2 border-accent-primary border-t-transparent rounded-full animate-spin" />
                    </div>
                  )}
                </div>

                {/* Footer / Meta */}
                <div className="p-6 border-t border-white/5 bg-bg-main/30 text-center">
                  <p className="text-[9px] text-text-muted/40 uppercase tracking-widest font-bold">
                    Powered by SF Tennis Kids Knowledge Base
                  </p>
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default UserChatView;
