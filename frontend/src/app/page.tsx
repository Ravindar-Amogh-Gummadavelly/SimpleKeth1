// SimpleKeth — Dashboard Page (/)
// Hero section + InputModule + DecisionCard + Quick Recommendations

"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sprout, TrendingUp, Shield } from "lucide-react";
import { DecisionCard } from "@/components/decision-card/DecisionCard";
import { InputModule } from "@/components/input-module/InputModule";
import { MultiMandiList } from "@/components/multi-mandi-list/MultiMandiList";
import { useUIStore, useRecommendationStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { fetchRecommendation } from "@/lib/api";
import type { RecommendationResponse } from "@/types";

// Sample data for initial display
const SAMPLE_RECOMMENDATION: RecommendationResponse = {
  decision: "SELL NOW",
  recommendedMandi: { id: "M001", name: "Azadpur Mandi", distanceKm: 25 },
  expectedNetProfit: 12450,
  alternativeMandis: [
    { id: "M002", name: "Lasalgaon Mandi", expectedNetProfit: 11800, distanceKm: 42 },
    { id: "M003", name: "Pimpalgaon Mandi", expectedNetProfit: 10200, distanceKm: 58 },
  ],
  confidence: 0.78,
  rationaleText:
    "Expected mandi price is higher in Azadpur Mandi and transport cost is low. Current price trend is favorable for selling now.",
  modelVersion: "ensemble-v1.0",
  generatedAt: new Date().toISOString(),
};

export default function DashboardPage() {
  const locale = useUIStore((s) => s.locale);
  const { lastRecommendation, setRecommendation, isLoading, setLoading } =
    useRecommendationStore();
  const [error, setError] = useState<string | null>(null);

  const recommendation = lastRecommendation || SAMPLE_RECOMMENDATION;

  const handleGetRecommendation = async (data: {
    crop: string;
    quantityKg: number;
    mandiId?: string;
  }) => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchRecommendation({
        farmerProfile: {
          location: { lat: 28.6139, lng: 77.209 },
          transportCostPerKg: 1.5,
          storageCostPerKgPerDay: 0.5,
          estimatedLossPct: 5,
        },
        crop: data.crop,
        quantityKg: data.quantityKg,
        predictionWindowDays: 7,
      });
      setRecommendation(result);
    } catch (err) {
      console.error("Recommendation error:", err);
      setError(t("common.error", locale));
      // Show sample data on error (offline-friendly)
      setRecommendation(SAMPLE_RECOMMENDATION);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--color-cream-white)" }}>
      {/* ─── Hero Section ─── */}
      <section
        className="section"
        style={{
          background: "linear-gradient(135deg, var(--color-light-green-tint) 0%, var(--color-cream-white) 60%)",
          paddingBottom: "60px",
        }}
      >
        <div className="container-main">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left: Content */}
            <div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full mb-6 text-sm font-medium"
                  style={{
                    backgroundColor: "var(--color-light-green-tint)",
                    color: "var(--color-deep-farm-green)",
                  }}
                >
                  <Sprout className="w-4 h-4" />
                  {t("app.tagline", locale)}
                </div>

                <h1
                  className="mb-4"
                  style={{ color: "var(--color-deep-farm-green)", lineHeight: 1.15 }}
                >
                  {t("hero.headline", locale)}
                </h1>

                <p
                  className="text-lg mb-8"
                  style={{ color: "var(--color-secondary-text)", lineHeight: 1.6 }}
                >
                  {t("hero.subtext", locale)}
                </p>
              </motion.div>

              {/* Input Module */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2, duration: 0.6 }}
              >
                <div className="card">
                  <InputModule
                    onSubmit={handleGetRecommendation}
                    isLoading={isLoading}
                  />
                </div>
              </motion.div>

              {error && (
                <p className="mt-3 text-sm" style={{ color: "var(--color-loss-red)" }}>
                  {error}
                </p>
              )}
            </div>

            {/* Right: DecisionCard */}
            <div>
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
              >
                <DecisionCard
                  decision={recommendation.decision as "SELL NOW" | "HOLD"}
                  expectedNetProfit={recommendation.expectedNetProfit}
                  recommendedMandi={recommendation.recommendedMandi}
                  confidence={recommendation.confidence}
                  rationaleText={recommendation.rationaleText}
                  onAction={() => {
                    const el = document.getElementById("multi-mandi-list");
                    el?.scrollIntoView({ behavior: "smooth" });
                  }}
                />
              </motion.div>

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-3 mt-4">
                {[
                  {
                    icon: TrendingUp,
                    label: "Price Trend",
                    value: "+8.2%",
                    color: "var(--color-profit-green)",
                  },
                  {
                    icon: Shield,
                    label: "Accuracy",
                    value: "82%",
                    color: "var(--color-deep-farm-green)",
                  },
                  {
                    icon: Sprout,
                    label: "Mandis",
                    value: "3",
                    color: "var(--color-fresh-leaf-green)",
                  },
                ].map((stat, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + i * 0.1 }}
                    className="card text-center p-3"
                  >
                    <stat.icon
                      className="w-5 h-5 mx-auto mb-1"
                      style={{ color: stat.color }}
                    />
                    <p
                      className="text-lg font-bold"
                      style={{ fontFamily: "var(--font-heading)", color: stat.color }}
                    >
                      {stat.value}
                    </p>
                    <p className="text-xs" style={{ color: "var(--color-secondary-text)" }}>
                      {stat.label}
                    </p>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── Multi-Mandi Comparison ─── */}
      <section className="section" style={{ paddingTop: "60px" }}>
        <div className="container-main">
          <MultiMandiList
            recommendedMandi={{
              ...recommendation.recommendedMandi,
              expectedNetProfit: recommendation.expectedNetProfit,
            }}
            alternativeMandis={recommendation.alternativeMandis}
          />
        </div>
      </section>
    </div>
  );
}
