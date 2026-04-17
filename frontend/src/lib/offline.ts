// SimpleKeth — Offline/IndexedDB Module
// Store farmer profile, predictions, and recommendations for offline display

import { openDB, type IDBPDatabase } from "idb";
import type { PredictionResponse, RecommendationResponse, Farmer } from "@/types";

const DB_NAME = "simpleketh-offline";
const DB_VERSION = 1;

interface SimpleKethDB {
  farmerProfile: {
    key: string;
    value: Farmer;
  };
  predictions: {
    key: string;
    value: PredictionResponse & { storedAt: string };
  };
  recommendations: {
    key: string;
    value: RecommendationResponse & { storedAt: string };
  };
}

let dbInstance: IDBPDatabase<SimpleKethDB> | null = null;

async function getDB(): Promise<IDBPDatabase<SimpleKethDB>> {
  if (dbInstance) return dbInstance;

  dbInstance = await openDB<SimpleKethDB>(DB_NAME, DB_VERSION, {
    upgrade(db) {
      if (!db.objectStoreNames.contains("farmerProfile")) {
        db.createObjectStore("farmerProfile");
      }
      if (!db.objectStoreNames.contains("predictions")) {
        db.createObjectStore("predictions");
      }
      if (!db.objectStoreNames.contains("recommendations")) {
        db.createObjectStore("recommendations");
      }
    },
  });

  return dbInstance;
}

// ─── Farmer Profile ─────────────────────────────────

export async function saveFarmerOffline(farmer: Farmer): Promise<void> {
  const db = await getDB();
  await db.put("farmerProfile", farmer, "current");
}

export async function getFarmerOffline(): Promise<Farmer | undefined> {
  const db = await getDB();
  return db.get("farmerProfile", "current");
}

// ─── Predictions ────────────────────────────────────

export async function savePredictionOffline(
  key: string,
  prediction: PredictionResponse
): Promise<void> {
  const db = await getDB();
  await db.put(
    "predictions",
    { ...prediction, storedAt: new Date().toISOString() },
    key
  );

  // Keep only last 7 predictions
  const allKeys = await db.getAllKeys("predictions");
  if (allKeys.length > 7) {
    const keysToDelete = allKeys.slice(0, allKeys.length - 7);
    for (const k of keysToDelete) {
      await db.delete("predictions", k);
    }
  }
}

export async function getPredictionOffline(
  key: string
): Promise<(PredictionResponse & { storedAt: string }) | undefined> {
  const db = await getDB();
  return db.get("predictions", key);
}

export async function getAllPredictionsOffline(): Promise<
  (PredictionResponse & { storedAt: string })[]
> {
  const db = await getDB();
  return db.getAll("predictions");
}

// ─── Recommendations ────────────────────────────────

export async function saveRecommendationOffline(
  recommendation: RecommendationResponse
): Promise<void> {
  const db = await getDB();
  await db.put(
    "recommendations",
    { ...recommendation, storedAt: new Date().toISOString() },
    "latest"
  );
}

export async function getRecommendationOffline(): Promise<
  (RecommendationResponse & { storedAt: string }) | undefined
> {
  const db = await getDB();
  return db.get("recommendations", "latest");
}
