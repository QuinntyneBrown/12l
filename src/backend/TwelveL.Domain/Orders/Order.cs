using TwelveL.Domain.Payouts;

namespace TwelveL.Domain.Orders;

/// <summary>Order states (L2-032). Cancelled, Completed and Refunded are terminal.</summary>
public enum OrderStatus
{
    Paid,
    Shipped,
    Delivered,
    Completed,
    Cancelled,
    Refunded,
}

/// <summary>
/// One sale of one listing to one buyer, created from the provider's signed webhook (L2-030 AC2).
/// The database allows one order per listing and per checkout (L2-029). Every status change goes
/// through <see cref="TransitionTo"/>, which checks <see cref="OrderStateMachine"/> and appends
/// an <see cref="OrderStatusChange"/> (L2-032).
/// </summary>
public sealed class Order
{
    /// <summary>Business days the seller has to add tracking (L2-033).</summary>
    public const int ShipWithinBusinessDays = 5;

    /// <summary>Business days after payment at which an unshipped seller is reminded (L2-033 AC3).</summary>
    public const int RemindAfterBusinessDays = 3;

    /// <summary>How long after delivery a Delivered order completes by itself (L2-034 AC2).</summary>
    public static readonly TimeSpan AutoCompleteAfter = TimeSpan.FromDays(3);

    private readonly List<OrderStatusChange> _statusChanges = [];

    private Order()
    {
    }

    public Guid Id { get; private set; }

    /// <summary>Sequential public number; the reference is "12L-" followed by it.</summary>
    public long Number { get; private set; }

    public string Reference { get; private set; } = string.Empty;

    public Guid CheckoutId { get; private set; }

    public Guid ListingId { get; private set; }

    public Guid BuyerId { get; private set; }

    public Guid SellerId { get; private set; }

    public Guid PaymentId { get; private set; }

    public OrderStatus Status { get; private set; }

    public decimal ItemPrice { get; private set; }

    public decimal ShippingCost { get; private set; }

    public decimal SalesTax { get; private set; }

    public decimal Total { get; private set; }

    /// <summary>The 12L fee rate when the order was paid (0.10 for 10%); later configuration changes do not alter it (L2-031).</summary>
    public decimal FeeRate { get; private set; }

    /// <summary>The 12L fee on item plus shipping, recorded against the order (L2-031 AC2).</summary>
    public decimal FeeAmount { get; private set; }

    public ShippingAddress ShippingAddress { get; private set; } = null!;

    public DateTime PaidAt { get; private set; }

    /// <summary>When the seller must have added tracking: 5 business days after payment (L2-033).</summary>
    public DateTime ShipBy { get; private set; }

    /// <summary>When an unshipped seller is reminded: 3 business days after payment (L2-033 AC3).</summary>
    public DateTime ShipReminderDue { get; private set; }

    /// <summary>When the ship-by reminder was queued; null until then, so it is sent once.</summary>
    public DateTime? ShipReminderSentAt { get; private set; }

    public DateTime? ShippedAt { get; private set; }

    public DateTime? DeliveredAt { get; private set; }

    /// <summary>When the buyer confirmed receipt or the order completed automatically (L2-034).</summary>
    public DateTime? CompletedAt { get; private set; }

    /// <summary>When a Delivered order completes by itself: 3 days after delivery; null in any other status.</summary>
    public DateTime? AutoCompletesAt => Status == OrderStatus.Delivered ? DeliveredAt + AutoCompleteAfter : null;

    /// <summary>When the order reached a terminal status.</summary>
    public DateTime? EndedAt { get; private set; }

    public Carrier? Carrier { get; private set; }

    public string? TrackingNumber { get; private set; }

    /// <summary>The append-only history of transitions, oldest first.</summary>
    public IReadOnlyList<OrderStatusChange> StatusChanges => _statusChanges;

    public static string ReferenceFor(long number) => $"12L-{number}";

