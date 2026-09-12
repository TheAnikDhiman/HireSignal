import React, { useEffect, useState } from 'react';
import { Activity, BarChart3, BrainCircuit, Menu, Network, X } from 'lucide-react';

type Screen = 'home' | 'analyze' | 'system' | 'benchmarks';

interface NavbarProps {
  currentScreen?: string;
  onNavigate?: (screen: Screen) => void;
  onSelectTab?: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentScreen = 'home', onNavigate }) => {
  const [open, setOpen] = useState(false);
  const items: { id: Screen; label: string; icon: React.ElementType }[] = [
    { id: 'home', label: 'Overview', icon: Activity },
    { id: 'analyze', label: 'Live Scorer', icon: BrainCircuit },
    { id: 'system', label: 'System', icon: Network },
    { id: 'benchmarks', label: 'Benchmarks', icon: BarChart3 },
  ];

  const go = (id: Screen) => {
    onNavigate?.(id);
    setOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  useEffect(() => {
    const move = (e: MouseEvent) => {
      document.documentElement.style.setProperty('--mx', `${e.clientX}px`);
      document.documentElement.style.setProperty('--my', `${e.clientY}px`);
    };
    window.addEventListener('mousemove', move);
    return () => window.removeEventListener('mousemove', move);
  }, []);

  return (
    <>
      <nav className="top-nav">
        <button className="brand" onClick={() => go('home')} aria-label="HireSignal home">
          <span className="brand-mark"><Activity size={18} /></span>
          <span>HireSignal</span>
          <small>AI JOB-FIT</small>
        </button>

        <div className="desktop-nav">
          {items.map(({ id, label, icon: Icon }) => (
            <button key={id} className={currentScreen === id ? 'nav-item active' : 'nav-item'} onClick={() => go(id)}>
              <Icon size={14} /> {label}
            </button>
          ))}
        </div>

        <button className="nav-cta" onClick={() => go('analyze')}>Run analysis <span>↗</span></button>
        <button className="mobile-menu" onClick={() => setOpen(v => !v)} aria-label="Toggle menu">
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>
      </nav>

      {open && (
        <div className="mobile-nav">
          {items.map(({ id, label, icon: Icon }) => (
            <button key={id} className={currentScreen === id ? 'active' : ''} onClick={() => go(id)}>
              <Icon size={16} /> {label}
            </button>
          ))}
        </div>
      )}
    </>
  );
};
