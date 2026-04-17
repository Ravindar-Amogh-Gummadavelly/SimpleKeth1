// SimpleKeth — MultiMandiList Component
// Ranked list of top mandis by expected net profit

"use client";

import { motion } from "framer-motion";
import { MapPin, TrendingUp, Medal } from "lucide-react";
import { formatCurrency, formatDistance, cn } from "@/lib/utils";
import { useUIStore } from "@/lib/store";
import { t } from "@/i18n/config";
import type { AlternativeMandi, RecommendedMandi } from "@/types";

interface MandiItem {
  id: string;
  name: string;
  expectedNetProfit: number;
  distanceKm: number;
  isRecommended?: boolean;
}

interface MultiMandiListProps {
  recommendedMandi: RecommendedMandi & { expectedNetProfit: number };
  alternativeMandis: AlternativeMandi[];
  className?: string;
}

const rankColors = [
  "var(--color-profit-green)",
  "var(--color-fresh-leaf-green)",
  "var(--color-soft-crop-green)",
  "var(--color-clay-brown)",
  "var(--color-secondary-text)",
];

export function MultiMandiList({
  recommendedMandi,
  alternativeMandis,
  className,
}: MultiMandiListProps) {
  const locale = useUIStore((s) => s.locale);

  // Combine recommended + alternatives into ranked list
  const allMandis: MandiItem[] = [
    {
      id: recommendedMandi.id,
      name: recommendedMandi.name,
      expectedNetProfit: recommendedMandi.expectedNetProfit,
      distanceKm: recommendedMandi.distanceKm,
      isRecommended: true,
    },
    ...alternativeMandis.map((m) => ({
      id: m.id,
      name: m.name,
      expectedNetProfit: m.expectedNetProfit,
      distanceKm: m.distanceKm,
      isRecommended: false,
    })),
  ].sort((a, b) => b.expectedNetProfit - a.expectedNetProfit);

  return (
    <div className={cn("", className)} id="multi-mandi-list">
      <h3 className="mb-1" style={{ color: "var(--color-deep-farm-green)" }}>
        {t("market.title", locale)}
      </h3>
      <p className="text-sm mb-4" style={{ color: "var(--color-secondary-text)" }}>
        {t("market.subtitle", locale)}
      </p>

      <div className="flex flex-col gap-3">
        {allMandis.map((mandi, index) => (
          <motion.div
            key={mandi.id}
            initial={{ opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={cn(
              "card flex items-center gap-4 cursor-pointer",
              mandi.isRecommended && "ring-2"
            )}
            style={{
              borderLeft: `4px solid ${rankColors[index] || rankColors[4]}`,
              ...(mandi.isRecommended
                ? {
                    ringColor: "var(--color-profit-green)",
                    backgroundColor: "var(--color-light-green-tint)",
                  }
                : {}),
            }}
          >
            {/* Rank Badge */}
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
              style={{
                backgroundColor: rankColors[index] || rankColors[4],
                color: "white",
              }}
            >
              {index === 0 ? (
                <Medal className="w-5 h-5" />
              ) : (
                <span className="font-bold text-sm">#{index + 1}</span>
              )}
            </div>

            {/* Mandi Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <p className="font-semibold truncate" style={{ color: "var(--color-primary-text)" }}>
                  {mandi.name}
                </p>
                {mandi.isRecommended && (
                  <span
                    className="text-xs px-2 py-0.5 rounded-full font-medium flex-shrink-0"
                    style={{
                      backgroundColor: "var(--color-profit-green)",
                      color: "white",
                    }}
                  >
                    Best
                  </span>
                )}
              </div>
              <div className="flex items-center gap-3 mt-1">
                <span className="flex items-center gap-1 text-xs" style={{ color: "var(--color-secondary-text)" }}>
                  <MapPin className="w-3 h-3" />
                  {formatDistance(mandi.distanceKm)}
                </span>
              </div>
            </div>

            {/* Profit */}
            <div className="text-right flex-shrink-0">
              <p className="text-xs" style={{ color: "var(--color-secondary-text)" }}>
                {t("market.netProfit", locale)}
              </p>
              <p
                className="font-bold text-lg"
                style={{
                  fontFamily: "var(--font-heading)",
                  color:
                    mandi.expectedNetProfit > 0
                      ? "var(--color-profit-green)"
                      : "var(--color-loss-red)",
                }}
              >
                {formatCurrency(mandi.expectedNetProfit)}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
