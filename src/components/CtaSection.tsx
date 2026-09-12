import React from 'react';

interface CtaSectionProps {
  onScrollToPreview: () => void;
}

export const CtaSection: React.FC<CtaSectionProps> = ({ onScrollToPreview }) => {
  return (
    <section className="py-24 sm:py-32 px-4 sm:px-8 text-center relative overflow-hidden">
      <div className="absolute inset-0 bg-radial from-[#3FD17E]/5 via-transparent to-transparent pointer-events-none" />
      
      <div className="max-w-[720px] mx-auto relative z-10">
        <h2 className="font-['Space_Grotesk'] text-[32px] sm:text-[46px] font-bold text-[#F2F5F7] leading-tight">
          Ready to screen with confidence?
        </h2>
        <p className="text-[#8C97A3] text-[16px] sm:text-[18px] mt-4 mb-9 max-w-[540px] mx-auto leading-relaxed">
          Paste a job description and a resume. Get a composite score, a structured skill vector, and ATS red flags in under 1.4 seconds.
        </p>

        <button
          onClick={onScrollToPreview}
          className="bg-[#3FD17E] hover:bg-[#4FD8E0] text-[#04160C] font-semibold text-[15px] px-8 py-3.5 rounded-full transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(63,209,126,0.35)]"
        >
          Score your first resume free
        </button>
      </div>
    </section>
  );
};
