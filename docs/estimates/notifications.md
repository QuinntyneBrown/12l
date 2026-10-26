# Estimates: notifications

| Design | Effort | Complete |
|---|---|---|
| manage-notification-preferences | 3 days | 0% |
| send-email-notifications | 4 days | 85% |

send-email-notifications is at 85%: the outbox, the dispatcher with retry and back-off, the
content guard and the emails for every event built so far are done. The real provider adapter,
HTML layout, retention job and metrics wait for the provider, the final copy and the platform
observability work ([ADR notifications/0001](../adr/notifications/0001-email-outbox-plain-text-templates-and-provider-port.md)).
