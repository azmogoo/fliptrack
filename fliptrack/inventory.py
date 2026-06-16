from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class InventoryItem:
    id: str
    title: str
    buy_price: float
    listed_price: float | None = None
    sold_price: float | None = None
    marketplace: str = "vinted"
    status: str = "stock"  # stock | listed | sold
    notes: str = ""
    added_at: str = ""

    @classmethod
    def create(cls, title: str, buy_price: float, **kwargs: Any) -> InventoryItem:
        ts = datetime.now(timezone.utc).isoformat()
        item_id = ts.replace(":", "").replace("-", "")[:14]
        return cls(id=item_id, title=title, buy_price=buy_price, added_at=ts, **kwargs)


class InventoryStore:
    def __init__(self, path: str | Path = "inventory.json") -> None:
        self.path = Path(path)
        self._items: list[InventoryItem] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self._items = []
            return
        raw = json.loads(self.path.read_text())
        self._items = [InventoryItem(**row) for row in raw.get("items", [])]

    def save(self) -> None:
        payload = {"items": [asdict(i) for i in self._items]}
        self.path.write_text(json.dumps(payload, indent=2))

    def add(self, item: InventoryItem) -> None:
        self._items.append(item)
        self.save()

    def list(self, status: str | None = None) -> list[InventoryItem]:
        if status is None:
            return list(self._items)
        return [i for i in self._items if i.status == status]

    def mark_sold(self, item_id: str, sold_price: float) -> bool:
        for item in self._items:
            if item.id == item_id:
                item.status = "sold"
                item.sold_price = sold_price
                self.save()
                return True
        return False

    def summary(self) -> dict[str, Any]:
        stock = [i for i in self._items if i.status != "sold"]
        sold = [i for i in self._items if i.status == "sold"]
        invested = sum(i.buy_price for i in stock)
        revenue = sum(i.sold_price or 0 for i in sold)
        cost_sold = sum(i.buy_price for i in sold)
        return {
            "in_stock": len(stock),
            "sold": len(sold),
            "invested": round(invested, 2),
            "revenue": round(revenue, 2),
            "profit_sold": round(revenue - cost_sold, 2),
        }
