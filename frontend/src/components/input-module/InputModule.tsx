// SimpleKeth — InputModule Component
// Crop dropdown, quantity input, mandi search — React Hook Form + Zod

"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2, Search, Wheat } from "lucide-react";
import { useUIStore, useRecommendationStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { cn } from "@/lib/utils";

const inputSchema = z.object({
  crop: z.string().min(1, "Please select a crop"),
  quantityKg: z.number().min(1, "Quantity must be greater than 0").max(100000),
  mandiId: z.string().optional(),
});

type InputFormData = z.infer<typeof inputSchema>;

const CROPS = [
  { value: "onion", label: "Onion", labelHi: "प्याज", labelTe: "ఉల్లిపాయ" },
  { value: "rice", label: "Rice", labelHi: "चावल", labelTe: "బియ్యం" },
  { value: "wheat", label: "Wheat", labelHi: "गेहूं", labelTe: "గోధుమ" },
  { value: "tomato", label: "Tomato", labelHi: "टमाटर", labelTe: "టమాటా" },
  { value: "potato", label: "Potato", labelHi: "आलू", labelTe: "బంగాళాదుంప" },
];

const MANDIS = [
  { id: "M001", name: "Azadpur Mandi, Delhi" },
  { id: "M002", name: "Lasalgaon Mandi, Maharashtra" },
  { id: "M003", name: "Pimpalgaon Mandi, Maharashtra" },
];

interface InputModuleProps {
  onSubmit: (data: InputFormData) => void;
  isLoading?: boolean;
  className?: string;
}

export function InputModule({ onSubmit, isLoading, className }: InputModuleProps) {
  const locale = useUIStore((s) => s.locale);
  const { quickInput, setQuickInput } = useRecommendationStore();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<InputFormData>({
    resolver: zodResolver(inputSchema),
    defaultValues: {
      crop: quickInput.crop || "onion",
      quantityKg: quickInput.quantityKg || 500,
      mandiId: quickInput.mandiId || "",
    },
  });

  const handleFormSubmit = (data: InputFormData) => {
    setQuickInput({
      crop: data.crop,
      quantityKg: data.quantityKg,
      mandiId: data.mandiId,
    });
    onSubmit(data);
  };

  const getCropLabel = (crop: typeof CROPS[0]) => {
    if (locale === "hi") return crop.labelHi;
    if (locale === "te") return crop.labelTe;
    return crop.label;
  };

  return (
    <form
      onSubmit={handleSubmit(handleFormSubmit)}
      className={cn("flex flex-col gap-4", className)}
      id="input-module"
    >
      {/* Crop Dropdown */}
      <div>
        <label
          htmlFor="crop-select"
          className="block text-sm font-semibold mb-1.5"
          style={{ color: "var(--color-primary-text)" }}
        >
          <Wheat className="w-4 h-4 inline mr-1" style={{ color: "var(--color-fresh-leaf-green)" }} />
          {t("input.selectCrop", locale)}
        </label>
        <select
          id="crop-select"
          {...register("crop")}
          className="input-field"
          style={{ cursor: "pointer" }}
        >
          {CROPS.map((crop) => (
            <option key={crop.value} value={crop.value}>
              {getCropLabel(crop)}
            </option>
          ))}
        </select>
        {errors.crop && (
          <p className="text-sm mt-1" style={{ color: "var(--color-loss-red)" }}>
            {errors.crop.message}
          </p>
        )}
      </div>

      {/* Quantity Input */}
      <div>
        <label
          htmlFor="quantity-input"
          className="block text-sm font-semibold mb-1.5"
          style={{ color: "var(--color-primary-text)" }}
        >
          {t("input.quantity", locale)}
        </label>
        <input
          id="quantity-input"
          type="number"
          {...register("quantityKg", { valueAsNumber: true })}
          className="input-field"
          placeholder={t("input.quantityPlaceholder", locale)}
          min={1}
          max={100000}
        />
        {errors.quantityKg && (
          <p className="text-sm mt-1" style={{ color: "var(--color-loss-red)" }}>
            {errors.quantityKg.message}
          </p>
        )}
      </div>

      {/* Mandi Selector */}
      <div>
        <label
          htmlFor="mandi-select"
          className="block text-sm font-semibold mb-1.5"
          style={{ color: "var(--color-primary-text)" }}
        >
          <Search className="w-4 h-4 inline mr-1" style={{ color: "var(--color-fresh-leaf-green)" }} />
          {t("input.location", locale)}
        </label>
        <select
          id="mandi-select"
          {...register("mandiId")}
          className="input-field"
          style={{ cursor: "pointer" }}
        >
          <option value="">{t("input.locationPlaceholder", locale)}</option>
          {MANDIS.map((mandi) => (
            <option key={mandi.id} value={mandi.id}>
              {mandi.name}
            </option>
          ))}
        </select>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        className="btn-primary"
        disabled={isLoading}
        id="get-recommendation-btn"
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            {t("common.loading", locale)}
          </>
        ) : (
          <>
            <Search className="w-5 h-5" />
            {t("input.getRecommendation", locale)}
          </>
        )}
      </button>
    </form>
  );
}
