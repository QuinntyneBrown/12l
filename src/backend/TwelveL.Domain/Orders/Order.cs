namespace TwelveL.Domain.Orders;

/// <summary>Order states. Checkout creates Paid orders; ship-order adds the states after it.</summary>
public enum OrderStatus
{
    Paid,
}

/// <summary>
/// One sale of one listing to one buyer, created from the provider's signed webhook (L2-030 AC2).
/// The database allows one order per listing and per checkout (L2-029).
/// </summary>
public sealed class Order
{
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

    public ShippingAddress ShippingAddress { get; private set; } = null!;

    public DateTime PaidAt { get; private set; }

    public static string ReferenceFor(long number) => $"12L-{number}";

    /// <summary>The Paid order of a checkout whose payment succeeded. The checkout must have an address and a tax quote.</summary>
    public static Order CreatePaid(long number, Checkout checkout, Guid sellerId, Payment payment, DateTime now) => new()
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
        ShippingAddress = checkout.Address ?? throw new InvalidOperationException("The checkout has no address."),
        PaidAt = now,
    };
}
