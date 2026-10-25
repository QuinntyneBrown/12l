# Estimate — Suspend and reinstate a member

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in the stack but new to this codebase. It assumes that the accounts subsystem provides `Member`, `GET /api/me` and `AuthStateService`, and that `IAuditLog`, the outbox and the Redis connection exist. It assumes `AdminShellComponent` exists from `moderate-reports`. Applying the `NotSuspended` policy to each listings, orders and reviews endpoint is one attribute per endpoint and is costed here as a single item. The catalog visibility query is costed in the catalog subsystem. The `<TO SUPPLY>` items (suspending administrators, reinstatement email) are assumed to add no work. Hours cover implementation, tests and review fixes. [Detailed design](../../detailed-designs/moderation/suspend-member/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `MemberAdminPageComponent` with default, suspended, loading and error states and history list | 6 |
| `SuspendMemberDialogComponent` in suspend and reinstate modes with invalid and busy states | 4 |
| Account banner danger variant and `memberStatus` signal refresh on `account.suspended` | 3 |
| `AdminMembersController` `GET` member summary query | 4 |
| Suspension and reinstatement endpoints, commands, validators and handlers | 4 |
| `MemberSuspensionService` with audit entry and `MemberSuspendedEmail` outbox message | 3 |
| `Member.Suspend` / `Reinstate`, `MemberSuspension` entity, migration and filtered unique index | 4 |
| `NotSuspendedRequirement`, `NotSuspendedAuthorizationHandler` and application to restricted endpoints | 4 |
| `RedisMemberStatusReader` with database fallback and eviction after commit | 3 |
| Backend acceptance tests for `L2-046` criteria 1 to 4 | 6 |
| Playwright acceptance tests for suspend, reinstate and the suspended member's banner and sell page | 4 |
| **Total** | **45** |

## Minimal scope

The minimal version ships the member admin page, the suspend and reinstate dialog, the `Member` transitions with audit entries and the suspension email, and the `NotSuspended` policy on restricted endpoints. The policy reads `Members.Status` directly from the database on each restricted request, with no Redis cache. It leaves out the history list on the member admin page, the account banner signal refresh (the banner appears after the next token refresh), and Playwright tests beyond the suspend path. It satisfies `L2-046` criteria 1 to 4 and defers no requirement. Total: 33 hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `RedisMemberStatusReader`; read status from the database | One extra database read per restricted request | 2 |
| History list on `MemberAdminPageComponent` | Administrators do not see open cases on the member page | 2 |
| Immediate banner refresh on `account.suspended` | A newly suspended member sees the banner up to 15 minutes later | 2 |
| `MemberSuspensions` history table; keep current suspension columns on `Members` | Past suspension periods are visible only in the audit log | 2 |
| Playwright tests reduced to the suspend path | Less end-to-end coverage of reinstatement and member-facing states | 2 |
