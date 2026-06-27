# Dynamic Pricing & Competitive Repricer Skill

This repository contains the **Dynamic Pricing & Competitive Repricer Skill** — a developer Python SDK client (`repricer.py`), an agent skill configuration interface (`skill.json`), and executable validation examples designed to monitor competitor product prices, evaluate inventory velocity, and output price adjustments to Shopify/Amazon APIs.

---

## 🚀 Capabilities

* **Active Competitor Monitoring:** Detects in-stock competitors and triggers undercutting logic ($0.10 decrement) down to safety price floors.
* **Stockout Bidding Optimization:** Identifies when competitors are out of stock and automatically increments pricing (+15%) to capture premium margins.
* **Inventory Run-Rate Pricing:** Calculates when current sales velocity threatens early stockouts and lifts pricing (+10%) to optimize returns.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configuration:
   Set your API environment variables if executing requests against the live production server (otherwise, client executes in mock mode):
   * **PowerShell**:
     ```powershell
     $env:REPRICER_API_KEY="your_api_key"
     ```
   * **bash**:
     ```bash
     export REPRICER_API_KEY="your_api_key"
     ```

---

## 💻 SDK Usage Reference

```python
from repricer import DynamicRepricerClient

# Initialize Client (mock mode by default)
client = DynamicRepricerClient()

# Recommend price based on active competitor and inventory parameters
repricing = client.calculate_new_price(
    current_price=45.00,
    min_floor=35.00,
    max_ceiling=65.00,
    competitor_prices=[{"price": 42.50, "in_stock": True}],
    inventory={"stock_level": 120, "daily_sales_velocity": 8.5}
)
print(f"New Price Recommendation: ${repricing['recommended_price']:.2f}")
print(f"Reasoning: {repricing['repricing_reason']}")

# Build Shopify update body payload draft
shopify_payload = client.build_shopify_payload("gid://shopify/ProductVariant/7492", repricing['recommended_price'])
```

---

## 📜 License
This project is licensed under the MIT License.
