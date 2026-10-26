namespace TwelveL.Domain.Orders;

public enum RefundReason
{
    DuplicatePayment,
    ShipDeadlinePassed,
}

public enum RefundStatus
{
    Pending,
    Issued,
}

/// <summary>
/// Money returned to a buyer. A payment for a listing that already has an order (L2-029 AC2) and
/// an order cancelled because the ship deadline passed (L2-033 AC2) are refunded in full.
/// </summary>
public sealed class Refund
{
    private Refund()
    {
    }

    public Guid Id { get; private set; }

    public Guid PaymentId { get; private set; }

    public decimal Amount { get; private set; }

    public RefundReason Reason { get; private set; }

    public RefundStatus Status { get; private set; }

    public string? ProviderRefundId { get; private set; }

    public DateTime CreatedAt { get; private set; }

    public static Refund ForDuplicate(Payment payment, DateTime now) => new()
    {
        Id = Guid.NewGuid(),
        PaymentId = payment.Id,
        Amount = payment.Amount,
        Reason = RefundReason.DuplicatePayment,
        Status = RefundStatus.Pending,
        CreatedAt = now,
    };

    public static Refund ForMissedShipDeadline(Payment payment, DateTime now) => new()
    {
        Id = Guid.NewGuid(),
        PaymentId = payment.Id,
        Amount = payment.Amount,
        Reason = RefundReason.ShipDeadlinePassed,
        Status = RefundStatus.Pending,
        CreatedAt = now,
    };

    public void Issued(string providerRefundId)
    {
        Status = RefundStatus.Issued;
        ProviderRefundId = providerRefundId;
    }
}
