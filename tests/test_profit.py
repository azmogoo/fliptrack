import pytest

from fliptrack.models import Marketplace, SaleInput
from fliptrack.profit import compute_profit, break_even_price
from fliptrack.fees import depop_fee, vestiaire_fee


def test_vinted_zero_fee():
    sale = SaleInput(buy_price=30, sell_price=60, marketplace=Marketplace.VINTED)
    r = compute_profit(sale)
    assert r.total_fees == 0
    assert r.net_profit == 30


def test_depop_fee():
    fees = depop_fee(100)
    assert fees["platform_fee"] == 10.0


def test_break_even():
    sale = SaleInput(buy_price=20, sell_price=40, marketplace=Marketplace.DEPOP)
    be = break_even_price(sale, target_profit=0)
    assert be >= 20
