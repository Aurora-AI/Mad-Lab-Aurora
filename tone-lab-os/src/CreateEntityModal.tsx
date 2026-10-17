import { useState } from "react";
import { X, ArrowRight } from "lucide-react";

export function CreateEntityModal({ type, contextItemId, onClose }: { type: string, contextItemId: string | null, onClose: () => void }) {
  const [step, setStep] = useState(1);

  // Dynamic fields based on SPEC
  const renderFields = () => {
    if (type === "Equipment") {
      return (
        <>
          <div className="grid grid-cols-2 gap-6">
             <Field label="Manufacturer" placeholder="e.g. Marshall" />
             <Field label="Model" placeholder="e.g. Origin 50C" />
          </div>
          <div className="grid grid-cols-2 gap-6 mt-6">
             <Field label="Category" placeholder="e.g. Amplifier" />
             <Field label="Subcategory" placeholder="e.g. Combo" />
          </div>
          <div className="grid grid-cols-3 gap-6 mt-6">
             <Field label="Status" placeholder="Owned / Planned" />
             <Field label="Priority" placeholder="P1 / P2" />
             <Field label="Role" placeholder="Role in the lab" />
          </div>
        </>
      );
    }
    if (type === "Research") {
      return (
        <>
          <Field label="Source URL / Title" placeholder="https://..." />
          <div className="mt-6">
             <label className="block text-[11px] font-bold uppercase tracking-widest text-neutral-400 mb-2">Summary / Findings</label>
             <textarea className="w-full bg-neutral-50 border border-neutral-200 rounded-lg p-3 text-sm outline-none focus:border-neutral-400 focus:bg-white transition-colors min-h-[120px]" placeholder="Key takeaways..."></textarea>
          </div>
          <div className="grid grid-cols-2 gap-6 mt-6">
             <Field label="Confidence" placeholder="High / Medium / Low" />
             <Field label="Impact" placeholder="How does this change things?" />
          </div>
        </>
      );
    }
    if (type === "Project") {
      return (
        <>
          <div className="grid grid-cols-2 gap-6">
             <Field label="Project ID" placeholder="e.g. AMP-001" />
             <Field label="Objective" placeholder="Main goal" />
          </div>
          <div className="grid grid-cols-2 gap-6 mt-6">
             <Field label="Baseline" placeholder="e.g. JCM800 Micro" />
             <Field label="Status" placeholder="Planning / R&D" />
          </div>
        </>
      );
    }
    
    // Default fallback
    return (
      <div className="space-y-6">
        <Field label="Title" placeholder={`Name of the ${type}`} />
        <Field label="Description" placeholder="Notes..." />
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-[110] flex items-center justify-center bg-neutral-900/60 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-3xl bg-white rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between px-8 py-6 border-b border-neutral-100">
          <div>
            <div className="text-[10px] font-bold uppercase tracking-widest text-neutral-400 mb-1">Structured Create</div>
            <h2 className="text-2xl font-extrabold tracking-tight text-neutral-900">New {type}</h2>
          </div>
          <button onClick={onClose} className="p-2 text-neutral-400 hover:text-neutral-900 transition-colors bg-neutral-50 hover:bg-neutral-100 rounded-full">
            <X size={20} />
          </button>
        </div>

        {/* Content */}
        <div className="p-8 bg-[#F8F7F3] min-h-[400px]">
          
          {contextItemId && (
            <div className="mb-8 p-4 bg-white border border-neutral-200 rounded-xl flex items-center justify-between">
              <div>
                <div className="text-[10px] font-bold uppercase tracking-widest text-neutral-400 mb-1">Auto-Relate Context</div>
                <div className="text-sm font-semibold text-neutral-900">Relating to: <span className="text-brand-black">{contextItemId}</span></div>
              </div>
              <div className="text-emerald-500">
                <span className="material-symbols-outlined">link</span>
              </div>
            </div>
          )}

          {renderFields()}

        </div>

        {/* Footer */}
        <div className="px-8 py-5 border-t border-neutral-100 bg-white flex justify-between items-center">
           <button onClick={onClose} className="text-xs font-bold uppercase tracking-widest text-neutral-400 hover:text-neutral-900 transition-colors">
             Cancel
           </button>
           <button onClick={onClose} className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-neutral-900 text-white text-xs font-bold tracking-widest uppercase hover:bg-neutral-800 transition-colors">
             Save to Inbox
             <ArrowRight size={14} />
           </button>
        </div>

      </div>
    </div>
  );
}

function Field({ label, placeholder }: { label: string, placeholder: string }) {
  return (
    <div>
      <label className="block text-[11px] font-bold uppercase tracking-widest text-neutral-400 mb-2">{label}</label>
      <input 
        type="text" 
        className="w-full bg-neutral-50 border border-neutral-200 rounded-lg px-4 py-3 text-sm font-medium outline-none focus:border-neutral-400 focus:bg-white transition-colors"
        placeholder={placeholder}
      />
    </div>
  );
}
