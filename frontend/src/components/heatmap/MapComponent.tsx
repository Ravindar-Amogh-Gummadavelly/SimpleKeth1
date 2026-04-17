// SimpleKeth — Mandi Heatmap Component
// Real-time leaflet map plotting mandi profitability

"use client";

import { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip, ZoomControl } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { formatCurrency } from "@/lib/utils";

interface MapProps {
  mandis: {
    id: string;
    name: string;
    lat: number;
    lng: number;
    expectedProfit: number;
    rank: number;
  }[];
}

export default function MapComponent({ mandis }: MapProps) {
  // Center roughly on Maharashtra/Central India
  const center: [number, number] = [20.5937, 78.9629];
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return <div className="h-[500px] w-full bg-gray-100 animate-pulse rounded-2xl flex items-center justify-center">Loading Map Engine...</div>;

  const getColor = (rank: number) => {
    if (rank === 1) return "#3FA34D"; // Profit Green
    if (rank === 2) return "#7DAA6A"; // Soft Green
    if (rank === 3) return "#C89B3C"; // Hold Yellow
    return "#B23A3A"; // Loss Red
  };

  return (
    <div className="h-[500px] w-full rounded-2xl overflow-hidden shadow-sm border border-gray-200">
      <MapContainer 
        center={center} 
        zoom={5} 
        scrollWheelZoom={false} 
        style={{ height: "100%", width: "100%", zIndex: 0 }}
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <ZoomControl position="bottomright" />
        
        {mandis.map((mandi) => (
          <CircleMarker
            key={mandi.id}
            center={[mandi.lat, mandi.lng]}
            radius={mandi.rank === 1 ? 16 : 10}
            pathOptions={{ 
                color: getColor(mandi.rank),
                fillColor: getColor(mandi.rank),
                fillOpacity: 0.7,
                weight: 2
            }}
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={1} permanent={mandi.rank === 1}>
              <div className="text-center">
                  <p className="font-bold text-gray-800">{mandi.name}</p>
                  <p className="text-sm font-semibold" style={{ color: getColor(mandi.rank) }}>
                      {formatCurrency(mandi.expectedProfit)} Profit
                  </p>
                  {mandi.rank === 1 && (
                      <p className="text-xs text-white bg-green-600 px-2 py-0.5 rounded-full mt-1 inline-block">Best Option</p>
                  )}
              </div>
            </Tooltip>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
