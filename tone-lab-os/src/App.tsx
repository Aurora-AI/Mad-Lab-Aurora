import { useState, useEffect } from 'react';
import { StoreMode } from './StoreMode';
import { DossierMode } from './DossierMode';
import { CommandPalette } from './CommandPalette';
import { CreateEntityModal } from './CreateEntityModal';

function App() {
  const [activeItem, setActiveItem] = useState<string | null>(null);
  const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
  const [createModalType, setCreateModalType] = useState<string | null>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        setIsCommandPaletteOpen(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      {activeItem ? (
        <DossierMode itemId={activeItem} onBack={() => setActiveItem(null)} />
      ) : (
        <StoreMode onSelect={(id) => setActiveItem(id)} />
      )}

      {/* Global Add Button */}
      <button 
        onClick={() => setIsCommandPaletteOpen(true)}
        className="fixed bottom-8 right-8 z-[90] w-14 h-14 bg-neutral-900 text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-105 transition-transform"
        title="Open Command Palette (Ctrl+K)"
      >
        <span className="material-symbols-outlined text-[24px]">add</span>
      </button>

      {/* Command Palette */}
      <CommandPalette 
        isOpen={isCommandPaletteOpen} 
        onClose={() => setIsCommandPaletteOpen(false)} 
        contextItemId={activeItem}
        onOpenCreate={(type) => {
          setIsCommandPaletteOpen(false);
          setCreateModalType(type);
        }}
      />

      {/* Create Modal */}
      {createModalType && (
        <CreateEntityModal 
          type={createModalType} 
          contextItemId={activeItem}
          onClose={() => setCreateModalType(null)} 
        />
      )}
    </>
  );
}

export default App;
