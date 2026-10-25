# Export personal data — estimate

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer
who knows MediatR, EF Core and hosted services but does not know this codebase. The
hours cover implementation, tests and review fixes for the
[Detailed design](../../detailed-designs/privacy/export-personal-data/README.md). They
assume the outbox dispatcher, the email adapter, the object storage adapter, `authGuard`
and the Settings page already exist in their own features. They also assume the source
tables for listings, orders, reviews and notification settings are in place. The email
copy and the download page copy are `<TO SUPPLY>`; the hours assume short copy.

## Full design

| Work item | Hours |
|-----------|------:|
| `DataExportDialogComponent` with default, busy, success and error states | 4 |
| "Your data" row wiring on the Settings page | 1 |
| `DataExportDownloadPageComponent` with loading, ready, expired, not-found and error states | 5 |
| `PrivacyApiService` and `ExportRequestView` | 2 |
| `PrivacyExportsController` with three endpoints, policy, problem codes and file streaming | 5 |
| `DataExportRequest` entity and `DataExportStatus` state machine with unit tests | 4 |
| `RequestDataExportCommandHandler` with open-request reuse and outbox message | 3 |
| `GetDataExportQueryHandler` and `OpenDataExportFileQueryHandler` | 4 |
| `DataExportRequests` table, indexes and migration | 2 |
| `PersonalDataExportComposer` and six `IPersonalDataSection` implementations | 12 |
| `ExportDocumentGuard` | 3 |
| `GenerateDataExportHandler` with retry, failure and alert | 6 |
| `ObjectStorageExportFileStore` and the private `exports` container | 4 |
| Export-ready email template and dispatch | 3 |
| `DataExportExpiryJob` with the `privacy_export_oldest_pending_hours` metric and alert | 4 |
| Acceptance tests for the three `L2-055` criteria (API integration and Playwright) | 8 |
| Review fixes | 4 |
| **Total** | **74** |

## Minimal scope

The minimal scope keeps the dialog, the download page with ready, expired and not-found
states, the three endpoints, the entity, the six sections, background generation,
private storage, the ready email and file deletion after 7 days. It leaves out
`ExportDocumentGuard`, reuse of an open request, the pending-age metric and alert, and
the separate `Failed` handling beyond the outbox's own retries. It still satisfies
`L2-055`, with criterion 2 verified by tests instead of a run-time guard. It defers
early warning when an export is close to missing the 24-hour target. Minimal scope
totals **59** hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `ExportDocumentGuard` | Another member's email in the file is caught only by tests | 3 |
| Open-request reuse | Repeated clicks create duplicate jobs and duplicate emails | 1 |
| Pending-age metric and alert | No warning before the 24-hour target is missed | 2 |
| Explicit `Failed` state and alert | Failed exports stay in retry until the outbox gives up silently | 2 |
| Download page error and loading states; keep ready, expired and not-found | Plainer feedback on slow or failed loads | 2 |
