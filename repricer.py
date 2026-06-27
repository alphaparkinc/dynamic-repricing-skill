import os
import requests
from typing import List, Dict, Any, Optional

class RepricerError(Exception):
    """Base exception class for Dynamic Repricer Client."""
    pass

class DynamicRepricerClient:
    """
    Client for driving e-commerce dynamic repricing calculations based on inventory velocity and competitive data.
    Supports a mock mode for local testing.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.dynamic-repricer.ai/v1"):
        self.api_key = api_key or os.environ.get("REPRICER_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.mock_mode = self.api_key is None or self.api_key == "mock"
        
        if self.mock_mode:
            print("[DynamicRepricerClient] API Key not set. Running in MOCK Mode.")

    def calculate_new_price(
        self,
        current_price: float,
        min_floor: float,
        max_ceiling: float,
        competitor_prices: List[Dict[str, Any]],
        inventory: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates the recommended price adjustment based on competitive and velocity heuristics.
        """
        stock = inventory.get("stock_level", 0)
        velocity = inventory.get("daily_sales_velocity", 0.0)
        
        # Heuristic rules
        # 1. Filter out of stock competitors
        active_comps = [c for c in competitor_prices if c.get("in_stock", True)]
        
        if not active_comps:
            # Competitors out of stock -> Raise price due to high exclusivity
            rec_price = min(max_ceiling, round(current_price * 1.15, 2))
            reason = "All competitors are out of stock. Raising price by 15% to capture additional margin."
        else:
            lowest_comp = min(float(c["price"]) for c in active_comps)
            
            # If sales velocity is very high and stock is low, raise price to slow down velocity and capture margin
            if velocity > 20 and stock < 50:
                rec_price = min(max_ceiling, round(current_price * 1.10, 2))
                reason = "Inventory is low (<50 units) and sales velocity is high. Raising price by 10% to prevent early stockout."
            elif lowest_comp < current_price:
                # Undercut competitor by $0.10, down to floor
                undercut = round(lowest_comp - 0.10, 2)
                rec_price = max(min_floor, undercut)
                
                if rec_price == min_floor:
                    reason = f"Competitor pricing is below target. Setting price to floor limit of ${min_floor:.2f} to protect margins."
                else:
                    reason = f"Undercutting lowest competitor price of ${lowest_comp:.2f} by $0.10."
            else:
                # Match or keep current price
                rec_price = current_price
                reason = "Current price remains competitive against active listings."
                
        return {
            "recommended_price": rec_price,
            "repricing_reason": reason,
            "price_delta": round(rec_price - current_price, 2)
        }

    def build_shopify_payload(self, variant_id: str, new_price: float) -> Dict[str, Any]:
        """
        Builds a standard Shopify Admin REST API PUT payload draft to update variant pricing.
        """
        return {
            "variant": {
                "id": int(variant_id.replace("gid://shopify/ProductVariant/", "") if isinstance(variant_id, str) else variant_id),
                "price": f"{new_price:.2f}"
            }
        }
