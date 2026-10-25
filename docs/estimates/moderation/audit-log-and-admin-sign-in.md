# Estimate — Audit log and administrator sign-in

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in the stack but new to this codebase. It assumes that the accounts subsystem provides password sign-in, the session store and `ISessionTokenService`, and that only the `secondFactorRequired` flag and `UpgradeToSecondFactorAsync` are added here. It assumes the rate-limiting middleware and `AdminShellComponent` exist. TOTP enrolment, recovery and the purge policy are `<TO SUPPLY>` and are excluded; the estimate assumes credentials are provisioned by a one-off script, costed below. Hours cover implementation, tests and review fixes. [Detailed design](../../detailed-designs/moderation/audit-log-and-admin-sign-in/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `AdminVerifyPageComponent` with default, invalid, submitting and error states | 4 |
| `AdminAuthService`, sign-in hand-off, `adminGuard` and interceptor redirect on `auth.second_factor_required` | 4 |
| `AuditLogPageComponent` with filters in the URL and default, loading, empty, error and no-results states | 6 |
| `AdministratorWithSecondFactor` policy and `amr` claim handling in token issue and refresh | 4 |
| `AdminVerificationController`, `VerifyAdminSecondFactorCommand`, validator and handler | 4 |
| `TotpVerifier` with drift tolerance, replay guard and constant-time comparison | 4 |
| `AdministratorTotpCredential`, Data Protection secret, migration and provisioning script | 3 |
| `admin-verify` rate-limit policy and security-event logging | 2 |
| `AuditEntry`, `AuditAction`, `IAuditLog` / `AuditLog` writing in the caller's unit of work | 3 |
| `AuditLogController` with `GetAuditLogQueryHandler`, keyset paging and 405 change refusal | 4 |
| Append-only enforcement: `AuditEntryImmutabilityInterceptor`, grants and `TR_AuditEntries_Immutable` trigger in the migration | 4 |
| Backend acceptance tests for `L2-047` criteria 1 to 3 | 6 |
| Playwright acceptance tests for TOTP sign-in and the audit log page | 4 |
| **Total** | **52** |

## Minimal scope

The minimal version ships the append-only `AuditEntries` table written by `IAuditLog`, the read-only audit log page without filters, and the 405 refusal of change requests with the interceptor and database grants. It also ships the TOTP step with the verify page, the policy and the replay guard. It leaves out the `INSTEAD OF` trigger (grants and interceptor still refuse changes), the target and action filters, keyset paging, the dedicated `admin-verify` rate-limit policy (the general per-member limit of `L2-051` applies), and Playwright tests beyond sign-in. It satisfies `L2-047` criteria 1 to 3 and defers no requirement. Total: 38 hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Target and action filters on the audit log | Finding one target's history means scrolling | 3 |
| `TR_AuditEntries_Immutable` trigger | A privileged login could change entries outside the application | 1 |
| Keyset paging on the audit log | The page loads a fixed recent window only | 2 |
| Dedicated `admin-verify` rate-limit policy | TOTP guessing is limited only by the general per-member limit | 2 |
| Playwright audit log tests | Less end-to-end coverage of empty, error and no-results states | 2 |
