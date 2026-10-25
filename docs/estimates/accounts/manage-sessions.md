# Estimate — Manage sessions

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. Redis, the secret store, Data Protection and the platform anti-forgery handling already exist. The signing key name and rotation schedule (`<TO SUPPLY>`) are assumed to be configuration only. The Settings rows for data export and cookies link to dialogs estimated in the privacy subsystem.
[Detailed design](../../detailed-designs/accounts/manage-sessions/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `SessionStore` and `sessionInitializer` | 4 |
| `authRefreshInterceptor` with single-flight refresh and replay | 5 |
| `SessionExpiredPage` | 1 |
| `SettingsPage` with `loading` and `error` states | 5 |
| `SignOutEverywhereDialog` with `busy` and `failed` states | 3 |
| `JwtCookieAuthenticationHandler`, `AccessTokenFactory`, `RevokedSessionCheck` | 7 |
| `SessionCookieWriter` (3 cookies) | 2 |
| `SessionTokenService` start and second-factor upgrade | 4 |
| `RefreshTokenFamilyStore` with atomic Lua rotation | 6 |
| `RefreshSessionCommandHandler` with reuse detection | 4 |
| `SessionRevoker`, sign-out and sign-out-everywhere commands and endpoints | 5 |
| `MemberSession` entity, configuration and migration | 3 |
| `AccountSettingsController` and query | 2 |
| Lint rule against web-storage writes | 1 |
| Acceptance tests for `L2-008` criteria 1 to 6, including a 3-instance run | 10 |
| **Total** | **62** |

## Minimal scope

The minimal scope keeps cookie-held tokens, rotation with reuse detection, server-side sign-out and sign-out everywhere, satisfying every clause of `L2-008`. It drops the immediate revoked-session check (a revoked access token stays usable for at most 15 minutes, while its refresh token is refused at once), the session hint and the dedicated session-expired page (an ended session lands on the plain sign-in page), and the device count on Settings. Removing these items saves 5 hours.

**Minimal scope total: 57 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `RevokedSessionCheck` | A signed-out access token keeps working for up to 15 minutes | 2 |
| Session hint and `SessionExpiredPage` | Members returning after 14 days see the plain sign-in page instead of "Welcome back" | 2 |
| Device count on Settings | Settings no longer shows "Signed in on {n} devices" | 1 |
