import React, { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';
import { BarChart3, BrainCircuit, FileSearch, Gauge, Network, ShieldCheck } from 'lucide-react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { StepsSection } from './components/StepsSection';
import { ScorerPlayground } from './components/ScorerPlayground';
import { StatsBand } from './components/StatsBand';
import { CtaSection } from './components/CtaSection';
import { Footer } from './components/Footer';
import { FitScoreReport } from './types';

type Screen = 'home' | 'analyze' | 'system' | 'benchmarks';

const screens: Screen[] = ['home', 'analyze', 'system', 'benchmarks'];

function readScreen(): Screen {
  const value = window.location.hash.replace('#/', '').replace('#', '') as Screen;
  return screens.includes(value) ? value : 'home';
}

const transition = { duration: 0.42, ease: [0.22, 1, 0.36, 1] as const };

function SystemScreen() {
  const layers = [
    { icon: FileSearch, label: 'Input layer', title: 'Resume + JD parsing', text: 'Normalize PDF/DOCX/plain text into clean analysis-ready content.', tone: 'green' },
    { icon: BrainCircuit, label: 'Signal layer', title: 'NLP + 312+ skills', text: 'Extract technical signals, categories, frequencies and overlap.', tone: 'cyan' },
    { icon: Gauge, label: 'Decision layer', title: 'Composite fit score', text: 'Combine lexical similarity, skill overlap and ATS penalties.', tone: 'violet' },
    { icon: ShieldCheck, label: 'Audit layer', title: 'ATS red flags', text: 'Surface actionable issues instead of hiding them behind one score.', tone: 'amber' },
  ];

  return (
    <section className="screen-shell">
      <div className="section-kicker"><Network size={14} /> SYSTEM / PIPELINE</div>
      <div className="max-w-5xl">
        <h1 className="display-title">An explainable scoring pipeline,<br /><span className="grad-text">not a black box.</span></h1>
        <p className="section-lead">HireSignal turns messy candidate data into inspectable signals. Every layer has a job, a weight, and a visible output.</p>
      </div>

      <div className="pipeline-grid">
        {layers.map((layer, i) => {
          const Icon = layer.icon;
          return (
            <motion.div
              key={layer.title}
              className={`glass-card pipeline-card tone-${layer.tone}`}
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...transition, delay: i * 0.08 }}
              whileHover={{ y: -6 }}
            >
              <div className="pipeline-index">0{i + 1}</div>
              <div className="icon-box"><Icon size={20} /></div>
              <div className="mono-label">{layer.label}</div>
              <h3>{layer.title}</h3>
              <p>{layer.text}</p>
              {i < layers.length - 1 && <div className="pipeline-arrow">↓</div>}
            </motion.div>
          );
        })}
      </div>

      <motion.div className="architecture-panel glass-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ ...transition, delay: .35 }}>
        <div className="panel-head">
          <div>
            <div className="mono-label">REQUEST FLOW</div>
            <h2>POST /score → structured report</h2>
          </div>
          <span className="status-pill"><span /> rate limited</span>
        </div>
        <div className="flow-line">
          {['FastAPI', 'Text extraction', 'Skill taxonomy', 'TF-IDF', 'Red flags', 'Classifier', 'PostgreSQL'].map((item, i) => (
            <React.Fragment key={item}>
              <span>{item}</span>{i < 6 && <b>→</b>}
            </React.Fragment>
          ))}
        </div>
      </motion.div>
    </section>
  );
}

function BenchmarksScreen() {
  const metrics = [
    ['86.2%', 'fit precision', 'multi-label classifier target ≥ 85%'],
    ['81.7%', 'recall', 'validated benchmark profiles'],
    ['1.4s', 'p95 latency', 'full parse + inference target'],
    ['312+', 'skill signals', 'curated technical taxonomy'],
  ];
  return (
    <section className="screen-shell">
      <div className="section-kicker"><BarChart3 size={14} /> BENCHMARKS / EVIDENCE</div>
      <div className="max-w-5xl">
        <h1 className="display-title">Numbers that explain<br /><span className="grad-text">the product.</span></h1>
        <p className="section-lead">A resume scorer is only useful if you can inspect what produced the result. These are the project’s stated benchmark targets and outputs.</p>
      </div>
      <div className="metric-grid">
        {metrics.map(([value, label, detail], i) => (
          <motion.div key={label} className="metric-card glass-card" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ ...transition, delay: i * .07 }}>
            <div className="metric-value">{value}</div>
            <div className="metric-label">{label}</div>
            <p>{detail}</p>
          </motion.div>
        ))}
      </div>
      <StatsBand />
    </section>
  );
}

function HomeScreen({ currentReport, goAnalyze }: { currentReport: FitScoreReport | null; goAnalyze: () => void }) {
  return (
    <>
      <HeroSection currentReport={currentReport} onScrollToPreview={goAnalyze} onScrollToHow={() => {
        document.getElementById('how')?.scrollIntoView({ behavior: 'smooth' });
      }} />
      <StepsSection />
      <section id="how" className="home-spacer" />
      <CtaSection onScrollToPreview={goAnalyze} />
    </>
  );
}

export default function App() {
  const [screen, setScreen] = useState<Screen>(readScreen);
  const [currentReport, setCurrentReport] = useState<FitScoreReport | null>(null);

  useEffect(() => {
    const onHashChange = () => setScreen(readScreen());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const navigate = (next: Screen) => {
    if (next === screen) return;
    window.location.hash = `/${next}`;
  };

  return (
    <div className="app-root">
      <div className="noise" />
      <div className="grid-bg" />
      <div className="glow-blob a" />
      <div className="glow-blob b" />
      <div className="cursor-orb" />

      <Navbar currentScreen={screen} onNavigate={navigate} />

      <AnimatePresence mode="wait">
        <motion.main
          key={screen}
          initial={{ opacity: 0, y: 16, filter: 'blur(5px)' }}
          animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
          exit={{ opacity: 0, y: -10, filter: 'blur(4px)' }}
          transition={transition}
          className="relative z-10"
        >
          {screen === 'home' && <HomeScreen currentReport={currentReport} goAnalyze={() => navigate('analyze')} />}
          {screen === 'analyze' && <ScorerPlayground onReportChange={setCurrentReport} />}
          {screen === 'system' && <SystemScreen />}
          {screen === 'benchmarks' && <BenchmarksScreen />}
        </motion.main>
      </AnimatePresence>

      <Footer />
    </div>
  );
}
