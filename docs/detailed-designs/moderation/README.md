# Moderation

The moderation subsystem realizes `L1-012` (trust, safety and moderation). Verified members report listings and members that break the marketplace rules. Administrators work through a queue of open reports and order problems, oldest first. They dismiss reports, remove listings and suspend or reinstate members, and every action lands in an append-only audit log. Administrators reach this area only after a TOTP second factor. Order cancellation, refunds and order-problem resolution belong to the [orders](../orders/) subsystem; this subsystem calls them through ports.

| Feature | L2 requirements | Design | Estimate |
|---------|-----------------|--------|----------|
| Report a listing or member | `L2-044`, `L2-010` | [report-listing-or-member](report-listing-or-member/README.md) | [estimate](../../estimates/moderation/report-listing-or-member.md) |
| Moderate reports | `L2-045`, `L2-044`, `L2-010` | [moderate-reports](moderate-reports/README.md) | [estimate](../../estimates/moderation/moderate-reports.md) |
| Suspend and reinstate a member | `L2-046`, `L2-010` | [suspend-member](suspend-member/README.md) | [estimate](../../estimates/moderation/suspend-member.md) |
| Audit log and administrator sign-in | `L2-047`, `L2-006`, `L2-010` | [audit-log-and-admin-sign-in](audit-log-and-admin-sign-in/README.md) | [estimate](../../estimates/moderation/audit-log-and-admin-sign-in.md) |
