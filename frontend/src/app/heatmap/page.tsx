// SimpleKeth — Mandi Heatmap Page
// Visualizes price trends and profitability dynamically

"use client";

import dynamic from "next/dynamic";
import { MapPin } from "lucide-react";
import { useUIStore, useFarmerStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { useQuery } from "@tanstack/react-query";
import { fetchRecommendation } from "@/lib/api";

// Dynamically import the map to avoid SSR mapping window errors
const MapComponent = dynamic(() => import("@/components/heatmap/MapComponent"), { ssr: false });

export default function HeatmapPage() {
  const locale = useUIStore((s) => s.locale);
  const farmerProfile = useFarmerStore((s) => s.farmer?.profile);

  const { data: recommendation, isLoading } = useQuery({
    queryKey: ["heatmapRecommendation", farmerProfile],
    queryFn: () => fetchRecommendation({
        farmerProfile: {
            location: { lat: 20.5937, lng: 78.9629 }, // Default to Central India
            transportCostPerKg: farmerProfile?.transportCostPerKg || 1.5,
            storageCostPerKgDay: farmerProfile?.storageCostPerKgDay || 0.5,
            estimatedLossPct: farmerProfile?.estimatedLossPct || 5,
        },
        crop: farmerProfile?.primaryCrop || "onion",
        quantityKg: farmerProfile?.avgQuantityKg || 500,
        predictionWindowDays: 7,
    }),
    refetchInterval: false,
    refetchOnWindowFocus: false,
  });

  // Convert the recommendations into map markers
  const mapData = [];
  if (recommendation) {
      // 1. Plot the best Mandi
      mapData.push({
          id: recommendation.recommendedMandi.mandiId,
          name: recommendation.recommendedMandi.name,
          lat: recommendation.recommendedMandi.location.lat,
          lng: recommendation.recommendedMandi.location.lng,
          expectedProfit: recommendation.expectedNetProfit,
          rank: 1,
      });

      // 2. Plot alternative Mandis
      recommendation.alternativeMandis.forEach((alt, idx) => {
          mapData.push({
             id: alt.mandi.mandiId,
             name: alt.mandi.name,
             lat: alt.mandi.location.lat,
             lng: alt.mandi.location.lng,
             expectedProfit: alt.expectedNetProfit,
             rank: idx + 2, 
          });
      });
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--color-cream-white)" }}>
      <div className="container-main section">
        <div className="flex justify-between items-end mb-8">
            <div>
                <h1 className="mb-2" style={{ color: "var(--color-deep-farm-green)", fontSize: "34px" }}>
                <MapPin className="w-8 h-8 inline mr-2" />
                {t("nav.heatmap", locale)}
                </h1>
                <p style={{ color: "var(--color-secondary-text)" }}>
                Visual profitability mapping dynamically mapped to your location profile.
                </p>
            </div>
            {farmerProfile && (
                <div className="text-right text-sm">
                    <span className="font-bold">Crop:</span> <span className="capitalize">{farmerProfile.primaryCrop}</span><br />
                    <span className="font-bold">Haul:</span> {farmerProfile.avgQuantityKg}kg
                </div>
            )}
        </div>

        {isLoading ? (
             <div className="h-[500px] w-full rounded-2xl flex items-center justify-center border-dashed border-2 bg-gray-50 border-gray-300">
                <div className="w-8 h-8 rounded-full border-4 border-t-transparent animate-spin" style={{ borderColor: 'var(--color-deep-farm-green) transparent transparent transparent' }} />
             </div>
        ) : (
            <MapComponent mandis={mapData} />
        )}
      </div>
    </div>
  );
}
