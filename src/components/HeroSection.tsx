import React from 'react';
import { FitScoreReport } from '../types';

interface HeroSectionProps {
  currentReport?: FitScoreReport | null;
  onScrollToPreview: () => void;
  onScrollToHow: () => void;
}

export const HeroSection: React.FC<HeroSectionProps> = ({
  currentReport,
  onScrollToPreview,
  onScrollToHow
}) => {
  const scoreVal = currentReport ? Math.round(currentReport.overallScore) : 78;
  const matchedCount = currentReport ? currentReport.matchedSkills.length : 14;
  const redFlagCount = currentReport ? currentReport.redFlags.length : 3;

  return (
    <section id="hero" className="relative min-h-[92vh] flex flex-col items-center justify-center text-center px-4 sm:px-8 pt-24 pb-16">
      {/* Eyebrow badge */}
      <div
        id="hero-eyebrow"
        className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-[#1B2027] bg-[#0A0D10]/80 mb-7 text-[12.5px] font-['JetBrains_Mono'] text-[#8C97A3] backdrop-blur-sm"
      >
        <span className="w-2 h-2 rounded-full bg-[#3FD17E] shadow-[0_0_8px_#3FD17E] animate-pulse" />
        <span>now scoring in under 1.4s</span>
      </div>

      {/* Main Headline */}
      <h1
        id="hero-heading"
        className="font-['Space_Grotesk'] font-bold text-[40px] sm:text-[62px] md:text-[80px] leading-[1.04] tracking-[-1.5px] max-w-[1020px] text-[#F2F5F7]"
      >
        See the fit,<br />
        <span className="grad-text">before the interview.</span>
      </h1>

      {/* Paragraph Description */}
      <p
        id="hero-description"
        className="mt-6 text-[#8C97A3] text-base sm:text-[18px] max-w-[580px] leading-[1.6]"
      >
        HireSignal reads every resume the way an ATS does — then tells you what it actually found:
        matched skills, missing ones, and the red flags a recruiter would catch.
      </p>

      {/* Action Buttons */}
      <div id="hero-actions" className="mt-9 flex flex-wrap items-center justify-center gap-3.5">
        <button
          id="hero-cta-report"
          onClick={onScrollToPreview}
          className="bg-[#F2F5F7] hover:bg-[#3FD17E] text-[#05070A] font-semibold text-[15px] px-7 py-3.5 rounded-full transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(63,209,126,0.35)]"
        >
          See a live report
        </button>
        <button
          id="hero-cta-how"
          onClick={onScrollToHow}
          className="border border-[#1B2027] hover:border-[#8C97A3] hover:bg-white/[0.03] text-[#F2F5F7] text-[15px] px-7 py-3.5 rounded-full transition-all duration-200"
        >
          How scoring works
        </button>
      </div>

      {/* Floating score chip */}
      <div
        id="hero-float-chip"
        className="float-chip mt-14 font-['JetBrains_Mono'] text-[13px] text-[#8C97A3] border border-[#1B2027] bg-[#0A0D10]/90 backdrop-blur-md rounded-2xl px-5 py-3.5 flex items-center gap-4 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.7)]"
      >
        <span>fit score</span>
        <b className="text-[#3FD17E] text-[17px] font-bold">{scoreVal}/100</b>
        <span className="text-[#4E5762]">·</span>
        <span><strong className="text-[#F2F5F7] font-medium">{matchedCount}</strong> skills matched</span>
        <span className="text-[#4E5762]">·</span>
        <span><strong className="text-[#F2F5F7] font-medium">{redFlagCount}</strong> flags found</span>
      </div>
    </section>
  );
};
