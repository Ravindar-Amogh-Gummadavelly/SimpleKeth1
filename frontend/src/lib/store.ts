// SimpleKeth — Zustand Stores
// Global state management for farmer profile, recommendations, and UI state

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  Farmer,
  FarmerProfile,
  RecommendationResponse,
  PredictionResponse,
  QuickInputState,
} from "@/types";
import type { Locale } from "@/i18n/config";

// ─── Farmer Store ───────────────────────────────────

interface FarmerState {
  farmer: Farmer | null;
  setFarmer: (farmer: Farmer | null) => void;
  updateProfile: (profile: Partial<FarmerProfile>) => void;
}

export const useFarmerStore = create<FarmerState>()(
  persist(
    (set) => ({
      farmer: null,
      setFarmer: (farmer) => set({ farmer }),
      updateProfile: (profile) =>
        set((state) => ({
          farmer: state.farmer
            ? {
                ...state.farmer,
                profile: { ...state.farmer.profile, ...profile } as FarmerProfile,
              }
            : null,
        })),
    }),
    { name: "simpleketh-farmer" }
  )
);

// ─── Recommendation Store ───────────────────────────

interface RecommendationState {
  lastRecommendation: RecommendationResponse | null;
  lastPredictions: PredictionResponse | null;
  quickInput: QuickInputState;
  isLoading: boolean;
  setRecommendation: (rec: RecommendationResponse | null) => void;
  setPredictions: (pred: PredictionResponse | null) => void;
  setQuickInput: (input: Partial<QuickInputState>) => void;
  setLoading: (loading: boolean) => void;
}

export const useRecommendationStore = create<RecommendationState>()(
  persist(
    (set) => ({
      lastRecommendation: null,
      lastPredictions: null,
      quickInput: {
        crop: "onion",
        quantityKg: 500,
        locationName: "",
        mandiId: undefined,
      },
      isLoading: false,
      setRecommendation: (rec) => set({ lastRecommendation: rec }),
      setPredictions: (pred) => set({ lastPredictions: pred }),
      setQuickInput: (input) =>
        set((state) => ({ quickInput: { ...state.quickInput, ...input } })),
      setLoading: (loading) => set({ isLoading: loading }),
    }),
    { name: "simpleketh-recommendation" }
  )
);

// ─── UI / Locale Store ──────────────────────────────

interface UIState {
  locale: Locale;
  isOffline: boolean;
  sidebarOpen: boolean;
  setLocale: (locale: Locale) => void;
  setOffline: (offline: boolean) => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>()(
  persist(
    (set) => ({
      locale: "en",
      isOffline: false,
      sidebarOpen: false,
      setLocale: (locale) => set({ locale }),
      setOffline: (offline) => set({ isOffline: offline }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
    }),
    { name: "simpleketh-ui" }
  )
);
