namespace TwelveL.Application.Notifications;

// The template model of each notification type (L2-042). No model has a property for a password,
// a card number or a security code: a card appears only as brand and last 4 digits, and a
// single-use token only inside the verification link that L2-002 requires.

public sealed record EmailVerificationEmail(string Link);

public sealed record SaleMadeEmail(Guid OrderId, string OrderReference, string ItemTitle, decimal Total, DateTime ShipBy);

public sealed record OrderShippedEmail(Guid OrderId, string OrderReference, string ItemTitle, string Carrier, string TrackingNumber, string TrackingUrl);

public sealed record OrderDeliveredEmail(Guid OrderId, string OrderReference, string ItemTitle);

public sealed record ShipByReminderEmail(Guid OrderId, string OrderReference, string ItemTitle, DateTime ShipBy);

/// <summary><paramref name="ToSeller"/> picks the seller's wording and the sale link instead of the buyer's order link.</summary>
public sealed record OrderCancelledEmail(Guid OrderId, string OrderReference, string ItemTitle, bool ToSeller);

public sealed record OrderRefundedEmail(Guid OrderId, string OrderReference, decimal Amount, string? CardBrand, string? CardLast4);
