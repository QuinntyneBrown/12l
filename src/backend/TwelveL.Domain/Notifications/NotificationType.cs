namespace TwelveL.Domain.Notifications;

/// <summary>
/// The emails 12L sends (L2-042) for events that exist in the code. Each has a template and a deep
/// link; types for features not built yet (password reset, lockout, problems, reviews) are added
/// with those features.
/// </summary>
public enum NotificationType
{
    EmailVerification,
    SaleMade,
    OrderShipped,
    OrderDelivered,
    ShipByReminder,
    OrderCancelled,
    OrderRefunded,
    CancellationRequested,
}
