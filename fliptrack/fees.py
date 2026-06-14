from __future__ import annotations

from fliptrack.models import Marketplace


def vinted_fee(sell_price: float, buyer_protection: bool = True) -> dict[str, float]:
    """vinted seller fees — buyer protection is paid by buyer, not seller."""
    # sellers on vinted typically pay no commission on casual sales
    # pro/business accounts may differ — kept at zero for standard flips
    _ = buyer_protection
    return {"platform_fee": 0.0}


def ebay_fee(sell_price: float, category_pct: float = 0.13) -> dict[str, float]:
    final_value = round(sell_price * category_pct, 2)
    fixed = 0.35 if sell_price < 100 else 0.0
    return {"final_value_fee": final_value, "listing_fee": fixed}


def depop_fee(sell_price: float) -> dict[str, float]:
    return {"platform_fee": round(sell_price * 0.10, 2)}


def leboncoin_fee(sell_price: float, has_shipping: bool = True) -> dict[str, float]:
    # particulier — no commission on most categories
    _ = sell_price, has_shipping
    return {"platform_fee": 0.0}


def vestiaire_fee(sell_price: float) -> dict[str, float]:
    if sell_price < 80:
        pct = 0.15
    elif sell_price < 200:
        pct = 0.125
    else:
        pct = 0.10
    return {"commission": round(sell_price * pct, 2)}


def calculate_fees(marketplace: Marketplace, sell_price: float) -> dict[str, float]:
    calculators = {
        Marketplace.VINTED: lambda p: vinted_fee(p),
        Marketplace.EBAY: lambda p: ebay_fee(p),
        Marketplace.DEPOP: lambda p: depop_fee(p),
        Marketplace.LEBONCOIN: lambda p: leboncoin_fee(p),
        Marketplace.VESTIAIRE: lambda p: vestiaire_fee(p),
    }
    calc = calculators.get(marketplace)
    if calc is None:
        return {"platform_fee": 0.0}
    return calc(sell_price)
