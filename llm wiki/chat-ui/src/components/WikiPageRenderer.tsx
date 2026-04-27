import React from 'react';
import ReactMarkdown from 'react-markdown';
import { 
  Info, 
  Link as LinkIcon, 
  Clock, 
  MapPin, 
  ExternalLink, 
  Globe,
  BookOpen
} from 'lucide-react';

interface WikiPageRendererProps {
  content: string;
  selectedPage?: string;
  onNavigate: (page: string) => void;
}

const WikiPageRenderer: React.FC<WikiPageRendererProps> = ({ content, selectedPage, onNavigate }) => {
  // Parsing logic
  const lines = content.split('\n');
  let title = '';
  const metadata: Record<string, string> = {};
  let bodyStartIndex = 0;

  // 1. Extract Title
  const titleMatch = lines[0]?.match(/^#\s+(.*)/);
  if (titleMatch) {
    title = titleMatch[1];
    bodyStartIndex = 1;
  }

  // 2. Extract Metadata (lines until ---)
  for (let i = bodyStartIndex; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line === '---') {
      bodyStartIndex = i + 1;
      break;
    }
    
    const metaMatch = line.match(/^\*\*(.*?)\*\*:\s*(.*)/);
    if (metaMatch) {
      metadata[metaMatch[1].toLowerCase()] = metaMatch[2];
    }
  }

  const bodyContent = lines.slice(bodyStartIndex).join('\n');

  // 3. Detect if it's a "Source" document (raw log, email, etc)
  const isSource = !metadata['summary'] || selectedPage?.toLowerCase().includes('re-') || selectedPage?.toLowerCase().includes('log');

  const processWikiLinks = (text: string) => {
    return text.replace(/\[\[(.*?)(?:\|(.*?))?\]\]/g, (_, link, display) => {
      const d = (display || link).trim();
      const l = link.trim();
      return `[${d}](wiki://${l})`; 
    });
  };

  return (
    <div className="flex flex-col space-y-8 animate-fade-in">
      {/* Metadata Header */}
      {(Object.keys(metadata).length > 0 || isSource) && (
        <div className="grid grid-cols-1 gap-4">
          <div className="p-5 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm space-y-4 shadow-xl relative overflow-hidden">
            {isSource && (
              <div className="absolute top-0 right-0 px-3 py-1 bg-accent-secondary/20 text-accent-secondary text-[8px] font-black uppercase tracking-tighter rounded-bl-lg border-l border-b border-white/10">
                Original Source
              </div>
            )}
            
            <div className="flex items-center gap-2 pb-2 border-b border-white/5">
              <Info className="w-4 h-4 text-accent-secondary" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-accent-secondary">
                {isSource ? 'Source Reference' : 'Quick Reference'}
              </span>
            </div>
            
            <div className="space-y-3">
              {metadata['summary'] && (
                <div className="flex gap-3">
                  <div className="w-5 h-5 rounded-md bg-accent-primary/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <Info className="w-3 h-3 text-accent-light" />
                  </div>
                  <p className="text-xs leading-relaxed text-text-main/80">{metadata['summary']}</p>
                </div>
              )}
              
              {metadata['sources'] && (
                <div className="flex gap-3">
                  <div className="w-5 h-5 rounded-md bg-emerald-500/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <LinkIcon className="w-3 h-3 text-emerald-400" />
                  </div>
                  <div className="text-xs text-text-muted flex flex-wrap gap-2">
                    <ReactMarkdown
                      components={{
                        a: ({ node, ...props }) => {
                          if (props.href?.startsWith('wiki://')) {
                            const page = props.href.replace('wiki://', '');
                            return (
                              <button 
                                onClick={() => onNavigate(page)}
                                className="text-accent-light hover:text-white transition-colors cursor-pointer font-medium underline decoration-accent-light/30 underline-offset-2"
                              >
                                {props.children}
                              </button>
                            );
                          }
                          return <a {...props} className="hover:text-white transition-colors underline" />;
                        }
                      }}
                    >
                      {processWikiLinks(metadata['sources'])}
                    </ReactMarkdown>
                  </div>
                </div>
              )}

              {metadata['last updated'] && (
                <div className="flex gap-3 items-center">
                  <div className="w-5 h-5 rounded-md bg-orange-500/10 flex items-center justify-center flex-shrink-0">
                    <Clock className="w-3 h-3 text-orange-400" />
                  </div>
                  <span className="text-[10px] text-text-muted font-medium">Last updated: {metadata['last updated']}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Main Body */}
      <div className={`markdown-content prose prose-invert prose-sm max-w-none ${isSource ? 'font-mono bg-white/2 p-6 rounded-xl border border-white/5' : ''}`}>
        <ReactMarkdown
          components={{
            h2: ({node, ...props}) => (
              <h2 className="flex items-center gap-2 group mt-10 first:mt-0">
                <span className="w-1.5 h-6 bg-accent-primary rounded-full group-hover:h-8 transition-all" />
                {props.children}
              </h2>
            ),
            h3: ({node, ...props}) => (
              <h3 className="text-accent-light font-outfit tracking-wide mt-6 border-b border-white/5 pb-2">
                {props.children}
              </h3>
            ),
            a: ({ node, ...props }) => {
              const href = props.href || '';
              const isWiki = href.startsWith('wiki://');
              const isMaps = href.includes('maps.app.goo.gl') || href.includes('google.com/maps');
              const isUrl = href.startsWith('http');

              if (isWiki) {
                const page = href.replace('wiki://', '');
                return (
                  <button 
                    onClick={() => onNavigate(page)}
                    className="inline-flex items-center gap-1 text-accent-light hover:text-white font-bold transition-all cursor-pointer underline decoration-accent-light/30 underline-offset-4"
                  >
                    <BookOpen className="w-3 h-3" />
                    {props.children}
                  </button>
                );
              }

              if (isMaps) {
                return (
                  <a 
                    href={href}
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-3 py-1.5 bg-accent-primary/10 hover:bg-accent-primary/20 border border-accent-primary/20 rounded-lg text-accent-light transition-all no-underline mt-1"
                  >
                    <MapPin className="w-3.5 h-3.5" />
                    <span className="font-medium text-xs">{props.children || 'View on Maps'}</span>
                    <ExternalLink className="w-3 h-3 opacity-50" />
                  </a>
                );
              }

              return (
                <a 
                  {...props} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center gap-1.5 text-blue-400 hover:text-blue-300 transition-colors"
                >
                  <Globe className="w-3 h-3" />
                  {props.children}
                  <ExternalLink className="w-3 h-3 opacity-30" />
                </a>
              );
            },
            table: ({node, ...props}) => (
              <div className="overflow-x-auto my-6 rounded-xl border border-white/5 shadow-2xl">
                <table className="w-full text-left border-collapse" {...props} />
              </div>
            ),
            thead: ({node, ...props}) => <thead className="bg-white/5" {...props} />,
            th: ({node, ...props}) => <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider text-text-muted border-b border-white/10" {...props} />,
            td: ({node, ...props}) => <td className="px-4 py-3 text-sm border-b border-white/5 bg-bg-secondary/30" {...props} />,
            ul: ({node, ...props}) => <ul className="space-y-2 my-4" {...props} />,
            li: ({node, ...props}) => (
              <li className="flex gap-2">
                <span className="text-accent-primary mt-1.5">•</span>
                <span>{props.children}</span>
              </li>
            ),
            hr: () => <hr className="border-white/5 my-10" />
          }}
        >
          {processWikiLinks(bodyContent)}
        </ReactMarkdown>
      </div>
    </div>
  );
};

export default WikiPageRenderer;
