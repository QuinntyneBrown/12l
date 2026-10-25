# Accounts subsystem

The accounts subsystem covers membership and access control (`L1-001`, `L1-002`). It lets
a visitor join, verify their email and sign in. It keeps the member's session alive and
ends it on request. It recovers access through a password reset, lets the member edit
their profile and close their account, and defines the authorisation rules that every
`12L API` endpoint applies. The subsystem owns the `Member` aggregate, `EmailLinkToken`
and `MemberSession`, the `/api/accounts` and `/api/auth` endpoints, and the `accounts`
feature area of `12L Web`. Each design has an estimate in
[`docs/estimates/accounts/`](../../estimates/accounts/).

| Feature | L2 requirements | Estimate (hours) |
|---------|-----------------|-----------------:|
| [register-account](register-account/README.md) | `L2-001`, `L2-051`, `L2-052` | [55](../../estimates/accounts/register-account.md) |
| [verify-email](verify-email/README.md) | `L2-002`, `L2-003` | [51](../../estimates/accounts/verify-email.md) |
| [sign-in](sign-in/README.md) | `L2-006`, `L2-007` | [35](../../estimates/accounts/sign-in.md) |
| [manage-sessions](manage-sessions/README.md) | `L2-008` | [62](../../estimates/accounts/manage-sessions.md) |
| [reset-password](reset-password/README.md) | `L2-009` | [38](../../estimates/accounts/reset-password.md) |
| [edit-profile](edit-profile/README.md) | `L2-004` | [44](../../estimates/accounts/edit-profile.md) |
| [close-account](close-account/README.md) | `L2-005` | [36](../../estimates/accounts/close-account.md) |
| [enforce-authorisation](enforce-authorisation/README.md) | `L2-010` | [40](../../estimates/accounts/enforce-authorisation.md) |
