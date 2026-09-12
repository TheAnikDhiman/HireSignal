import React from 'react';

export const StepsSection: React.FC = () => {
  return (
    <section id="how" className="max-w-[1080px] mx-auto py-24 sm:py-32 px-4 sm:px-8">
      <div>
        <div
          id="how-tag"
          className="font-['JetBrains_Mono'] text-[12.5px] text-[#3FD17E] tracking-wider mb-3.5 uppercase"
        >
          01 — how it scores
        </div>
        <h2
          id="how-heading"
          className="font-['Space_Grotesk'] text-[28px] sm:text-[38px] md:text-[44px] font-bold max-w-[640px] leading-[1.15] mb-16 text-[#F2F5F7]"
        >
          Three signals combined into one number you can actually act on.
        </h2>
      </div>

      <div id="step-grid" className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Step 1 */}
        <div
          id="step-card-1"
          className="border border-[#1B2027] hover:border-white/20 rounded-2xl p-7 bg-gradient-to-b from-white/[0.03] to-transparent transition-all duration-300 hover:-translate-y-1 group"
        >
          <div className="font-['JetBrains_Mono'] text-[#4E5762] text-[13px] mb-4.5 group-hover:text-[#3FD17E] transition-colors">
            01
          </div>
          <h3 className="font-['Space_Grotesk'] text-[20px] font-semibold mb-2.5 text-[#F2F5F7]">
            Text signal
          </h3>
          <p className="text-[#8C97A3] text-[14.5px] leading-[1.6]">
            Resume and JD are parsed into clean text, then compared with TF-IDF cosine similarity — the base fit score.
          </p>
          <div className="mt-5 pt-4 border-t border-[#1B2027] flex items-center justify-between text-[11px] font-['JetBrains_Mono'] text-[#8C97A3]">
            <span>Sublinear TF (1,2 ngrams)</span>
            <span className="text-[#3FD17E]">Weight: 40%</span>
          </div>
        </div>

        {/* Step 2 */}
        <div
          id="step-card-2"
          className="border border-[#1B2027] hover:border-white/20 rounded-2xl p-7 bg-gradient-to-b from-white/[0.03] to-transparent transition-all duration-300 hover:-translate-y-1 group"
        >
          <div className="font-['JetBrains_Mono'] text-[#4E5762] text-[13px] mb-4.5 group-hover:text-[#4FD8E0] transition-colors">
            02
          </div>
          <h3 className="font-['Space_Grotesk'] text-[20px] font-semibold mb-2.5 text-[#F2F5F7]">
            Skill signal
          </h3>
          <p className="text-[#8C97A3] text-[14.5px] leading-[1.6]">
            A 300+ term taxonomy extracts real skill overlap, not just keyword echoes, and weights it into the final score.
          </p>
          <div className="mt-5 pt-4 border-t border-[#1B2027] flex items-center justify-between text-[11px] font-['JetBrains_Mono'] text-[#8C97A3]">
            <span>312+ taxonomy dictionary</span>
            <span className="text-[#4FD8E0]">Weight: 60%</span>
          </div>
        </div>

        {/* Step 3 */}
        <div
          id="step-card-3"
          className="border border-[#1B2027] hover:border-white/20 rounded-2xl p-7 bg-gradient-to-b from-white/[0.03] to-transparent transition-all duration-300 hover:-translate-y-1 group"
        >
          <div className="font-['JetBrains_Mono'] text-[#4E5762] text-[13px] mb-4.5 group-hover:text-[#8B7CFF] transition-colors">
            03
          </div>
          <h3 className="font-['Space_Grotesk'] text-[20px] font-semibold mb-2.5 text-[#F2F5F7]">
            Red-flag signal
          </h3>
          <p className="text-[#8C97A3] text-[14.5px] leading-[1.6]">
            Rule-based checks catch what an ATS would silently reject — gaps, formatting issues, inconsistent dates.
          </p>
          <div className="mt-5 pt-4 border-t border-[#1B2027] flex items-center justify-between text-[11px] font-['JetBrains_Mono'] text-[#8C97A3]">
            <span>11 heuristic checks</span>
            <span className="text-[#8B7CFF]">Penalty: 0 - 28 pts</span>
          </div>
        </div>
      </div>
    </section>
  );
};
