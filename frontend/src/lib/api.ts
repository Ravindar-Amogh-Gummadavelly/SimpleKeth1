// SimpleKeth — API Client
// Typed API functions with TanStack Query hooks

import type {
  PredictionRequest,
  PredictionResponse,
  RecommendationRequest,
  RecommendationResponse,
  NotifyRequest,
  NotifyResponse,
  Farmer,
  Mandi,
  Crop,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

// ─── Base Fetch ─────────────────────────────────────

async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => "Unknown error");
    throw new Error(`API Error ${res.status}: ${errorText}`);
  }

  return res.json() as Promise<T>;
}

// ─── Prediction API ─────────────────────────────────

export async function fetchPrediction(
  request: PredictionRequest
): Promise<PredictionResponse> {
  return apiFetch<PredictionResponse>("/predict", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

// ─── Recommendation API ─────────────────────────────

export async function fetchRecommendation(
  request: RecommendationRequest
): Promise<RecommendationResponse> {
  return apiFetch<RecommendationResponse>("/recommend", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

// ─── Notification API ───────────────────────────────

export async function sendNotification(
  request: NotifyRequest
): Promise<NotifyResponse> {
  return apiFetch<NotifyResponse>("/notify", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

// ─── Profile API ────────────────────────────────────

export async function createFarmer(data: {
  name: string;
  phone: string;
  email?: string;
  language?: string;
}): Promise<Farmer> {
  return apiFetch<Farmer>("/farmers", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getFarmer(farmerId: string): Promise<Farmer> {
  return apiFetch<Farmer>(`/farmers/${farmerId}`);
}

export async function updateFarmer(
  farmerId: string,
  data: Partial<Farmer>
): Promise<Farmer> {
  return apiFetch<Farmer>(`/farmers/${farmerId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function updateFarmerProfile(
  farmerId: string,
  profile: Record<string, unknown>
): Promise<Farmer> {
  return apiFetch<Farmer>(`/farmers/${farmerId}/profile`, {
    method: "PUT",
    body: JSON.stringify(profile),
  });
}

// ─── Reference Data ─────────────────────────────────

export async function fetchMandis(): Promise<Mandi[]> {
  return apiFetch<Mandi[]>("/mandis");
}

export async function fetchCrops(): Promise<Crop[]> {
  return apiFetch<Crop[]>("/crops");
}
