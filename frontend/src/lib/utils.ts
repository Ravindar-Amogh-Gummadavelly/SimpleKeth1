// SimpleKeth — Utility Functions

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes with clsx */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/** Format number as Indian currency (₹) */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

/** Format number with Indian number system (lakhs, crores) */
export function formatNumber(num: number): string {
  return new Intl.NumberFormat("en-IN").format(num);
}

/** Format distance in km */
export function formatDistance(km: number): string {
  return `${km.toFixed(1)} km`;
}

/** Format confidence as percentage */
export function formatConfidence(confidence: number): string {
  return `${Math.round(confidence * 100)}%`;
}

/** Format date for display */
export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

/** Calculate net profit */
export function calculateNetProfit({
  predictedPrice,
  quantityKg,
  transportCostPerKg,
  storageCostPerKgPerDay,
  estimatedLossPct,
  commissionPct,
  distanceKm,
  storageDays = 0,
}: {
  predictedPrice: number;
  quantityKg: number;
  transportCostPerKg: number;
  storageCostPerKgPerDay: number;
  estimatedLossPct: number;
  commissionPct: number;
  distanceKm: number;
  storageDays?: number;
}): number {
  const effectiveQty = quantityKg * (1 - estimatedLossPct / 100);
  const grossRevenue = (predictedPrice / 100) * effectiveQty;
  const transportCost = transportCostPerKg * quantityKg * (distanceKm / 50);
  const storageCost = storageCostPerKgPerDay * quantityKg * storageDays;
  const commission = grossRevenue * (commissionPct / 100);
  return grossRevenue - transportCost - storageCost - commission;
}
