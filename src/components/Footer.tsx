import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-[#1B2027] bg-[#050607] py-12 px-6 sm:px-10 text-[13px] text-[#4E5762]">
      <div className="max-w-[1080px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-3">
          <svg width="22" height="22" viewBox="0 0 30 30" fill="none">
            <path
              d="M1 15 L7 15 L10 6 L14 24 L17 12 L20 18 L23 15 L29 15"
              stroke="#3FD17E"
              strokeWidth="1.8"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="font-['Space_Grotesk'] font-semibold text-[#8C97A3]">HireSignal</span>
          <span>·</span>
          <span>AI Job-Fit Scorer</span>
        </div>

        <div className="flex flex-wrap items-center gap-5 text-[12px] font-['JetBrains_Mono']">
          <span className="text-[#3FD17E]">Python FastAPI</span>
          <span>·</span>
          <span>Scikit-Learn ML</span>
          <span>·</span>
          <span>TF-IDF NLP</span>
          <span>·</span>
          <span>PostgreSQL</span>
        </div>

        <div>
          © {new Date().getFullYear()} HireSignal. All rights reserved.
        </div>
      </div>
    </footer>
  );
};
