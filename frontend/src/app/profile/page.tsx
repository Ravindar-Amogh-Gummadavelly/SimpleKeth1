// SimpleKeth — Farmer Profile Page
// Edit farmer profile: crop, quantity, location, transport/storage parameters

"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { User, Save, Check } from "lucide-react";
import { useUIStore, useFarmerStore } from "@/lib/store";
import { t, locales, type Locale } from "@/i18n/config";

export default function ProfilePage() {
  const locale = useUIStore((s) => s.locale);
  const setLocale = useUIStore((s) => s.setLocale);
  const { farmer, setFarmer } = useFarmerStore();
  const [saved, setSaved] = useState(false);

  const [form, setForm] = useState({
    name: farmer?.name || "",
    phone: farmer?.phone || "",
    email: farmer?.email || "",
    language: farmer?.language || locale,
    primaryCrop: farmer?.profile?.primaryCrop || "onion",
    locationName: farmer?.profile?.locationName || "",
    transportCostPerKg: farmer?.profile?.transportCostPerKg ?? 1.5,
    storageCostPerKgDay: farmer?.profile?.storageCostPerKgDay ?? 0.5,
    estimatedLossPct: farmer?.profile?.estimatedLossPct ?? 5,
    avgQuantityKg: farmer?.profile?.avgQuantityKg ?? 500,
  });

  const handleSave = async () => {
    try {
        const { createFarmer, updateFarmer, updateFarmerProfile } = await import("@/lib/api");
        
        let activeId = farmer?.id;
        
        if (!activeId || activeId === "local-user") {
            const newFarmer = await createFarmer({
                name: form.name,
                phone: form.phone,
                email: form.email,
                language: form.language,
            });
            activeId = newFarmer.id;
        } else {
            await updateFarmer(activeId, {
                name: form.name,
                phone: form.phone,
                email: form.email,
                language: form.language,
            });
        }
        
        // Push profile metrics to backend
        await updateFarmerProfile(activeId, {
            primaryCrop: form.primaryCrop,
            locationName: form.locationName,
            transportCostPerKg: form.transportCostPerKg,
            storageCostPerKgDay: form.storageCostPerKgDay,
            estimatedLossPct: form.estimatedLossPct,
            avgQuantityKg: form.avgQuantityKg,
        });

        setFarmer({
            id: activeId,
            name: form.name,
            phone: form.phone,
            email: form.email,
            language: form.language as Locale,
            profile: {
                primaryCrop: form.primaryCrop,
                locationName: form.locationName,
                transportCostPerKg: form.transportCostPerKg,
                storageCostPerKgDay: form.storageCostPerKgDay,
                estimatedLossPct: form.estimatedLossPct,
                avgQuantityKg: form.avgQuantityKg,
            },
        });

        setLocale(form.language as Locale);
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    } catch (e) {
        console.error("Failed to save to backend:", e);
        // Fallback to offline mode
        setFarmer({
            id: "local-user",
            name: form.name,
            phone: form.phone,
            email: form.email,
            language: form.language as Locale,
            profile: {
                primaryCrop: form.primaryCrop,
                locationName: form.locationName,
                transportCostPerKg: form.transportCostPerKg,
                storageCostPerKgDay: form.storageCostPerKgDay,
                estimatedLossPct: form.estimatedLossPct,
                avgQuantityKg: form.avgQuantityKg,
            },
        });
        setLocale(form.language as Locale);
        alert("Saved offline. Backend unreachable.");
    }
  };

  const inputClass = "input-field";

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--color-cream-white)" }}>
      <div className="container-main section" style={{ maxWidth: "700px" }}>
        <h1 className="mb-2" style={{ color: "var(--color-deep-farm-green)", fontSize: "34px" }}>
          <User className="w-8 h-8 inline mr-2" />
          {t("profile.title", locale)}
        </h1>
        <p className="mb-8" style={{ color: "var(--color-secondary-text)" }}>
          {t("profile.subtitle", locale)}
        </p>

        <div className="card">
          <div className="flex flex-col gap-5">
            {/* Name */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("profile.name", locale)}</label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                className={inputClass}
                placeholder="Enter your name"
              />
            </div>

            {/* Phone */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("profile.phone", locale)}</label>
              <input
                type="tel"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
                className={inputClass}
                placeholder="+91 98765 43210"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("profile.email", locale)}</label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className={inputClass}
                placeholder="email@example.com"
              />
            </div>

            {/* Language */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("profile.language", locale)}</label>
              <select
                value={form.language}
                onChange={(e) => setForm({ ...form, language: e.target.value as Locale })}
                className={inputClass}
              >
                {(Object.entries(locales) as [Locale, string][]).map(([key, label]) => (
                  <option key={key} value={key}>{label}</option>
                ))}
              </select>
            </div>

            <hr style={{ borderColor: "var(--color-border)" }} />

            {/* Primary Crop */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("profile.primaryCrop", locale)}</label>
              <select
                value={form.primaryCrop}
                onChange={(e) => setForm({ ...form, primaryCrop: e.target.value })}
                className={inputClass}
              >
                <option value="onion">Onion / प्याज / ఉల్లిపాయ</option>
                <option value="rice">Rice / चावल / బియ్యం</option>
                <option value="wheat">Wheat / गेहूं / గోధుమ</option>
                <option value="tomato">Tomato / टमाटर / టమాటా</option>
                <option value="potato">Potato / आलू / బంగాళాదుంప</option>
              </select>
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("input.quantity", locale)}</label>
              <input
                type="number"
                value={form.avgQuantityKg}
                onChange={(e) => setForm({ ...form, avgQuantityKg: parseFloat(e.target.value) || 0 })}
                className={inputClass}
              />
            </div>

            {/* Transport Cost */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("simulator.transportCost", locale)}</label>
              <input
                type="number"
                step="0.1"
                value={form.transportCostPerKg}
                onChange={(e) => setForm({ ...form, transportCostPerKg: parseFloat(e.target.value) || 0 })}
                className={inputClass}
              />
            </div>

            {/* Storage Cost */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("simulator.storageCost", locale)}</label>
              <input
                type="number"
                step="0.1"
                value={form.storageCostPerKgDay}
                onChange={(e) => setForm({ ...form, storageCostPerKgDay: parseFloat(e.target.value) || 0 })}
                className={inputClass}
              />
            </div>

            {/* Loss % */}
            <div>
              <label className="block text-sm font-semibold mb-1.5">{t("simulator.lossPct", locale)}</label>
              <input
                type="number"
                step="0.5"
                value={form.estimatedLossPct}
                onChange={(e) => setForm({ ...form, estimatedLossPct: parseFloat(e.target.value) || 0 })}
                className={inputClass}
              />
            </div>

            {/* Save Button */}
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleSave}
              className="btn-primary"
            >
              {saved ? (
                <>
                  <Check className="w-5 h-5" />
                  Saved!
                </>
              ) : (
                <>
                  <Save className="w-5 h-5" />
                  {t("profile.save", locale)}
                </>
              )}
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  );
}
