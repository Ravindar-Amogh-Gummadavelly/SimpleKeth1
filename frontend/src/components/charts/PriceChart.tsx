// SimpleKeth — PriceChart Component
// Lightweight line chart for price trends (7/14/30 day toggle)

"use client";

import { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useUIStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { cn } from "@/lib/utils";

interface PriceDataPoint {
  date: string;
  actualPrice?: number;
  predictedPrice?: number;
}

interface PriceChartProps {
  data: PriceDataPoint[];
  className?: string;
}

const periodOptions = [
  { value: 7, labelKey: "trends.days7" },
  { value: 14, labelKey: "trends.days14" },
  { value: 30, labelKey: "trends.days30" },
];

export function PriceChart({ data, className }: PriceChartProps) {
  const locale = useUIStore((s) => s.locale);
  const [period, setPeriod] = useState(7);

  const filteredData = data.slice(-period);

  return (
    <div className={cn("card", className)} id="price-chart">
      {/* Period Toggle */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg" style={{ color: "var(--color-deep-farm-green)" }}>
          {t("trends.title", locale)}
        </h3>
        <div className="flex gap-1">
          {periodOptions.map((opt) => (
            <button
              key={opt.value}
              onClick={() => setPeriod(opt.value)}
              className={cn(
                "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
              )}
              style={{
                backgroundColor:
                  period === opt.value
                    ? "var(--color-deep-farm-green)"
                    : "var(--color-soft-earth)",
                color:
                  period === opt.value ? "white" : "var(--color-secondary-text)",
              }}
            >
              {t(opt.labelKey, locale)}
            </button>
          ))}
        </div>
      </div>

      {/* Chart */}
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={filteredData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12, fill: "var(--color-secondary-text)" }}
              tickFormatter={(val) => {
                const d = new Date(val);
                return `${d.getDate()}/${d.getMonth() + 1}`;
              }}
            />
            <YAxis
              tick={{ fontSize: 12, fill: "var(--color-secondary-text)" }}
              tickFormatter={(val) => `₹${val}`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "white",
                border: "1px solid var(--color-border)",
                borderRadius: "8px",
                fontSize: "14px",
              }}
              formatter={(value, name) => [
                `₹${value}`,
                name === "actualPrice"
                  ? t("trends.actual", locale)
                  : t("trends.predicted", locale),
              ]}
            />
            <Legend
              formatter={(value) =>
                value === "actualPrice"
                  ? t("trends.actual", locale)
                  : t("trends.predicted", locale)
              }
            />
            <Line
              type="monotone"
              dataKey="actualPrice"
              stroke="var(--color-deep-farm-green)"
              strokeWidth={2}
              dot={{ r: 3 }}
              name="actualPrice"
            />
            <Line
              type="monotone"
              dataKey="predictedPrice"
              stroke="var(--color-profit-green)"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ r: 3 }}
              name="predictedPrice"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
