# Estimates: orders

| Design | Effort | Complete |
|---|---|---|
| cancel-order | 3 days | 0% |
| checkout-and-pay | 7 days | 90% |
| complete-order | 3 days | 90% |
| order-history | 3 days | 0% |
| resolve-order-problems | 5 days | 0% |
| seller-payouts | 5 days | 0% |
| ship-order | 4 days | 85% |

Excludes deferred work (see AGENTS.md).

checkout-and-pay is at 90%: the payment provider adapter, its hosted-fields SDK and credentials
are deferred until a provider is chosen ([ADR orders/0001](../adr/orders/0001-payment-provider-behind-a-port-until-chosen.md)).

ship-order is at 85%: the tracking, cancellation and reminder emails and the reminder job wait for
send-email-notifications, and the carrier tracking service adapter and the US holiday list wait
until they are chosen and supplied ([ADR orders/0003](../adr/orders/0003-ship-order-status-token-weekday-deadline-and-carrier-port.md)).

complete-order is at 90%: the open-problem guard of L2-034 criterion 3 and "Report a problem" wait
for resolve-order-problems, which introduces problems, and the payout handler of `OrderCompleted`
belongs to seller-payouts ([ADR orders/0004](../adr/orders/0004-complete-order-in-process-event-and-fixed-3-day-window.md)).
