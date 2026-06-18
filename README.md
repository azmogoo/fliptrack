# fliptrack

CLI profit calculator and inventory tracker for resellers. Estimate fees across Vinted, eBay, Depop, Leboncoin, and Vestiaire Collective before you buy.

## install

```bash
pip install -e .
```

## profit calculator

```bash
fliptrack calc --buy 35 --sell 75 -m vinted
fliptrack calc --buy 20 --sell 45 -m depop --shipping 3.50
fliptrack calc --buy 50 --sell 120 -m vestiaire --target 30
```

Output includes fees, net profit, ROI, and margin. Use `--target` to find the break-even sell price.

## inventory

```bash
fliptrack inventory add "nike tech fleece M" --buy 38 --listed 75
fliptrack inventory list
fliptrack inventory sold ITEM_ID --price 72
fliptrack inventory summary
```

Data is stored in `inventory.json`.

## supported marketplaces

| marketplace | fee model |
|-------------|-----------|
| vinted | no seller commission (standard) |
| ebay | ~13% final value + listing |
| depop | 10% platform fee |
| leboncoin | free (individual) |
| vestiaire | tiered 10–15% commission |

Fee models are approximate — always check current platform pricing.

## license

MIT
