# Estimates: orders

| Design | Effort | Complete |
|---|---|---|
| cancel-order | 3 days | 0% |
| checkout-and-pay | 7 days | 90% |
| complete-order | 3 days | 90% |
| order-history | 3 days | 0% |
| resolve-order-problems | 5 days | 0% |
| seller-payouts | 5 days | 90% |
| ship-order | 4 days | 95% |

Excludes deferred work (see AGENTS.md).

checkout-and-pay is at 90%: the payment provider adapter, its hosted-fields SDK and credentials
are deferred until a provider is chosen ([ADR orders/0001](../adr/orders/0001-payment-provider-behind-a-port-until-chosen.md)).

ship-order is at 95%: the tracking, delivery, cancellation and reminder emails and the reminder
job came with send-email-notifications; the carrier tracking service adapter and the US holiday
list wait until they are chosen and supplied ([ADR orders/0003](../adr/orders/0003-ship-order-status-token-weekday-deadline-and-carrier-port.md)).

complete-order is at 90%: the open-problem guard of L2-034 criterion 3 and "Report a problem" wait
for resolve-order-problems, which introduces problems ([ADR orders/0004](../adr/orders/0004-complete-order-in-process-event-and-fixed-3-day-window.md)).

seller-payouts is at 90%: the payout provider adapter and its credentials wait until a provider is
chosen, and re-sending a failed payout and the open-problem hold are deferred
([ADR orders/0005](../adr/orders/0005-seller-payouts-payout-port-fee-snapshot-and-shell-banner.md)).
