import { ArrowLeft } from "lucide-react";
import { DossierContent } from "./DossierContent";
import { toneLabData } from "./data";

export function DossierMode({ itemId, onBack }: { itemId: string, onBack: () => void }) {
  const item = toneLabData.find(i => i.id === itemId);

  if (!item) {
    return <div>Item not found</div>;
  }

  return (
    <div className="min-h-screen bg-[#F8F7F3] font-sans antialiased selection:bg-neutral-200">
      <div className="border-b border-neutral-200/60 bg-white/50 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-8 sm:px-12 lg:px-16 h-12 flex items-center">
           <button 
             onClick={onBack}
             className="flex items-center gap-2 text-[10px] uppercase tracking-widest font-bold text-neutral-400 hover:text-black transition-colors"
           >
             <ArrowLeft size={14} />
             Back to Equipment
           </button>
        </div>
      </div>
      <DossierContent item={item} />
    </div>
  );
}
