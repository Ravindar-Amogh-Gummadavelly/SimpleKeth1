// SimpleKeth — i18n Configuration
// Supports: English (en), Hindi (hi), Telugu (te)

import en from "./en.json";
import hi from "./hi.json";
import te from "./te.json";

export type Locale = "en" | "hi" | "te";

export const locales: Record<Locale, string> = {
  en: "English",
  hi: "हिन्दी",
  te: "తెలుగు",
};

const translations: Record<Locale, typeof en> = { en, hi, te };

export type TranslationKeys = typeof en;

/**
 * Get a nested translation value by dot-notation key.
 * e.g., t("hero.headline", "en") → "Know Exactly When & Where to Sell Your Crops"
 */
export function t(key: string, locale: Locale = "en"): string {
  const keys = key.split(".");
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let value: any = translations[locale] || translations.en;
  
  for (const k of keys) {
    value = value?.[k];
    if (value === undefined) {
      // Fallback to English
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let fallback: any = translations.en;
      for (const fk of keys) {
        fallback = fallback?.[fk];
      }
      return fallback ?? key;
    }
  }
  
  return value as string;
}

export function getTranslations(locale: Locale = "en"): TranslationKeys {
  return translations[locale] || translations.en;
}

export default translations;
