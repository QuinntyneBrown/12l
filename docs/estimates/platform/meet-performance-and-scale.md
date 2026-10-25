# Estimate — Meet performance and scale targets

## Basis

The hours assume an intermediate Angular/TypeScript and ASP.NET Core/C# developer
who does not yet know the 12L codebase. They cover implementation, automated tests and review fixes, and
exclude requirements, design and mock work. They assume the lazy route files of
each feature area exist (each feature's estimate builds its own routes) and that
the rate-limit store of harden-http-and-api and the token store of accounts
exist. Tuning queries is counted in the owning feature's estimate. No load or
scale tests are built ([ADR 0002](../../adr/general/0002-no-load-or-scale-tests.md)).
[Detailed design](../../detailed-designs/platform/meet-performance-and-scale/README.md)

## Full design

| Work item | Hours |
|-----------|------:|
| `app.routes.ts` with lazy `loadChildren` per feature area and `FlagPreloadingStrategy` | 4 |
| `angular.json` budgets, `check-bundle-budget.mjs` (gzip of initial chunks) | 4 |
| `check-lazy-chunks.mjs` and `e2e/lazy-loading.spec.ts` | 4 |
| Lighthouse CI configuration with stub API and mobile assertions | 5 |
| `WebVitalsReporter` and `TelemetryController` with histograms | 5 |
| `EndpointKindAttribute` tagging and its use in metrics | 2 |
| `RedisConnectionFactory` and Data Protection key ring in Redis | 3 |
| `StatelessApiTests` architecture test | 2 |
| `DbContext` pooling, read/write command timeouts, read-path conventions sample and checklist | 2 |
| **Total** | **31** |

## Minimal scope

The minimal version ships lazy feature routes without a preloading strategy, the
gzip bundle check, the lazy-chunk check, Lighthouse CI on the catalog and listing
pages, the Data Protection key ring in Redis and the stateless architecture
test. It drops `WebVitalsReporter` and `TelemetryController` (INP is then checked
only through the lab proxy), the Playwright lazy-loading test and
`EndpointKindAttribute`. It still satisfies the acceptance criteria of `L2-058`
and `L2-060`. Minimal total: **21** hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `WebVitalsReporter` and telemetry endpoint | No field INP, LCP or CLS data from real devices | 5 |
| `FlagPreloadingStrategy` | Listing detail opens slightly slower after the catalog | 1 |
| `e2e/lazy-loading.spec.ts` | Lazy split is checked from `stats.json` only, not from network requests | 2 |
