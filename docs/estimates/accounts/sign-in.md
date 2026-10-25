# Estimate — Sign in

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. The hasher, the platform rate limiter and Redis connection, and `ISessionTokenService` (manage-sessions) already exist. The administrator TOTP step is estimated in moderation/audit-log-and-admin-sign-in; only the hand-off is counted here.
[Detailed design](../../detailed-designs/accounts/sign-in/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `SignInPage` with `return`, `invalid`, `submitting`, `locked`, throttled and `error` states; `ReturnUrlValidator` | 8 |
| `AuthApi.signIn`, post-sign-in navigation and administrator hand-off | 2 |
| `AuthController` sign-in endpoint and `sign-in` rate-limit policy | 3 |
| `SignInCommandHandler` with dummy hash, closed-account handling and rehash | 6 |
| `SignInLockout` Redis counters and lock keys | 5 |
| Lockout email enqueue | 1 |
| Security-event logging for failed attempts | 1 |
| Acceptance tests for `L2-006` criteria 1 to 4 and `L2-007` criteria 1 to 4 | 9 |
| **Total** | **35** |

## Minimal scope

The minimal scope keeps identical errors, account lockout with its email, and the IP limit, so `L2-006` and `L2-007` are both satisfied. It drops the "Sign in to buy" variant of the page (the return URL still works), the dedicated throttled state (the generic error alert shows instead), the transparent rehash on sign-in, and the dedicated security-event logging beyond the platform request log. Removing these items saves 4 hours.

**Minimal scope total: 31 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| "Sign in to buy" heading and lead | Context that the member returns to the listing | 1 |
| Dedicated throttled state | Specific wait-time message for the IP limit | 1 |
| Rehash on sign-in | Hashes keep their original iteration count after a configuration increase | 1 |
| Security-event logging for failures | Failed attempts are visible only in generic request logs | 1 |
