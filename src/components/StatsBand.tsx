import React from 'react';

export const StatsBand: React.FC = () => {
  return (
    <section id="stats" className="border-t border-b border-[#1B2027] bg-[#0A0D10]/50 py-20 px-4 sm:px-8">
      <div className="max-w-[1080px] mx-auto">
        <div className="text-center mb-16">
          <div className="font-['JetBrains_Mono'] text-[12.5px] text-[#3FD17E] tracking-wider mb-2 uppercase">
            03 — by the numbers
          </div>
          <h2 className="font-['Space_Grotesk'] text-[28px] sm:text-[40px] font-bold text-[#F2F5F7]">
            Built to replace keyword-match guesswork.
          </h2>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center sm:text-left">
          {/* Stat 1 */}
          <div className="p-4 border-l border-[#1B2027]">
            <div className="font-['Space_Grotesk'] text-[44px] sm:text-[56px] font-bold text-[#F2F5F7] tracking-tight">
              86.2<span className="text-[#3FD17E]">%</span>
            </div>
            <p className="text-[#8C97A3] text-[13.5px] mt-2 leading-snug">
              precision on candidate fit classification (SLA ≥ 85%)
            </p>
          </div>

          {/* Stat 2 */}
          <div className="p-4 border-l border-[#1B2027]">
            <div className="font-['Space_Grotesk'] text-[44px] sm:text-[56px] font-bold text-[#F2F5F7] tracking-tight">
              81.7<span className="text-[#4FD8E0]">%</span>
            </div>
            <p className="text-[#8C97A3] text-[13.5px] mt-2 leading-snug">
              recall across 500 validated tech benchmark profiles
            </p>
          </div>

          {/* Stat 3 */}
          <div className="p-4 border-l border-[#1B2027]">
            <div className="font-['Space_Grotesk'] text-[44px] sm:text-[56px] font-bold text-[#F2F5F7] tracking-tight">
              1.4<span className="text-[#8B7CFF]">s</span>
            </div>
            <p className="text-[#8C97A3] text-[13.5px] mt-2 leading-snug">
              p95 response latency for full parsing and ML inference
            </p>
          </div>

          {/* Stat 4 */}
          <div className="p-4 border-l border-[#1B2027]">
            <div className="font-['Space_Grotesk'] text-[44px] sm:text-[56px] font-bold text-[#F2F5F7] tracking-tight">
              312<span className="text-[#3FD17E]">+</span>
            </div>
            <p className="text-[#8C97A3] text-[13.5px] mt-2 leading-snug">
              skills in our curated, boundary-safe NLP taxonomy
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
