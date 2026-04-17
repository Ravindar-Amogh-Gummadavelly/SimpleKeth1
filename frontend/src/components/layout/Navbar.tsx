// SimpleKeth — Navbar Component
// Mobile-first responsive navigation with language switcher

"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  BarChart3,
  TrendingUp,
  Calculator,
  Bell,
  User,
  Menu,
  X,
  Globe,
  Leaf,
} from "lucide-react";
import { useUIStore } from "@/lib/store";
import { t, locales, type Locale } from "@/i18n/config";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", icon: LayoutDashboard, labelKey: "nav.dashboard" },
  { href: "/market-comparison", icon: BarChart3, labelKey: "nav.market" },
  { href: "/prediction-trends", icon: TrendingUp, labelKey: "nav.trends" },
  { href: "/simulator", icon: Calculator, labelKey: "nav.simulator" },
  { href: "/alerts", icon: Bell, labelKey: "nav.alerts" },
  { href: "/profile", icon: User, labelKey: "nav.profile" },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const { locale, setLocale, isOffline } = useUIStore();

  return (
    <>
      {/* Offline Banner */}
      {isOffline && (
        <div className="offline-banner">
          {t("offline.banner", locale)}
        </div>
      )}

      <nav
        className="sticky top-0 z-50 border-b"
        style={{
          backgroundColor: "var(--color-cream-white)",
          borderColor: "var(--color-border)",
        }}
      >
        <div className="container-main">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 no-underline">
              <div
                className="w-9 h-9 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: "var(--color-deep-farm-green)" }}
              >
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <span
                className="text-xl font-bold"
                style={{
                  fontFamily: "var(--font-heading)",
                  color: "var(--color-deep-farm-green)",
                }}
              >
                SimpleKeth
              </span>
            </Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium no-underline transition-colors",
                      isActive
                        ? "text-white"
                        : "hover:bg-[var(--color-light-green-tint)]"
                    )}
                    style={{
                      backgroundColor: isActive
                        ? "var(--color-deep-farm-green)"
                        : undefined,
                      color: isActive
                        ? "white"
                        : "var(--color-secondary-text)",
                    }}
                  >
                    <item.icon className="w-4 h-4" />
                    {t(item.labelKey, locale)}
                  </Link>
                );
              })}
            </div>

            {/* Language Switcher + Mobile Toggle */}
            <div className="flex items-center gap-2">
              {/* Language Dropdown */}
              <div className="relative">
                <button
                  onClick={() => setLangOpen(!langOpen)}
                  className="flex items-center gap-1 px-2 py-1.5 rounded-lg text-sm transition-colors hover:bg-[var(--color-light-green-tint)]"
                  style={{ color: "var(--color-secondary-text)" }}
                  aria-label="Change language"
                >
                  <Globe className="w-4 h-4" />
                  <span className="hidden sm:inline">{locales[locale]}</span>
                </button>
                <AnimatePresence>
                  {langOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: -8 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -8 }}
                      className="absolute right-0 mt-1 py-1 rounded-lg shadow-lg border z-50"
                      style={{
                        backgroundColor: "white",
                        borderColor: "var(--color-border)",
                        minWidth: "120px",
                      }}
                    >
                      {(Object.entries(locales) as [Locale, string][]).map(
                        ([key, label]) => (
                          <button
                            key={key}
                            onClick={() => {
                              setLocale(key);
                              setLangOpen(false);
                            }}
                            className={cn(
                              "w-full text-left px-4 py-2 text-sm transition-colors",
                              locale === key
                                ? "font-bold"
                                : "hover:bg-[var(--color-light-green-tint)]"
                            )}
                            style={{
                              color:
                                locale === key
                                  ? "var(--color-deep-farm-green)"
                                  : "var(--color-primary-text)",
                              backgroundColor:
                                locale === key
                                  ? "var(--color-light-green-tint)"
                                  : undefined,
                            }}
                          >
                            {label}
                          </button>
                        )
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Mobile Menu Toggle */}
              <button
                onClick={() => setMobileOpen(!mobileOpen)}
                className="md:hidden p-2 rounded-lg hover:bg-[var(--color-light-green-tint)]"
                aria-label="Toggle menu"
              >
                {mobileOpen ? (
                  <X className="w-5 h-5" />
                ) : (
                  <Menu className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Nav */}
        <AnimatePresence>
          {mobileOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="md:hidden overflow-hidden border-t"
              style={{ borderColor: "var(--color-border)" }}
            >
              <div className="container-main py-3 flex flex-col gap-1">
                {navItems.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setMobileOpen(false)}
                      className={cn(
                        "flex items-center gap-3 px-4 py-3 rounded-lg text-base font-medium no-underline transition-colors"
                      )}
                      style={{
                        backgroundColor: isActive
                          ? "var(--color-light-green-tint)"
                          : undefined,
                        color: isActive
                          ? "var(--color-deep-farm-green)"
                          : "var(--color-primary-text)",
                      }}
                    >
                      <item.icon className="w-5 h-5" />
                      {t(item.labelKey, locale)}
                    </Link>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </>
  );
}
