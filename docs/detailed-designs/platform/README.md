# Platform subsystem

The platform subsystem holds the cross-cutting capabilities that every 12L
feature inherits: HTTP and API hardening, credential and supply-chain
protection, performance budgets and stateless scaling, the responsive and
accessible application shell, error reporting and observability, and
availability and recovery. It refines `L1-013`, `L1-015`, `L1-016`, `L1-017` and
`L1-018`. Each feature is a vertical slice through middleware, the Angular shell,
infrastructure and CI, and each has an estimate in
[`docs/estimates/platform/`](../../estimates/platform/).

| Feature | L2 requirements |
|---------|-----------------|
| [harden-http-and-api](harden-http-and-api/README.md) | `L2-048`, `L2-049`, `L2-050`, `L2-051` |
| [protect-credentials-and-supply-chain](protect-credentials-and-supply-chain/README.md) | `L2-052`, `L2-053` |
| [meet-performance-and-scale](meet-performance-and-scale/README.md) | `L2-058`, `L2-060` |
| [responsive-accessible-shell](responsive-accessible-shell/README.md) | `L2-061`, `L2-062`, `L2-063`, `L2-064`, `L2-065` |
| [report-errors-and-observe](report-errors-and-observe/README.md) | `L2-068`, `L2-069`, `L2-070` |
| [keep-available-and-recoverable](keep-available-and-recoverable/README.md) | `L2-066`, `L2-067` |
