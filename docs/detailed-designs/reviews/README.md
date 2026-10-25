# Reviews subsystem

The reviews subsystem lets the buyer and the seller of a Completed order rate and review each other. It publishes those reviews under a blind-review rule and turns them into a public reputation shown on each member's profile (`L1-009`, `L1-010`). It reads order state from `orders`, member data from `accounts` and listings from `listings`. It sends the "review received" email through `notifications`.

| Feature | Design | L2 requirements |
|---------|--------|-----------------|
| Leave a review | [leave-review](leave-review/README.md) | `L2-038`, `L2-039` |
| View a member profile | [view-member-profile](view-member-profile/README.md) | `L2-040`, `L2-041`, `L2-054` |
