# Estimate — Register an account

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. The platform rate limiter, `IPasswordHasher`, `ValidationBehavior`, anti-forgery handling and the notifications outbox (`INotificationPublisher`) already exist. `ISessionTokenService` is built in manage-sessions and only called here. The hours assume the breached-password service is reachable from test environments through a stub; the fail-open or fail-closed decision (`<TO SUPPLY>`) does not change the number.
[Detailed design](../../detailed-designs/accounts/register-account/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `RegisterPage` form with error summary and the `default`, `invalid`, `submitting`, `success`, `error` and rate-limited states | 10 |
| `AccountsApi.register` and shared `FormErrorMapper` | 3 |
| `AccountsController` `POST /api/accounts`, `RegisterRequest`, `register` rate-limit policy wiring | 3 |
| `RegisterMemberCommand`, validator and handler with uniqueness checks and one-transaction save | 8 |
| `Member.Register`, `DisplayName` and `EmailAddress` value objects, `MemberStatus` | 4 |
| `PasswordPolicy` length and breach rules | 2 |
| `BreachedPasswordClient` k-anonymity lookup with cache and timeout | 6 |
| `EmailLinkTokenIssuer` and `EmailLinkToken` entity | 3 |
| EF Core configuration and migration for `Members`, `MemberRoles`, `EmailLinkTokens` | 4 |
| Verification email enqueue and session start on registration | 2 |
| Acceptance tests for `L2-001` criteria 1 to 7, `L2-051` criterion 3, `L2-052` criterion 1 | 10 |
| **Total** | **55** |

## Minimal scope

The minimal scope keeps every server rule of `L2-001`, the IP limit of `L2-051` and hashed storage under `L2-052`, because all three are mandatory for a safe join flow. It drops the client-side mirror of the validation rules, so errors appear only after submission, and the breached-range cache, so every registration calls the external service. It also skips the automatic sign-in after registration: the member signs in before using "Resend email". The rate-limited state reuses the generic error alert. All three L2 requirements remain satisfied; nothing is deferred. Removing these items saves 8 hours.

**Minimal scope total: 47 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Client-side validation mirror; server errors only | Instant feedback before submission | 3 |
| Breached-range cache | Repeat lookups for common prefixes; more calls to the external service | 2 |
| Automatic sign-in after registration | Banner and "Resend email" need a separate sign-in first | 2 |
| Dedicated rate-limited state; reuse the generic error alert | Specific wait-time message | 1 |
