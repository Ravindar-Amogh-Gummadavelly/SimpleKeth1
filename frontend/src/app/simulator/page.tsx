// SimpleKeth — Scenario Simulator Page
// Adjust transport, storage, loss parameters and see recalculated net profit

"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Calculator, RefreshCw } from "lucide-react";
import { useUIStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { formatCurrency, calculateNetProfit } from "@/lib/utils";

export default function SimulatorPage() {
  const locale = useUIStore((s) => s.locale);

  const [params, setParams] = useState({
    predictedPrice: 1200,
    quantityKg: 500,
    transportCostPerKg: 1.5,
    storageCostPerKgPerDay: 0.5,
    estimatedLossPct: 5,
    commissionPct: 2.5,
    distanceKm: 25,
    storageDays: 0,
  });

  const netProfit = calculateNetProfit(params);

  const handleChange = (field: string, value: number) => {
    setParams((prev) => ({ ...prev, [field]: value }));
  };

  const fields = [
    { key: "predictedPrice", label: "Predicted Price (₹/quintal)", min: 100, max: 5000, step: 50 },
    { key: "quantityKg", label: t("input.quantity", locale), min: 10, max: 50000, step: 50 },
    { key: "transportCostPerKg", label: t("simulator.transportCost", locale), min: 0, max: 10, step: 0.1 },
    { key: "storageCostPerKgPerDay", label: t("simulator.storageCost", locale), min: 0, max: 5, step: 0.1 },
    { key: "estimatedLossPct", label: t("simulator.lossPct", locale), min: 0, max: 30, step: 0.5 },
    { key: "storageDays", label: t("simulator.storageDays", locale), min: 0, max: 30, step: 1 },
    { key: "distanceKm", label: "Distance (km)", min: 1, max: 500, step: 5 },
    { key: "commissionPct", label: "Commission (%)", min: 0, max: 10, step: 0.5 },
  ];

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--color-cream-white)" }}>
      <div className="container-main section">
        <h1 className="mb-2" style={{ color: "var(--color-deep-farm-green)", fontSize: "34px" }}>
          <Calculator className="w-8 h-8 inline mr-2" />
          {t("simulator.title", locale)}
        </h1>
        <p className="mb-8" style={{ color: "var(--color-secondary-text)" }}>
          {t("simulator.subtitle", locale)}
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Sliders */}
          <div className="lg:col-span-2">
            <div className="card">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {fields.map((field) => (
                  <div key={field.key}>
                    <label className="block text-sm font-medium mb-1" style={{ color: "var(--color-primary-text)" }}>
                      {field.label}
                    </label>
                    <div className="flex items-center gap-3">
                      <input
                        type="range"
                        min={field.min}
                        max={field.max}
                        step={field.step}
                        value={params[field.key as keyof typeof params]}
                        onChange={(e) => handleChange(field.key, parseFloat(e.target.value))}
                        className="flex-1 accent-[#4E7C4F]"
                        style={{ height: "6px" }}
                      />
                      <input
                        type="number"
                        min={field.min}
                        max={field.max}
                        step={field.step}
                        value={params[field.key as keyof typeof params]}
                        onChange={(e) => handleChange(field.key, parseFloat(e.target.value) || 0)}
                        className="input-field w-24 text-center text-sm p-2"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Result */}
          <div>
            <motion.div
              key={netProfit}
              initial={{ scale: 0.95, opacity: 0.8 }}
              animate={{ scale: 1, opacity: 1 }}
              className="card text-center"
              style={{
                borderTop: `4px solid ${netProfit > 0 ? "var(--color-profit-green)" : "var(--color-loss-red)"}`,
              }}
            >
              <p className="text-sm font-medium mb-2" style={{ color: "var(--color-secondary-text)" }}>
                {t("simulator.netProfit", locale)}
              </p>
              <p
                className="profit-display mb-4"
                style={{
                  color: netProfit > 0 ? "var(--color-profit-green)" : "var(--color-loss-red)",
                  fontSize: "42px",
                }}
              >
                {formatCurrency(netProfit)}
              </p>

              {/* Breakdown */}
              <div className="text-left space-y-2 text-sm">
                <div className="flex justify-between" style={{ color: "var(--color-secondary-text)" }}>
                  <span>Gross Revenue</span>
                  <span className="font-medium">{formatCurrency((params.predictedPrice / 100) * params.quantityKg * (1 - params.estimatedLossPct / 100))}</span>
                </div>
                <div className="flex justify-between" style={{ color: "var(--color-loss-red)" }}>
                  <span>Transport</span>
                  <span>-{formatCurrency(params.transportCostPerKg * params.quantityKg * (params.distanceKm / 50))}</span>
                </div>
                <div className="flex justify-between" style={{ color: "var(--color-loss-red)" }}>
                  <span>Storage</span>
                  <span>-{formatCurrency(params.storageCostPerKgPerDay * params.quantityKg * params.storageDays)}</span>
                </div>
                <div className="flex justify-between" style={{ color: "var(--color-loss-red)" }}>
                  <span>Commission</span>
                  <span>-{formatCurrency(((params.predictedPrice / 100) * params.quantityKg * (1 - params.estimatedLossPct / 100)) * params.commissionPct / 100)}</span>
                </div>
                <hr style={{ borderColor: "var(--color-border)" }} />
                <div className="flex justify-between font-bold" style={{ color: "var(--color-primary-text)" }}>
                  <span>Net Profit</span>
                  <span style={{ color: netProfit > 0 ? "var(--color-profit-green)" : "var(--color-loss-red)" }}>
                    {formatCurrency(netProfit)}
                  </span>
                </div>
              </div>

              <button
                onClick={() =>
                  setParams({
                    predictedPrice: 1200,
                    quantityKg: 500,
                    transportCostPerKg: 1.5,
                    storageCostPerKgPerDay: 0.5,
                    estimatedLossPct: 5,
                    commissionPct: 2.5,
                    distanceKm: 25,
                    storageDays: 0,
                  })
                }
                className="mt-4 flex items-center gap-2 mx-auto text-sm font-medium px-4 py-2 rounded-lg transition-colors hover:bg-[var(--color-light-green-tint)]"
                style={{ color: "var(--color-deep-farm-green)" }}
              >
                <RefreshCw className="w-4 h-4" />
                Reset
              </button>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
