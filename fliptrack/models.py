from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Marketplace(str, Enum):
    VINTED = "vinted"
    EBAY = "ebay"
    DEPOP = "depop"
    LEBONCOIN = "leboncoin"
    VESTIAIRE = "vestiaire"


@dataclass
class SaleInput:
    buy_price: float
    sell_price: float
    shipping_cost: float = 0.0
    packaging_cost: float = 0.0
    marketplace: Marketplace = Marketplace.VINTED
    buyer_pays_shipping: bool = True


@dataclass
class ProfitResult:
    gross_revenue: float
    total_fees: float
    total_costs: float
    net_profit: float
    roi_percent: float
    margin_percent: float
    fee_breakdown: dict[str, float]
