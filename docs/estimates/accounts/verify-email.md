# Estimate — Verify email

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. The `EmailLinkToken` entity and issuer come from register-account, `SessionStore` from manage-sessions, and the email template and dispatch from notifications. The overview stat counts rely on read ports that the listings and orders subsystems implement; their implementation is outside these hours.
[Detailed design](../../detailed-designs/accounts/verify-email/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `VerifyEmailPage` with `loading`, verified, `expired`, `used` and `error` states | 5 |
| `VerifyEmailPromptDialog` with `busy`, `sent` and `limited` states | 4 |
| `AccountBannerComponent` `info`, `warning` and `success` states | 4 |
| `AccountLayout` tabs and `AccountOverviewPage` with 5 states | 8 |
| `EmailVerificationController` (3 endpoints) and `AccountOverviewController` | 4 |
| `VerifyEmailCommandHandler` and `EmailLinkToken.StateAt` / `Consume` | 5 |
| `ResendVerificationEmailCommandHandler` and `VerificationResendLimiter` | 4 |
| `MemberVerificationReader` and `VerifiedMember` handler hook-up | 3 |
| Overview query and the `IMemberListingCounts` / `IMemberOrderCounts` port contracts | 4 |
| Acceptance tests for `L2-002` criteria 1 to 6 and `L2-003` criteria 1 and 2 | 10 |
| **Total** | **51** |

## Minimal scope

The minimal scope keeps the verification page, the resend endpoint with its limit, and the 403 gate, which together satisfy `L2-002` and `L2-003`. It drops the anonymous resend from an expired link (the member signs in to resend), the `info` and `success` banner states (the persistent `warning` banner stays), and the overview stat tiles, leaving the overview with its greeting and the unverified alert. Removing these items saves 10 hours.

**Minimal scope total: 41 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Anonymous resend from an expired link | A member without a session signs in before resending | 2 |
| Banner `info` and `success` states | Confirmation after joining and after verifying is shown only on the pages themselves | 2 |
| Overview stat tiles and count ports | The overview shows no listing, sale or purchase counts | 6 |
