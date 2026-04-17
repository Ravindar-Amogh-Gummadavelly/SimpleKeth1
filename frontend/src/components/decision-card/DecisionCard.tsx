// SimpleKeth — DecisionCard Component (CORE)
// The most important UI element: displays SELL NOW / HOLD decision
// with prominent profit, recommended mandi, confidence bar, and CTA

"use client";

import { motion } from "framer-motion";
import { MapPin, TrendingUp, ArrowRight, ShieldCheck } from "lucide-react";
import { cn, formatCurrency, formatConfidence, formatDistance } from "@/lib/utils";
import { useUIStore } from "@/lib/store";
import { t } from "@/i18n/config";
import type { Decision } from "@/types";

export interface DecisionCardProps {
  /** The recommendation decision */
  decision: Decision;
  /** Expected net profit in INR */
  expectedNetProfit: number;
  /** Recommended mandi details */
  recommendedMandi: {
    name: string;
    distanceKm: number;
  };
  /** Model confidence score (0-1) */
  confidence: number;
  /** Human-readable reasoning */
  rationaleText: string;
  /** CTA button callback */
  onAction?: () => void;
  /** Additional CSS class */
  className?: string;
}

export function DecisionCard({
  decision,
  expectedNetProfit,
  recommendedMandi,
  confidence,
  rationaleText,
  onAction,
  className,
}: DecisionCardProps) {
  const locale = useUIStore((s) => s.locale);
  const isSell = decision === "SELL NOW";
  const isProfit = expectedNetProfit > 0;

  const decisionColor = isSell
    ? "var(--color-profit-green)"
    : "var(--color-hold-warning)";

  const profitColor = isProfit
    ? "var(--color-profit-green)"
    : "var(--color-loss-red)";

  const decisionLabel = isSell
    ? t("decision.sellNow", locale)
    : t("decision.hold", locale);

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className={cn("card relative overflow-hidden", className)}
      role="region"
      aria-live="polite"
      aria-label={`Recommendation: ${decision}`}
      id="decision-card"
      style={{ borderLeft: `5px solid ${decisionColor}` }}
    >
      {/* Decision Badge */}
      <div className="flex items-center justify-between mb-4">
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className="decision-text px-4 py-2 rounded-lg text-white"
          style={{
            backgroundColor: decisionColor,
            fontSize: "22px",
          }}
          aria-label={`Decision: ${decisionLabel}`}
        >
          {decisionLabel}
        </motion.div>
        <div className="flex items-center gap-1.5" style={{ color: "var(--color-secondary-text)" }}>
          <ShieldCheck className="w-4 h-4" />
          <span className="text-sm font-medium">
            {t("decision.confidence", locale)}: {formatConfidence(confidence)}
          </span>
        </div>
      </div>

      {/* Profit Display */}
      <div className="mb-5">
        <p
          className="text-sm font-medium mb-1"
          style={{ color: "var(--color-secondary-text)" }}
        >
          {t("decision.expectedProfit", locale)}
        </p>
        <motion.p
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="profit-display"
          style={{ color: profitColor }}
          aria-label={`Expected profit: ${formatCurrency(expectedNetProfit)}`}
        >
          {formatCurrency(expectedNetProfit)}
        </motion.p>
      </div>

      {/* Recommended Mandi */}
      <div
        className="flex items-center gap-3 mb-4 p-3 rounded-lg"
        style={{ backgroundColor: "var(--color-light-green-tint)" }}
      >
        <MapPin
          className="w-5 h-5 flex-shrink-0"
          style={{ color: "var(--color-deep-farm-green)" }}
        />
        <div>
          <p
            className="text-xs font-medium mb-0.5"
            style={{ color: "var(--color-secondary-text)" }}
          >
            {t("decision.recommendedMandi", locale)}
          </p>
          <p
            className="font-semibold"
            style={{ color: "var(--color-deep-farm-green)" }}
          >
            {recommendedMandi.name}
          </p>
          <p className="text-xs" style={{ color: "var(--color-secondary-text)" }}>
            {t("decision.distance", locale)}: {formatDistance(recommendedMandi.distanceKm)}
          </p>
        </div>
      </div>

      {/* Confidence Bar */}
      <div className="mb-4">
        <div className="confidence-bar">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.round(confidence * 100)}%` }}
            transition={{ delay: 0.4, duration: 0.8, ease: "easeOut" }}
            className="confidence-bar-fill"
            style={{ backgroundColor: decisionColor }}
          />
        </div>
      </div>

      {/* Rationale */}
      <p
        className="text-sm mb-5 leading-relaxed"
        style={{ color: "var(--color-secondary-text)" }}
      >
        <span className="font-semibold" style={{ color: "var(--color-primary-text)" }}>
          {t("decision.rationale", locale)}:
        </span>{" "}
        {rationaleText}
      </p>

      {/* CTA Button */}
      {onAction && (
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onAction}
          className="btn-primary w-full"
          style={{
            backgroundColor: decisionColor,
          }}
        >
          <TrendingUp className="w-5 h-5" />
          {t("decision.viewAlternatives", locale)}
          <ArrowRight className="w-4 h-4" />
        </motion.button>
      )}
    </motion.div>
  );
}
