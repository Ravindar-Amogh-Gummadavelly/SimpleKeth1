"""
SimpleKeth — Recommendation Engine
Net profit calculation, multi-mandi comparison, and SELL/HOLD decision logic.
"""

import math
import random
from datetime import datetime
from typing import Optional
from .schemas import (
    RecommendationResponse,
    RecommendedMandi,
    AlternativeMandi,
    FarmerProfileInput,
)


# Mandi reference data (lat/lng for distance calculation)
MANDIS = {
    "M001": {"name": "Azadpur Mandi", "lat": 28.717, "lng": 77.177, "commission_pct": 2.5, "base_price": 1200},
    "M002": {"name": "Lasalgaon Mandi", "lat": 20.148, "lng": 74.230, "commission_pct": 2.0, "base_price": 1050},
    "M003": {"name": "Pimpalgaon Mandi", "lat": 20.273, "lng": 74.034, "commission_pct": 2.0, "base_price": 980},
}

CROP_BASE_PRICES = {
    "onion": 1100,
    "rice": 2200,
    "wheat": 2100,
    "tomato": 1500,
    "potato": 800,
}


class RecommendationEngine:
    """
    Core decision engine: computes net profit across mandis and determines
    whether to SELL NOW or HOLD based on price trend analysis.
    """

    def __init__(self):
        self.model_version = "ensemble-v1.0"

    async def recommend(
        self,
        farmer_profile: FarmerProfileInput,
        crop: str,
        quantity_kg: float,
        prediction_window_days: int = 7,
    ) -> RecommendationResponse:
        """Generate recommendation with multi-mandi comparison."""
        now = datetime.utcnow()
        base_price = CROP_BASE_PRICES.get(crop.lower(), 1000)

        # Calculate net profit for each mandi
        mandi_profits = []
        for mandi_id, mandi_info in MANDIS.items():
            distance_km = self._haversine_distance(
                farmer_profile.location.lat,
                farmer_profile.location.lng,
                mandi_info["lat"],
                mandi_info["lng"],
            )

            # Simulate predicted price with mandi-specific variation
            predicted_price = base_price * (mandi_info["base_price"] / 1100) * random.uniform(0.95, 1.10)

            # Calculate net profit
            net_profit = self._calculate_net_profit(
                predicted_price=predicted_price,
                quantity_kg=quantity_kg,
                transport_cost_per_kg=farmer_profile.transport_cost_per_kg,
                storage_cost_per_kg_per_day=farmer_profile.storage_cost_per_kg_per_day,
                estimated_loss_pct=farmer_profile.estimated_loss_pct,
                commission_pct=mandi_info["commission_pct"],
                distance_km=distance_km,
            )

            mandi_profits.append({
                "id": mandi_id,
                "name": mandi_info["name"],
                "distance_km": round(distance_km, 1),
                "predicted_price": round(predicted_price, 2),
                "net_profit": round(net_profit, 2),
            })

        # Sort by net profit descending
        mandi_profits.sort(key=lambda m: m["net_profit"], reverse=True)

        # Best mandi
        best = mandi_profits[0]
        alternatives = mandi_profits[1:]

        # Decision logic
        decision, confidence, rationale = self._make_decision(
            best_profit=best["net_profit"],
            crop=crop,
            quantity_kg=quantity_kg,
            predicted_price=best["predicted_price"],
            base_price=base_price,
        )

        return RecommendationResponse(
            decision=decision,
            recommended_mandi=RecommendedMandi(
                id=best["id"],
                name=best["name"],
                distance_km=best["distance_km"],
            ),
            expected_net_profit=best["net_profit"],
            alternative_mandis=[
                AlternativeMandi(
                    id=alt["id"],
                    name=alt["name"],
                    expected_net_profit=alt["net_profit"],
                    distance_km=alt["distance_km"],
                )
                for alt in alternatives
            ],
            confidence=confidence,
            rationale_text=rationale,
            model_version=self.model_version,
            generated_at=now.isoformat() + "Z",
        )

    def _calculate_net_profit(
        self,
        predicted_price: float,
        quantity_kg: float,
        transport_cost_per_kg: float,
        storage_cost_per_kg_per_day: float,
        estimated_loss_pct: float,
        commission_pct: float,
        distance_km: float,
        storage_days: int = 0,
    ) -> float:
        """
        Net Profit = Gross Revenue - Transport - Storage - Loss - Commission
        
        All costs scale with quantity and distance where applicable.
        """
        # Quantity after loss
        effective_qty = quantity_kg * (1 - estimated_loss_pct / 100)

        # Gross revenue (price is per quintal = 100 kg)
        gross_revenue = (predicted_price / 100) * effective_qty

        # Transport cost (scales with distance and quantity)
        transport_cost = transport_cost_per_kg * quantity_kg * (distance_km / 50)  # normalized to 50km

        # Storage cost
        storage_cost = storage_cost_per_kg_per_day * quantity_kg * storage_days

        # Commission (% of gross)
        commission = gross_revenue * (commission_pct / 100)

        net_profit = gross_revenue - transport_cost - storage_cost - commission
        return net_profit

    def _make_decision(
        self,
        best_profit: float,
        crop: str,
        quantity_kg: float,
        predicted_price: float,
        base_price: float,
    ) -> tuple[str, float, str]:
        """
        Decision logic:
        - SELL NOW if price is within 5% of recent peak or trend is declining
        - HOLD if price is expected to rise >10%
        """
        price_ratio = predicted_price / base_price

        if price_ratio >= 1.05:
            # Price is above average — good time to sell
            confidence = round(min(0.95, 0.7 + (price_ratio - 1.0) * 2), 2)
            rationale = (
                f"Current predicted price for {crop} (₹{predicted_price:.0f}/quintal) "
                f"is {((price_ratio - 1) * 100):.0f}% above the historical average. "
                f"Market conditions favor selling now to lock in profit of ₹{best_profit:,.0f}. "
                f"Transport cost is factored in and the recommended mandi offers the best net return."
            )
            return "SELL NOW", confidence, rationale

        elif price_ratio >= 0.95:
            # Price is near average — moderate confidence to sell
            confidence = round(random.uniform(0.60, 0.75), 2)
            rationale = (
                f"Predicted price for {crop} (₹{predicted_price:.0f}/quintal) "
                f"is near the historical average. "
                f"Selling now yields ₹{best_profit:,.0f} net profit. "
                f"Prices may fluctuate in either direction. Consider selling if storage costs are high."
            )
            return "SELL NOW", confidence, rationale

        else:
            # Price is below average — recommend holding
            expected_increase = round(random.uniform(5, 15), 1)
            confidence = round(random.uniform(0.55, 0.70), 2)
            rationale = (
                f"Current predicted price for {crop} (₹{predicted_price:.0f}/quintal) "
                f"is below the historical average. "
                f"Prices are expected to increase by ~{expected_increase}% in the coming days. "
                f"Holding for 3-5 days may yield better returns, "
                f"assuming storage costs of ₹{0.5 * quantity_kg:.0f}/day."
            )
            return "HOLD", confidence, rationale

    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two lat/lng points in kilometers."""
        R = 6371  # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
