# Estimate — Close an account

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. `SessionRevoker` (manage-sessions), `IPhotoStorage` (listings) and the outbox already exist. The port implementations owned by the orders and listings subsystems (`IOpenOrderLookup`, `IMemberListingRemover`, `IMemberAddressEraser`, `IOrderAnonymiser`) are counted here as thin queries over their tables. The legal retention period (`<TO SUPPLY>`) affects only configuration.
[Detailed design](../../detailed-designs/accounts/close-account/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `CloseAccountDialog` with `invalid`, `busy` and `blocked` states | 5 |
| `AccountClosureController` | 1 |
| `CloseAccountCommandHandler` | 5 |
| Port contracts and implementations for open orders and listing removal | 4 |
| `Member.Close` / `Member.Erase` and closure columns migration | 2 |
| `AccountErasureJob` scheduling and batching | 4 |
| `MemberDataEraser` with photo, address, preference and order anonymisation calls | 8 |
| Acceptance tests for `L2-005` criteria 1 to 4 | 7 |
| **Total** | **36** |

## Minimal scope

The minimal scope still satisfies all of `L2-005`, because closure, the open-order refusal, sign-out everywhere and 30-day erasure are each mandatory. It replaces the order list in the `blocked` state with a count and a link to the purchases and sales pages, and runs the erasure job without batching. Removing these items saves 2 hours.

**Minimal scope total: 34 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Order links in the `blocked` state; show a count instead | The member finds the open orders through the purchases and sales pages | 1 |
| Erasure batching | One run processes every due member at once | 1 |
