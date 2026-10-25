# Privacy subsystem

The privacy subsystem realizes `L1-014`: 12L collects only the personal data it needs,
keeps it private, protects it at rest and in transit, and lets members export their
data. It supplies the public DTO allow-list and field-level encryption that other
subsystems build on, the background data export, and the cookie consent banner and
dialog. Account closure and erasure (`L2-005`) belong to the accounts subsystem.

| Feature | L2 | Estimate |
|---------|----|----------|
| [protect-personal-data](protect-personal-data/README.md) | `L2-054` | [65 hours](../../estimates/privacy/protect-personal-data.md) |
| [export-personal-data](export-personal-data/README.md) | `L2-055` | [74 hours](../../estimates/privacy/export-personal-data.md) |
| [manage-cookie-consent](manage-cookie-consent/README.md) | `L2-056` | [37 hours](../../estimates/privacy/manage-cookie-consent.md) |
