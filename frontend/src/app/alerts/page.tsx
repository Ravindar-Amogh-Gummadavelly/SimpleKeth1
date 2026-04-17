// SimpleKeth — Alerts Page
// Manage notification subscriptions + alert history

"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Bell, MessageSquare, Phone, Smartphone, TrendingUp, AlertTriangle } from "lucide-react";
import { useUIStore } from "@/lib/store";
import { t } from "@/i18n/config";
import { formatCurrency } from "@/lib/utils";

interface Alert {
  id: string;
  type: "opportunity" | "urgency" | "caution";
  message: string;
  crop: string;
  mandi: string;
  price: number;
  timestamp: string;
}

const sampleAlerts: Alert[] = [
  {
    id: "1",
    type: "opportunity",
    message: "Onion price spike detected at Azadpur Mandi!",
    crop: "Onion",
    mandi: "Azadpur Mandi",
    price: 1350,
    timestamp: "2026-04-17T10:30:00Z",
  },
  {
    id: "2",
    type: "caution",
    message: "Potato prices expected to drop in 3 days.",
    crop: "Potato",
    mandi: "Lasalgaon Mandi",
    price: 780,
    timestamp: "2026-04-16T14:00:00Z",
  },
  {
    id: "3",
    type: "urgency",
    message: "High supply arriving at Pimpalgaon — sell before prices drop.",
    crop: "Tomato",
    mandi: "Pimpalgaon Mandi",
    price: 1420,
    timestamp: "2026-04-15T09:00:00Z",
  },
];

const alertColors = {
  opportunity: "var(--color-profit-green)",
  urgency: "var(--color-loss-red)",
  caution: "var(--color-hold-warning)",
};

const alertIcons = {
  opportunity: TrendingUp,
  urgency: AlertTriangle,
  caution: Bell,
};