    /// <summary>
    /// The Paid order of a checkout whose payment succeeded, with the fee at <paramref name="feeRate"/>.
    /// The checkout must have an address and a tax quote.
    /// </summary>
    public static Order CreatePaid(long number, Checkout checkout, Guid sellerId, Payment payment, decimal feeRate, DateTime now)
    {
        var order = new Order
        {
            Id = Guid.NewGuid(),
            Number = number,
            Reference = ReferenceFor(number),
            CheckoutId = checkout.Id,
            ListingId = checkout.ListingId,
            BuyerId = checkout.BuyerId,
            SellerId = sellerId,
            PaymentId = payment.Id,
            Status = OrderStatus.Paid,
            ItemPrice = checkout.ItemPrice,
            ShippingCost = checkout.ShippingCost,
            SalesTax = checkout.SalesTax ?? throw new InvalidOperationException("The checkout has no tax."),
            Total = payment.Amount,
            FeeRate = feeRate,
            FeeAmount = PayoutFees.Fee(feeRate, checkout.ItemPrice + checkout.ShippingCost),
            ShippingAddress = checkout.Address ?? throw new InvalidOperationException("The checkout has no address."),
            PaidAt = now,
            ShipBy = BusinessDays.Add(now, ShipWithinBusinessDays),
            ShipReminderDue = BusinessDays.Add(now, RemindAfterBusinessDays),
        };
        order._statusChanges.Add(OrderStatusChange.Record(order.Id, null, OrderStatus.Paid, OrderActor.System, now));
        return order;
    }

    /// <summary>Whether the reminder job should remind the seller at <paramref name="now"/>: Paid, due and not yet reminded.</summary>
    public bool IsDueForShipReminder(DateTime now) => Status == OrderStatus.Paid && ShipReminderSentAt is null && ShipReminderDue <= now;

    /// <summary>Records that the ship-by reminder was queued, so the job does not send it again.</summary>
    public void MarkShipReminderSent(DateTime now)
    {
        if (!IsDueForShipReminder(now))
        {
            throw new InvalidOperationException("The order is not due for a ship-by reminder.");
        }

        ShipReminderSentAt = now;
    }

    /// <summary>The seller added a well-formed tracking number: Paid to Shipped.</summary>
    public void MarkShipped(Carrier carrier, string trackingNumber, DateTime now)
    {
        TransitionTo(OrderStatus.Shipped, OrderActor.Seller, now);
        Carrier = carrier;
        TrackingNumber = trackingNumber;
        ShippedAt = now;
    }

    /// <summary>The carrier reported delivery, or the buyer confirmed receipt: Shipped to Delivered.</summary>
    public void MarkDelivered(OrderActor actor, DateTime now)
    {
        TransitionTo(OrderStatus.Delivered, actor, now);
        DeliveredAt = now;
    }

    /// <summary>
    /// The buyer confirmed receipt (L2-034 AC1). A Shipped order first becomes Delivered, because
    /// L2-032 has no direct Shipped to Completed move; both changes are recorded against the buyer.
    /// </summary>
    public void ConfirmReceipt(DateTime now)
    {
        if (Status == OrderStatus.Shipped)
        {
            MarkDelivered(OrderActor.Buyer, now);
        }

        Complete(OrderActor.Buyer, now);
    }

    /// <summary>Delivered to Completed, by the buyer, the system after 3 days, or an administrator.</summary>
    public void Complete(OrderActor actor, DateTime now)
    {
        TransitionTo(OrderStatus.Completed, actor, now);
        CompletedAt = now;
    }

    /// <summary>Whether the completion job should complete this order at <paramref name="now"/> (L2-034 AC2).</summary>
    public bool IsDueForAutoCompletion(DateTime now) => AutoCompletesAt <= now;

    /// <summary>The seller cancelled, or the ship deadline passed: Paid to Cancelled.</summary>
    public void Cancel(OrderActor actor, DateTime now) => TransitionTo(OrderStatus.Cancelled, actor, now);

    /// <summary>The only path that changes <see cref="Status"/>; throws <see cref="InvalidOrderTransitionException"/> for any move L2-032 does not list.</summary>
    public void TransitionTo(OrderStatus to, OrderActor actor, DateTime now)
    {
        OrderStateMachine.EnsureAllowed(Status, to, actor);
        _statusChanges.Add(OrderStatusChange.Record(Id, Status, to, actor, now));
        Status = to;
        if (OrderStateMachine.IsTerminal(to))
        {
            EndedAt = now;
        }
    }
}
