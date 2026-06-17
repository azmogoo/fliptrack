from __future__ import annotations

import argparse
import sys

from fliptrack.inventory import InventoryItem, InventoryStore
from fliptrack.models import Marketplace, SaleInput
from fliptrack.profit import break_even_price, compute_profit


def cmd_calc(args: argparse.Namespace) -> int:
    try:
        marketplace = Marketplace(args.marketplace)
    except ValueError:
        print(f"unknown marketplace: {args.marketplace}", file=sys.stderr)
        return 1
    sale = SaleInput(
        buy_price=args.buy,
        sell_price=args.sell,
        shipping_cost=args.shipping,
        packaging_cost=args.packaging,
        marketplace=marketplace,
        buyer_pays_shipping=not args.seller_pays_shipping,
    )
    result = compute_profit(sale)
    print(f"marketplace: {marketplace.value}")
    print(f"sell price:   {result.gross_revenue:.2f}")
    print(f"fees:         {result.total_fees:.2f}  {result.fee_breakdown}")
    print(f"total costs:  {result.total_costs:.2f}")
    print(f"net profit:   {result.net_profit:.2f}")
    print(f"roi:          {result.roi_percent:.1f}%")
    print(f"margin:       {result.margin_percent:.1f}%")
    if args.target is not None:
        be = break_even_price(sale, target_profit=args.target)
        print(f"break-even (target {args.target:.2f}): {be:.2f}")
    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    store = InventoryStore(args.file)
    if args.action == "add":
        item = InventoryItem.create(title=args.title, buy_price=args.buy, marketplace=args.marketplace)
        if args.listed:
            item.listed_price = args.listed
            item.status = "listed"
        store.add(item)
        print(f"added {item.id}: {item.title}")
        return 0
    if args.action == "list":
        items = store.list(status=args.status)
        for item in items:
            print(f"{item.id}  [{item.status}]  {item.buy_price:>7.2f}  {item.title}")
        return 0
    if args.action == "sold":
        if not store.mark_sold(args.id, args.price):
            print(f"item not found: {args.id}", file=sys.stderr)
            return 1
        print(f"marked {args.id} sold at {args.price:.2f}")
        return 0
    if args.action == "summary":
        s = store.summary()
        for k, v in s.items():
            print(f"{k}: {v}")
        return 0
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fliptrack", description="resell profit calculator")
    sub = parser.add_subparsers(dest="command", required=True)

    calc = sub.add_parser("calc", help="compute profit for a flip")
    calc.add_argument("--buy", type=float, required=True)
    calc.add_argument("--sell", type=float, required=True)
    calc.add_argument("--shipping", type=float, default=0)
    calc.add_argument("--packaging", type=float, default=0)
    calc.add_argument("-m", "--marketplace", default="vinted", choices=[m.value for m in Marketplace])
    calc.add_argument("--seller-pays-shipping", action="store_true")
    calc.add_argument("--target", type=float, default=None, help="target profit for break-even")
    calc.set_defaults(func=cmd_calc)

    inv = sub.add_parser("inventory", help="track stock and sales")
    inv.add_argument("-f", "--file", default="inventory.json")
    inv_sub = inv.add_subparsers(dest="action", required=True)

    add = inv_sub.add_parser("add")
    add.add_argument("title")
    add.add_argument("--buy", type=float, required=True)
    add.add_argument("--listed", type=float, default=None)
    add.add_argument("-m", "--marketplace", default="vinted")

    lst = inv_sub.add_parser("list")
    lst.add_argument("--status", default=None)

    sold = inv_sub.add_parser("sold")
    sold.add_argument("id")
    sold.add_argument("--price", type=float, required=True)

    inv_sub.add_parser("summary")
    inv.set_defaults(func=cmd_inventory)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