export default function AlertsPage() {
  const locale = useUIStore((s) => s.locale);
  const [channels, setChannels] = useState({
    sms: true,
    push: true,
    voice: false,
  });

  const [simulation, setSimulation] = useState<{ type: string; active: boolean } | null>(null);

  const handleToggle = async (channelKey: "sms" | "push" | "voice", checked: boolean) => {
    setChannels((prev) => ({ ...prev, [channelKey]: checked }));
    
    if (checked) {
        try {
            const { sendNotification } = await import("@/lib/api");
            const farmerId = useUIStore.getState().locale || "local-user"; // Fallback ID

            await sendNotification({
                farmerId,
                channel: channelKey,
                message: `Successfully subscribed to ${channelKey.toUpperCase()} alerts from SimpleKeth!`,
            });
        } catch (e) {
            console.error(`Failed to register ${channelKey} on backend:`, e);
        }
    }
  };

  const simulateOfflineAlert = (type: "sms" | "voice") => {
      setSimulation({ type, active: true });
      setTimeout(() => setSimulation(null), 4000);
  };

  return (
    <div className="min-h-screen relative" style={{ backgroundColor: "var(--color-cream-white)" }}>
      {/* Simulation Overlay */}
      {simulation?.active && (
         <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm px-4">
             <motion.div 
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="bg-white rounded-2xl p-6 shadow-xl max-w-sm w-full text-center"
             >
                 {simulation.type === "sms" ? (
                     <>
                        <MessageSquare className="w-12 h-12 mx-auto mb-4" style={{ color: "var(--color-profit-green)" }} />
                        <h3 className="text-lg font-bold mb-2">Offline SMS Received</h3>
                        <p className="text-gray-600 bg-gray-100 p-3 rounded-lg text-sm text-left">
                           "SimpleKeth Alert: SELL NOW! Onion prices at Azadpur hit ₹1400/q. Expecting drop by tomorrow."
                        </p>
                     </>
                 ) : (
                     <>
                        <Phone className="w-12 h-12 mx-auto mb-4 animate-bounce" style={{ color: "var(--color-deep-farm-green)" }} />
                        <h3 className="text-lg font-bold mb-2">Incoming Voice Call...</h3>
                        <p className="text-gray-600 text-sm italic">
                           "Hello! This is your SimpleKeth smart assistant. A profitable selling window is open today..."
                        </p>
                     </>
                 )}
             </motion.div>
         </div>
      )}

      <div className="container-main section">
        <h1 className="mb-2" style={{ color: "var(--color-deep-farm-green)", fontSize: "34px" }}>
          <Bell className="w-8 h-8 inline mr-2" />
          {t("alerts.title", locale)}
        </h1>
        <p className="mb-8" style={{ color: "var(--color-secondary-text)" }}>
          {t("alerts.subtitle", locale)}
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Channel Settings & Simulators */}
          <div className="flex flex-col gap-6">
              <div className="card" style={{ height: "fit-content" }}>
                <h3 className="text-lg mb-4" style={{ color: "var(--color-deep-farm-green)" }}>
                  Notification Channels
                </h3>
                {[
                  { key: "sms" as const, icon: MessageSquare, label: t("alerts.enableSms", locale) },
                  { key: "push" as const, icon: Smartphone, label: t("alerts.enablePush", locale) },
                  { key: "voice" as const, icon: Phone, label: t("alerts.enableVoice", locale) },
                ].map((ch) => (
                  <label
                    key={ch.key}
                    className="flex items-center justify-between py-3 cursor-pointer border-b last:border-0"
                    style={{ borderColor: "var(--color-border)" }}
                  >
                    <div className="flex items-center gap-3">
                      <ch.icon className="w-5 h-5" style={{ color: "var(--color-fresh-leaf-green)" }} />
                      <span className="font-medium">{ch.label}</span>
                    </div>
                    <input
                      type="checkbox"
                      checked={channels[ch.key]}
                      onChange={(e) => handleToggle(ch.key, e.target.checked)}
                      className="w-5 h-5 accent-[#4E7C4F] cursor-pointer"
                    />
                  </label>
                ))}
              </div>

              {/* Simulators */}
              <div className="card bg-gray-50 border-dashed border-2">
                 <h3 className="text-sm font-bold mb-3 text-gray-500 uppercase tracking-wider">Test Offline Fallbacks</h3>
                 <div className="flex flex-col gap-3">
                    <button onClick={() => simulateOfflineAlert('sms')} className="btn-secondary w-full flex items-center justify-center gap-2" style={{ borderColor: 'var(--color-deep-farm-green)', color: 'var(--color-deep-farm-green)' }}>
                        <MessageSquare className="w-4 h-4" /> Simulate SMS
                    </button>
                    <button onClick={() => simulateOfflineAlert('voice')} className="btn-secondary w-full flex items-center justify-center gap-2" style={{ borderColor: 'var(--color-deep-farm-green)', color: 'var(--color-deep-farm-green)' }}>
                        <Phone className="w-4 h-4" /> Simulate Voice Call
                    </button>
                 </div>
              </div>
          </div>

          {/* Alert Feed */}
          <div className="lg:col-span-2 flex flex-col gap-3">
            {sampleAlerts.map((alert, i) => {
              const Icon = alertIcons[alert.type];
              return (
                <motion.div
                  key={alert.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="card flex items-start gap-4"
                  style={{ borderLeft: `4px solid ${alertColors[alert.type]}` }}
                >
                  <div
                    className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
                    style={{ backgroundColor: `${alertColors[alert.type]}20`, color: alertColors[alert.type] }}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold mb-1" style={{ color: "var(--color-primary-text)" }}>
                      {alert.message}
                    </p>
                    <div className="flex items-center gap-4 text-sm" style={{ color: "var(--color-secondary-text)" }}>
                      <span>{alert.crop}</span>
                      <span>•</span>
                      <span>{alert.mandi}</span>
                      <span>•</span>
                      <span className="font-medium" style={{ color: alertColors[alert.type] }}>
                        {formatCurrency(alert.price)}/q
                      </span>
                    </div>
                    <p className="text-xs mt-1" style={{ color: "var(--color-secondary-text)" }}>
                      {new Date(alert.timestamp).toLocaleString("en-IN")}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
