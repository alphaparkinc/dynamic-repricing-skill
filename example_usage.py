import sys
import json
from repricer import DynamicRepricerClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== Dynamic Pricing & Repricer Agent Example ===")
    
    # Initialize client in mock mode
    client = DynamicRepricerClient()
    
    current_price = 45.00
    min_floor = 35.00
    max_ceiling = 65.00
    
    inventory = {
        "stock_level": 120,
        "daily_sales_velocity": 8.5
    }

    # Scenario A: Competitor is matching or slightly cheaper (Undercut)
    print("\n--- Scenario A: Active Competitor Undercutting ---")
    competitors_a = [
        {"source": "Competitor_1", "price": 42.50, "in_stock": True},
        {"source": "Competitor_2", "price": 48.00, "in_stock": True}
    ]
    
    repricing_a = client.calculate_new_price(current_price, min_floor, max_ceiling, competitors_a, inventory)
    print(f"Current Price: ${current_price:.2f}")
    print(f"Recommended Price: ${repricing_a['recommended_price']:.2f}")
    print(f"Price Change Delta: ${repricing_a['price_delta']:.2f}")
    print(f"Reason: {repricing_a['repricing_reason']}")
    
    shopify_payload = client.build_shopify_payload("gid://shopify/ProductVariant/7492019842", repricing_a['recommended_price'])
    print("[Shopify API Price Update Payload Draft]:")
    print(json.dumps(shopify_payload, indent=2))

    # Scenario B: All Competitors are out of stock (Stockout Bidding)
    print("\n--- Scenario B: Competitors Out of Stock (Raise Pricing) ---")
    competitors_b = [
        {"source": "Competitor_1", "price": 42.50, "in_stock": False},
        {"source": "Competitor_2", "price": 48.00, "in_stock": False}
    ]
    
    repricing_b = client.calculate_new_price(current_price, min_floor, max_ceiling, competitors_b, inventory)
    print(f"Current Price: ${current_price:.2f}")
    print(f"Recommended Price: ${repricing_b['recommended_price']:.2f}")
    print(f"Price Change Delta: ${repricing_b['price_delta']:.2f}")
    print(f"Reason: {repricing_b['repricing_reason']}")

if __name__ == "__main__":
    main()
