# Estimates: orders

| Design | Effort | Complete |
|---|---|---|
| cancel-order | 3 days | 0% |
| checkout-and-pay | 7 days | 90% |
| complete-order | 3 days | 0% |
| order-history | 3 days | 0% |
| resolve-order-problems | 5 days | 0% |
| seller-payouts | 5 days | 0% |
| ship-order | 4 days | 0% |

Excludes deferred work (see AGENTS.md).

checkout-and-pay is at 90%: the payment provider adapter, its hosted-fields SDK and credentials
are deferred until a provider is chosen ([ADR orders/0001](../adr/orders/0001-payment-provider-behind-a-port-until-chosen.md)).
