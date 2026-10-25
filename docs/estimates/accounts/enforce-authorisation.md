# Estimate — Enforce authorisation

## Basis

The estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer who is productive in both stacks but new to this codebase.
Hours cover implementation, unit and acceptance tests, and review fixes; they exclude
requirements, design and mock work. The `NotSuspended` handler and `IMemberStatusReader` come from moderation/suspend-member, `AdministratorWithSecondFactor` from moderation/audit-log-and-admin-sign-in, and the error middleware from the platform. Applying the policies to each endpoint is counted in the feature that owns the endpoint; this estimate covers the shared parts and the cross-cutting tests.
[Detailed design](../../detailed-designs/accounts/enforce-authorisation/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| Policy catalogue, fallback policy, `MemberOnly` and `VerifiedMember` handlers | 5 |
| `ProblemDetailsAuthorizationResultHandler` | 3 |
| `ICurrentMember` | 1 |
| `OwnershipQueryExtensions` and `IOwnedByMember` | 3 |
| `AuthorizationBehavior` and `RequiresCapabilityAttribute` | 4 |
| Architecture tests for endpoint policy metadata | 3 |
| `authGuard`, `guestGuard` and `adminGuard` | 3 |
| `problemDetailsInterceptor` mappings | 4 |
| `ForbiddenPage` | 1 |
| Suspension states of the account banner, overview and Sell page hook | 3 |
| Acceptance tests for `L2-010` criteria 1 to 5, with a generated 401 sweep | 10 |
| **Total** | **40** |

## Minimal scope

The minimal scope keeps the policy catalogue, owner-scoped queries returning 404, the result handler and the acceptance tests, which satisfy every criterion of `L2-010`. It drops the MediatR `AuthorizationBehavior` defence in depth, the architecture tests (policy coverage is then checked in review), and the suspension states on the overview and banner (the API still refuses with 403 and a toast explains it). Removing these items saves 10 hours.

**Minimal scope total: 30 hours.**

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `AuthorizationBehavior` and `RequiresCapabilityAttribute` | No second check inside the application layer | 4 |
| Architecture tests for policy metadata | An endpoint without a policy is caught only in review | 3 |
| Suspension states on banner and overview | Suspended members learn of the restriction only when an action is refused | 3 |
