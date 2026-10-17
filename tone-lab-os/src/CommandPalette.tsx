import { useState, useEffect, useRef } from "react";
import { Search, Plus, FileText, Settings, Database, ArrowRight } from "lucide-react";

export function CommandPalette({ isOpen, onClose, contextItemId, onOpenCreate }: { isOpen: boolean, onClose: () => void, contextItemId: string | null, onOpenCreate: (type: string) => void }) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const actions = [
    { id: "eq", icon: <Database size={16} />, label: "Create Equipment", type: "Equipment" },
    { id: "proj", icon: <Settings size={16} />, label: "New Project", type: "Project" },
    { id: "res", icon: <Search size={16} />, label: "Add Research", type: "Research" },
    { id: "doc", icon: <FileText size={16} />, label: "Upload Document", type: "Document" },
    { id: "pur", icon: <Database size={16} />, label: "Add Purchase Lead", type: "Purchase" },
    { id: "note", icon: <FileText size={16} />, label: "Quick Note", type: "Note" }
  ];

  const filteredActions = query 
    ? actions.filter(a => a.label.toLowerCase().includes(query.toLowerCase()))
    : actions;

  const isQuickCapture = query.length > 0 && filteredActions.length === 0;

  return (
    <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] bg-neutral-900/40 backdrop-blur-sm p-4">
      <div 
        className="absolute inset-0" 
        onClick={onClose}
      ></div>
      
      <div className="relative w-full max-w-2xl bg-[#F8F7F3] rounded-2xl shadow-2xl overflow-hidden border border-neutral-200/60 animate-in fade-in zoom-in-95 duration-200">
        
        {/* Input Area */}
        <div className="flex items-center px-6 py-5 border-b border-neutral-200/60 bg-white">
          <Search size={20} className="text-neutral-400 mr-4" />
          <input
            ref={inputRef}
            type="text"
            className="flex-1 bg-transparent text-lg text-neutral-900 outline-none placeholder:text-neutral-300 font-medium"
            placeholder="Search Tone Lab or type to Quick Capture..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Escape') onClose();
            }}
          />
          <div className="flex items-center gap-2 text-[10px] font-mono text-neutral-400 uppercase tracking-widest font-bold">
            <span className="bg-neutral-100 px-2 py-1 rounded">ESC</span> to cancel
          </div>
        </div>

        {/* Contextual Intelligence Banner */}
        {contextItemId && (
           <div className="bg-emerald-50/50 border-b border-emerald-100 px-6 py-2.5 flex items-center gap-2 text-xs font-medium text-emerald-800">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Context Active: <span className="font-bold">{contextItemId}</span>. Relations will be automatically established.
           </div>
        )}

        {/* Results / Actions */}
        <div className="max-h-[60vh] overflow-y-auto p-2">
          {isQuickCapture ? (
            <div className="p-4">
              <button className="w-full text-left flex items-start gap-4 p-4 rounded-xl hover:bg-white border border-transparent hover:border-neutral-200/60 transition-colors group">
                <div className="mt-1 bg-neutral-900 text-white p-2 rounded-lg group-hover:scale-105 transition-transform">
                  <Plus size={18} />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-neutral-900">Quick Capture</h4>
                  <p className="text-xs text-neutral-500 mt-1 line-clamp-1">Save "{query}" to Inbox for review</p>
                </div>
                <div className="ml-auto mt-2 text-neutral-300 group-hover:text-neutral-900 transition-colors">
                  <ArrowRight size={16} />
                </div>
              </button>
            </div>
          ) : (
            <div className="space-y-1">
              <div className="px-4 py-2 text-[10px] font-bold uppercase tracking-widest text-neutral-400">
                Create
              </div>
              {filteredActions.map((action, i) => (
                <button 
                  key={action.id}
                  onClick={() => {
                    onOpenCreate(action.type);
                  }}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-white text-neutral-600 hover:text-neutral-900 transition-colors group"
                >
                  <div className="text-neutral-400 group-hover:text-neutral-900">
                    {action.icon}
                  </div>
                  <span className="text-sm font-medium">{action.label}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
