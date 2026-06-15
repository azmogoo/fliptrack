from __future__ import annotations

from fliptrack.fees import calculate_fees
from fliptrack.models import ProfitResult, SaleInput


def compute_profit(sale: SaleInput) -> ProfitResult:
    fee_breakdown = calculate_fees(sale.marketplace, sale.sell_price)
    total_fees = sum(fee_breakdown.values())

    shipping = 0.0 if sale.buyer_pays_shipping else sale.shipping_cost
    total_costs = sale.buy_price + sale.packaging_cost + shipping + total_fees
    net = sale.sell_price - total_costs

    invested = sale.buy_price + sale.packaging_cost + (0 if sale.buyer_pays_shipping else sale.shipping_cost)
    roi = (net / invested * 100) if invested > 0 else 0.0
    margin = (net / sale.sell_price * 100) if sale.sell_price > 0 else 0.0

    return ProfitResult(
        gross_revenue=sale.sell_price,
        total_fees=round(total_fees, 2),
        total_costs=round(total_costs, 2),
        net_profit=round(net, 2),
        roi_percent=round(roi, 1),
        margin_percent=round(margin, 1),
        fee_breakdown=fee_breakdown,
    )


def break_even_price(sale: SaleInput, target_profit: float = 0.0) -> float:
    """estimate minimum sell price for target net profit."""
    low, high = sale.buy_price, sale.buy_price * 5
    for _ in range(40):
        mid = (low + high) / 2
        trial = SaleInput(
            buy_price=sale.buy_price,
            sell_price=mid,
            shipping_cost=sale.shipping_cost,
            packaging_cost=sale.packaging_cost,
            marketplace=sale.marketplace,
            buyer_pays_shipping=sale.buyer_pays_shipping,
        )
        if compute_profit(trial).net_profit >= target_profit:
            high = mid
        else:
            low = mid
    return round(high, 2)
