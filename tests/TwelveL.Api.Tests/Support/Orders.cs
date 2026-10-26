using System.Net.Http.Json;
using TwelveL.Domain.Members;

namespace TwelveL.Api.Tests.Support;

/// <summary>Seeding and calls for the order endpoints of ship-order.</summary>
public static class Orders
{
    public const string UspsNumber = "9400 1118 9922 3456 1204 77";

    /// <summary>
    /// A Paid order bought by the signed-in <paramref name="buyer"/> through checkout and the signed
    /// payment webhook, from a new seller. Returns the order ID and a client signed in as the seller.
    /// </summary>
    public static async Task<(Guid OrderId, HttpClient Seller)> SeedPaidOrderAsync(this TwelveLApiFactory factory, HttpClient buyer, long listingNumber = 30001)
    {
        Member seller = null!;
        factory.InDatabase(db =>
        {
            seller = Member.Register($"kicks_{listingNumber}", $"kicks{listingNumber}@example.com", "hash", DateTime.UtcNow);
            seller.MarkEmailVerified(DateTime.UtcNow);
            db.Members.Add(seller);
            db.SaveChanges();
        });
        var (checkout, payment) = await buyer.CheckoutAndPayAsync(factory.SeedActiveListing(seller.Id, listingNumber));
        using var provider = factory.CreateMemberClient();
        (await provider.PostWebhookAsync(FakePaymentProvider.Webhook(payment.Id))).EnsureSuccessStatusCode();
        var orderId = (await buyer.GetFromJsonAsync<CheckoutView>($"/api/checkouts/{checkout.Id}"))!.OrderId!.Value;
        return (orderId, factory.CreateMemberClient().WithSession(factory, seller));
    }

    public static Task<HttpResponseMessage> AddTrackingAsync(this HttpClient client, Guid orderId, string carrier = "USPS", string trackingNumber = UspsNumber) =>
        client.PostAsJsonAsync($"/api/orders/{orderId}/shipment", new { carrier, trackingNumber });

    public static Task<HttpResponseMessage> PostCarrierWebhookAsync(this HttpClient client, string body, string? signature = null)
    {
        var request = new HttpRequestMessage(HttpMethod.Post, "/api/carriers/webhook") { Content = new StringContent(body, System.Text.Encoding.UTF8, "application/json") };
        request.Headers.Add("Carrier-Signature", signature ?? FakeCarrierTracking.Sign(body));
        return client.SendAsync(request);
    }
}

public sealed record TimelineStepView(string Status, DateTime? At);

public sealed record TrackingView(string Carrier, string Number, string Url);

public sealed record SaleView(
    Guid Id,
    string Reference,
    string Status,
    DateTime PaidAt,
    DateTime ShipBy,
    CheckoutItemView Item,
    string ItemPrice,
    string ShippingCost,
    string SalesTax,
    string Total,
    string BuyerDisplayName,
    AddressView ShipTo,
    IReadOnlyList<TimelineStepView> Timeline,
    TrackingView? Tracking);

public sealed record OrderView(Guid Id, string Reference, string Status, DateTime ShipBy, IReadOnlyList<TimelineStepView> Timeline, TrackingView? Tracking);
