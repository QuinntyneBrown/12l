# Estimate — Moderate reports

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in the stack but new to this codebase. It assumes that `report-listing-or-member` has delivered the `Reports` tables, and that `suspend-member` supplies `MemberSuspensionService`. It assumes `audit-log-and-admin-sign-in` supplies `IAuditLog` and the `AdministratorWithSecondFactor` policy. The orders subsystem implements `IOrderModerationPort` and `IOrderProblemQueueSource`, including the cancellation and refund; only the calls are costed here. The number rests on the order-warning wording for a Paid order and the rule for orders past Paid (both `<TO SUPPLY>`) adding no new screens. Hours cover implementation, tests and review fixes. [Detailed design](../../detailed-designs/moderation/moderate-reports/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `AdminShellComponent` with Admin badge and Queue / Audit log tabs, lazy `/admin` routes | 4 |
| `ModerationQueuePageComponent` with default, loading, empty, error and forbidden states | 6 |
| `ReportDetailPageComponent` with default, hidden, resolved, loading and error states | 6 |
| `ResolveReportDialogComponent` with default, invalid, busy, order-warning and failed states | 7 |
| `ModerationApiService` queue, detail and resolve calls with 409 mapping | 2 |
| `ModerationQueueController` and `GetModerationQueueQueryHandler` merging reports with order problems, keyset paging | 6 |
| `AdminReportsController` and `GetReportDetailQueryHandler` | 4 |
| `ResolveReportCommand`, validator and handler for dismiss, remove listing and suspend decisions | 8 |
| Order-warning flow with `IOrderModerationPort` calls and confirmation flag | 4 |
| `Report.Resolve`, `Listing.RemoveByAdministrator`, `Listing.ReturnToCatalog` and migration for resolution and removal columns | 4 |
| `ListingRemovedEmail` outbox message | 1 |
| Backend acceptance tests for `L2-045` criteria 1 to 4, including concurrent resolution | 7 |
| Playwright acceptance tests for queue, detail and resolve dialog | 5 |
| **Total** | **64** |

## Minimal scope

The minimal version ships the queue of open reports (oldest first), the report detail page and the resolve dialog with dismiss and remove listing. It keeps the order warning and confirmation, the reason, the seller email and the audit entry. It leaves out order problems in the queue (administrators reach them from the orders area), the suspend decision inside the dialog (administrators suspend from the member admin page), keyset paging (the queue returns all open items), and the Playwright tests beyond the remove path. It satisfies `L2-045` criteria 1 to 4 for reports and defers the "order problems" part of the queue in `L2-045`. Total: 46 hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Order problems in the queue (`IOrderProblemQueueSource`) | Administrators see order problems in a separate place, not in one oldest-first queue | 3 |
| Suspend decision in `ResolveReportDialogComponent` | Suspension from a report needs a second step on the member admin page | 3 |
| Keyset paging on the queue | A queue of any length loads in one response | 2 |
| Concurrent-resolution test and `409 report.already_resolved` reload | Two administrators deciding at once see a generic error | 2 |
| Playwright tests reduced to the remove path | Less end-to-end coverage of dismiss, empty and error states | 3 |
