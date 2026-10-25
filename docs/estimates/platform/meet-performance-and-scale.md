# Estimate — Meet performance and scale targets

## Basis

The hours assume an intermediate Angular/TypeScript and ASP.NET Core/C# developer
who has used k6 or a similar load tool once before and does not yet know the 12L
codebase. They cover implementation, automated tests and review fixes, and
exclude requirements, design and mock work. They assume the lazy route files of
each feature area exist (each feature's estimate builds its own routes) and that
the rate-limit store of harden-http-and-api and the token store of accounts
exist. Provisioning the performance environment is `<TO SUPPLY>` and not
counted; tuning queries that miss the latency budget is counted in the owning
feature's estimate.
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
| `TwelveL.LoadTestSeeder` for 100,000 Active listings | 6 |
| k6 scenarios and thresholds; `load-test.yml` workflow | 8 |
| `docker-compose.scale.yml` and `TwelveL.ScaleTests` (session, reservation, rate limit across 3 instances) | 8 |
| **Total** | **53** |

## Minimal scope

The minimal version ships lazy feature routes without a preloading strategy, the
gzip bundle check, the lazy-chunk check, Lighthouse CI on the catalog and listing
pages, the Data Protection key ring in Redis, the k6 read and write scenarios with
the seeder, and the three-instance scale tests. It drops `WebVitalsReporter` and
`TelemetryController` (INP is then checked only through the lab proxy), the
Playwright lazy-loading test, `EndpointKindAttribute` and the stateless
architecture test. It still satisfies the acceptance criteria of `L2-057`,
`L2-058` and `L2-060`. Minimal total: **41** hours.

## Partial descoping

| Descope | What is lost | Hours saved |
|---------|--------------|------------:|
| `WebVitalsReporter` and telemetry endpoint | No field INP, LCP or CLS data from real devices | 5 |
| `FlagPreloadingStrategy` | Listing detail opens slightly slower after the catalog | 1 |
| `e2e/lazy-loading.spec.ts` | Lazy split is checked from `stats.json` only, not from network requests | 2 |
| `StatelessApiTests` | An in-memory state regression is caught only by the scale tests | 2 |
| Scale tests run on demand instead of each pull request (no CI wiring) | Multi-instance regressions surface later | 2 |
