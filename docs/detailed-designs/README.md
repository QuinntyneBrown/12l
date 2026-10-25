# 12L detailed designs

This folder holds the detailed design of every 12L feature. Each design refines the
level-2 (L2) requirements in [`docs/specs/L2.md`](../specs/L2.md) and draws its screens
and states from the HTML mocks in [`docs/mocks/`](../mocks/README.md). Each feature
folder holds a `README.md` with four sections (Overview, Description, Requirements,
Diagrams) and a `diagrams/` folder of PlantUML sources and rendered PNGs. Each design
has a matching estimate in [`docs/estimates/`](../estimates/).

## Architecture baseline

Every feature design builds on the same baseline, so the names below recur across all
designs.

### Containers

| Container | Technology | Responsibility |
|-----------|------------|----------------|
| `12L Web` | Angular (TypeScript), standalone components, signals, lazy-loaded routes, in `src/frontend` | Responsive single-page application for visitors, members and administrators |
| `12L API` | ASP.NET Core Web API (C#), in `src/backend` | REST API over HTTPS; source of truth for every business rule, including the size rules |
| `12L Worker` | .NET worker service, in `src/backend` | Background jobs: outbox email dispatch, reservation expiry, order auto-completion, payouts, photo processing, data export and erasure |
| `12L database` | SQL Server through EF Core | Members, listings, orders, reviews, reports, audit log, outbox |
| `Distributed cache` | Redis | Rate-limit counters, refresh-token families and other state shared across API instances (`L2-060`) |
| `Photo storage` | Object storage behind a CDN | Original uploads (private) and processed, content-addressed photo versions (public through the CDN) |

### External systems

| System | Used for |
|--------|----------|
| `Payment provider` | PCI DSS compliant hosted card fields, payments, refunds, seller payout onboarding and payouts, signed webhooks (`L2-030`, `L2-031`) |
| `Email provider` | Transactional and marketing email (`L2-042`) |
| `Breached-password service` | k-anonymity lookup of known breached passwords (`L2-001`) |

The specific payment provider, email provider and hosting platform are `<TO SUPPLY>`.

### Backend solution layout

The C# namespace prefix is `TwelveL`, because a C# identifier cannot start with a digit.

| Project | Layer | Holds |
|---------|-------|-------|
| `TwelveL.Api` | API | Controllers, endpoint policies, middleware (problem details, correlation ID, security headers, rate limiting, anti-forgery) |
| `TwelveL.Application` | Application | MediatR commands, queries and handlers; FluentValidation validators; DTOs; interfaces for infrastructure ports |
| `TwelveL.Domain` | Domain | Entities, value objects, enumerations, domain events and state machines (`Member`, `Listing`, `Order`, `Review`, `Report`) |
| `TwelveL.Infrastructure` | Infrastructure | `TwelveLDbContext` (EF Core), repositories, outbox, adapters for the payment provider, email provider, photo storage and cache |
| `TwelveL.Worker` | Worker | Hosted background services that run the jobs listed above |

### Frontend layout

The Angular application groups code into lazy-loaded feature areas under
`src/frontend/src/app/`: `accounts`, `catalog`, `listings`, `orders`, `reviews`,
`moderation`, `privacy`, plus `core` (HTTP interceptors, auth state, error handling) and
`shared` (design-system components). Each feature area exposes route components
(pages), dialog components and a typed API service that calls `12L API`.

### Cross-cutting conventions

- **Sessions.** `12L API` issues a 15-minute access token and a rotating 14-day refresh token in `HttpOnly`, `Secure`, `SameSite=Strict` cookies (`L2-008`). The frontend never stores a token in web storage.
- **Authorisation.** Every endpoint applies a policy; resources the caller may not see return HTTP 404 (`L2-010`).
- **Errors.** Every API error is an RFC 9457 problem details response with a stable error code and a correlation ID (`L2-068`).
- **Outbox.** Handlers that must send email or call an external system write an outbox message in the same database transaction as the state change; `12L Worker` dispatches it with retry and back-off (`L2-042`).
- **Audit.** Every administrator action writes an append-only `AuditEntry` (`L2-047`).
- **Authorisation policies.** Endpoints use the policy catalogue defined in [enforce-authorisation](accounts/enforce-authorisation/README.md): `PublicRead`, `MemberOnly`, `VerifiedMember`, `NotSuspended`, `TradingMember` and `AdministratorWithSecondFactor`.
- **API paths.** Every endpoint sits under `/api/` with no version segment.
- **Error codes.** Catalog and listings designs write error codes in `UPPER_SNAKE` form; accounts, moderation, orders, notifications and privacy write them in `dotted.lower` form. The single convention is `<TO SUPPLY>` and shall be applied to all designs before implementation.

## Subsystems

| Subsystem | Scope (L1) | Features | Estimate (hours) |
|-----------|------------|----------|-----------------:|
| [accounts](accounts/) | `L1-001`, `L1-002` | register-account, verify-email, sign-in, manage-sessions, reset-password, edit-profile, close-account, enforce-authorisation | 361 |
| [listings](listings/) | `L1-003`, `L1-004` | create-listing, upload-listing-photos, edit-and-withdraw-listing, manage-my-listings | 210 |
| [catalog](catalog/) | `L1-005`, `L1-006` | browse-catalog, search-and-filter-catalog, view-listing-detail | 196 |
| [orders](orders/) | `L1-007`, `L1-008` | checkout-and-pay, seller-payouts, ship-order, complete-order, cancel-order, resolve-order-problems, order-history | 404 |
| [reviews](reviews/) | `L1-009`, `L1-010` | leave-review, view-member-profile | 136 |
| [notifications](notifications/) | `L1-011` | send-email-notifications, manage-notification-preferences | 114 |
| [moderation](moderation/) | `L1-012` | report-listing-or-member, moderate-reports, suspend-member, audit-log-and-admin-sign-in | 206 |
| [privacy](privacy/) | `L1-014` | protect-personal-data, export-personal-data, manage-cookie-consent | 176 |
| [platform](platform/) | `L1-013`, `L1-015` to `L1-018` | harden-http-and-api, protect-credentials-and-supply-chain, meet-performance-and-scale, responsive-accessible-shell, report-errors-and-observe, keep-available-and-recoverable | 360 |
| **Total** | | 39 features | **2163** |

Each estimate assumes an intermediate Angular/TypeScript and ASP.NET Core/C# developer and covers implementation, tests and review fixes. Per-feature figures, minimal scopes and descoping options are in [`docs/estimates/`](../estimates/).
