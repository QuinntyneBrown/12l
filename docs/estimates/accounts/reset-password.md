# Estimate — Reset or change a password

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. `PasswordPolicy`, `EmailLinkTokenIssuer` (register-account) and `SessionRevoker` (manage-sessions) already exist; the email templates are estimated in notifications. The hours assume the change-password path sends the confirmation email, which is `<TO SUPPLY>`.
[Detailed design](../../detailed-designs/accounts/reset-password/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `ForgotPasswordPage` with `invalid`, `submitting`, `success` and `error` states | 4 |
| `ResetPasswordPage` with `invalid`, `submitting`, `success`, `expired` and `error` states | 5 |
| `ChangePasswordDialog` with `invalid`, `busy` and `failed` states | 4 |
| `PasswordResetController` and `AccountPasswordController` | 3 |
| `RequestPasswordResetCommandHandler` with per-email limit and uniform response | 5 |
| `ResetPasswordCommandHandler` with token consumption and session revocation | 4 |
| `ChangePasswordCommandHandler` | 3 |
| `NewPasswordValidator`, `Member.ChangePassword` and `PasswordChanged` event | 2 |
| Acceptance tests for `L2-009` criteria 1 to 5 and the change-password dialog | 8 |
| **Total** | **38** |

## Minimal scope

The minimal scope delivers the forgot and reset pages with their rules, which satisfy every criterion of `L2-009`. It defers the change-password dialog on Settings; a signed-in member who wants a new password uses the reset flow instead. Removing these items saves 10 hours.

**Minimal scope total: 28 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| Change-password dialog and its endpoint | Signed-in members change their password only through the emailed reset link | 10 |
| Password-changed confirmation email on the change path | No email after a change from Settings; reset still emails | 1 |
