// SimpleKeth — TypeScript types matching API contracts

// ─── Prediction API ─────────────────────────────────

export interface FeatureExplanation {
  feature: string;
  impact: number;
}

export interface SinglePrediction {
  mandiId: string;
  mandiName: string;
  date: string;
  predictedPrice: number;
  priceCurrency: string;
  confidence: number;
  explanation: FeatureExplanation[];
}

export interface PredictionRequest {
  farmerId?: string;
  crop: string;
  mandiId?: string;
  date?: string;
  quantityKg?: number;
}

export interface PredictionResponse {
  predictions: SinglePrediction[];
  modelVersion: string;
  generatedAt: string;
}

// ─── Recommendation API ─────────────────────────────

export interface FarmerLocation {
  lat: number;
  lng: number;
}

export interface FarmerProfileInput {
  id?: string;
  location: FarmerLocation;
  transportCostPerKg: number;
  storageCostPerKgPerDay: number;
  estimatedLossPct: number;
}

export interface RecommendationRequest {
  farmerProfile: FarmerProfileInput;
  crop: string;
  quantityKg: number;
  predictionWindowDays?: number;
}

export interface RecommendedMandi {
  id: string;
  name: string;
  distanceKm: number;
}

export interface AlternativeMandi {
  id: string;
  name: string;
  expectedNetProfit: number;
  distanceKm: number;
}

export type Decision = "SELL NOW" | "HOLD";

export interface RecommendationResponse {
  decision: Decision;
  recommendedMandi: RecommendedMandi;
  expectedNetProfit: number;
  alternativeMandis: AlternativeMandi[];
  confidence: number;
  rationaleText: string;
  modelVersion: string;
  generatedAt: string;
}

// ─── Notification API ───────────────────────────────

export type NotificationChannel = "sms" | "push" | "voice";

export interface NotifyRequest {
  farmerId: string;
  channel: NotificationChannel;
  message: string;
  payload?: Record<string, unknown>;
}

export interface NotifyResponse {
  success: boolean;
  notificationId: string;
  channel: string;
  status: "sent" | "queued" | "failed";
  message: string;
}

// ─── Farmer Profile ─────────────────────────────────

export interface Farmer {
  id: string;
  name: string;
  phone: string;
  email?: string;
  language: "en" | "hi" | "te";
  profile?: FarmerProfile;
}

export interface FarmerProfile {
  locationLat?: number;
  locationLng?: number;
  locationName?: string;
  primaryCrop?: string;
  secondaryCrops?: string[];
  avgQuantityKg?: number;
  transportCostPerKg: number;
  storageCostPerKgDay: number;
  estimatedLossPct: number;
  preferredMandis?: string[];
}

// ─── Mandi & Crop ───────────────────────────────────

export interface Mandi {
  id: string;
  code: string;
  name: string;
  state: string;
  district: string;
  latitude: number;
  longitude: number;
}

export interface Crop {
  name: string;
  category: string;
  nameHi: string;
  nameTe: string;
}

// ─── UI State ───────────────────────────────────────

export interface QuickInputState {
  crop: string;
  quantityKg: number;
  locationName: string;
  mandiId?: string;
}
