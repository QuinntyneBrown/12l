# ADR-0005: Marketing Size Wording and the Deferred Size-Lock Widening

**Date:** 2026-10-26
**Category:** general
**Status:** Accepted
**Deciders:** Quinntyne Brown (product owner)

## Context

The marketing page (`/welcome`) and its 30-second pitch video were asked to soften
"12 and L only": mainly men's US 12 shoes and L-and-up clothing, with 11 to 11.5 shoes and
XXL-and-up clothing "on rare occasions". The product does not accept those sizes. The size
lock (`L1-003`, `L2-011` to `L2-014`) and the API take only men's US 12 shoes and men's L
clothing and reject anything else. Copy that promises other sizes would send visitors to a
catalog and a sell form that refuse them.

## Decision

The marketing copy and narration use wording that is true today and stays true if the lock
ever widens: "Built for size 12 and L", "Big sizes, finally in one place", "Every pair is a
men's US 12", "Everything already fits you". They never say "only", and never name 11, 11.5,
XL or XXL. The size rules, the domain, the API and the sell page do not change.

Widening the size lock to 11 to 11.5 shoes and L, XL, XXL and up clothing is **deferred**.
It is a product decision that needs new L2 requirements (sizes per category, size tags,
filters, the catalog hero "Size 12. Size L. Nothing else.", the rules page), a domain and
API change and a data migration.

## Options Considered

### Option 1: Neutral wording, defer the widening (chosen)
- **Pros:** No false promise; no change outside the marketing feature; copy survives a
  later widening.
- **Cons:** The softer message the request asked for is not said outright.

### Option 2: Say "mostly 12 and L, sometimes 11 to 11.5 and XXL+"
- **Pros:** Matches the request word for word.
- **Cons:** Contradicts the API, the sell page and the rules page; visitors hit rejections.

### Option 3: Widen the size lock now
- **Pros:** Copy and product agree on the wider range.
- **Cons:** Out of scope for a marketing page; touches every subsystem.

## Consequences

### Positive
- The page and video are accurate against `L2-012` and `L2-013`.

### Negative
- The open question stays open until the product owner decides.

### Risks
- A later widening must re-check the page copy and re-record the video narration
  (`docs/mocks/_build/video/build_video.py`, `LINES`). Mitigation: the copy avoids "only".

## Open question

Should the size lock widen to men's US 11 to 11.5 shoes and men's L, XL, XXL and up
clothing? Deferred to the product owner.

## References

- [marketing-page design](../../detailed-designs/platform/marketing-page/README.md)
- `docs/specs/L2.md` (`L2-012`, `L2-013`, `L2-078` to `L2-083`)
