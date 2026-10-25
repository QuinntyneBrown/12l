# Estimate — Report a listing or member

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in the stack but new to this codebase. It assumes that the accounts subsystem already provides authentication, the `VerifiedMember` policy and the problem-details middleware. It also assumes that `suspend-member` supplies the `NotSuspended` policy, and that the shared dialog, radio-choice and textarea components exist in `shared`. Applying the catalog visibility rule inside catalog queries is costed in the catalog subsystem. The `<TO SUPPLY>` details length limit does not move the number. Hours cover implementation, unit and acceptance tests, and review fixes. [Detailed design](../../detailed-designs/moderation/report-listing-or-member/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `ReportListingDialogComponent` with default, invalid, busy, success and already states | 6 |
| `ReportMemberDialogComponent` with default, invalid, busy, success and already states | 4 |
| `ReportsApiService` with 409 and 422 mapping, and report links on listing detail and profile pages | 3 |
| `ReportsController` `POST /api/reports` with policies and status-code mapping | 3 |
| `SubmitReportCommand`, `SubmitReportCommandValidator` and the two reason enumerations | 3 |
| `SubmitReportCommandHandler` with target resolution, own-target refusal, duplicate check and retry on concurrency | 6 |
| `Report` aggregate, `ReportSubmission`, `AddSubmission` and auto-hide rule with `Listing.HidePendingReview` | 4 |
| EF Core configuration and migration: `Reports`, `ReportSubmissions`, `ReportNumbers` sequence, filtered and unique indexes, `Listings` hidden columns | 4 |
| `ListingHiddenPendingReview` domain event and `ModerationOptions` binding | 2 |
| Backend acceptance tests for `L2-044` criteria 1 to 4, including concurrent third reporter | 6 |
| Playwright acceptance tests for both dialogs | 4 |
| **Total** | **45** |

## Minimal scope

The minimal version ships listing reports only, through `ReportListingDialogComponent` and `POST /api/reports`. It keeps the reason set, the "Other" details rule, the database-enforced once-per-member rule (HTTP 409) and the auto-hide at 3 distinct reporters. It leaves out member reports, the concurrency retry (a rare conflict returns an error and the member retries), the domain event for cache eviction, and the Playwright tests beyond the happy path. It satisfies the listing half of `L2-044` and the `L2-010` refusals for reporting, and defers member reporting from `L2-044`. Total: 30 hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `ReportMemberDialogComponent` and member target handling | Members cannot report other members | 6 |
| Concurrency retry in `SubmitReportCommandHandler` | A conflicting concurrent submission returns an error instead of succeeding | 2 |
| `ListingHiddenPendingReview` event for cache eviction | A hidden listing may stay in a cached catalog page until the cache expires | 1 |
| Playwright tests reduced to the listing happy path | Less end-to-end coverage of invalid and already states | 2 |
