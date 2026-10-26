using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using TwelveL.Domain.Listings;
using TwelveL.Domain.Members;
using TwelveL.Domain.Orders;

namespace TwelveL.Application.Abstractions;

/// <summary>The unit of work over 12L database. Implemented by TwelveLDbContext in Infrastructure.</summary>
public interface ITwelveLDbContext
{
    DbSet<Member> Members { get; }

    DbSet<EmailVerificationToken> EmailVerificationTokens { get; }

    DbSet<Session> Sessions { get; }

    DbSet<Listing> Listings { get; }

    DbSet<ListingPhoto> ListingPhotos { get; }

    DbSet<Checkout> Checkouts { get; }

    DbSet<Payment> Payments { get; }

    DbSet<Refund> Refunds { get; }

    DbSet<Order> Orders { get; }

    DbSet<SavedAddress> SavedAddresses { get; }

    DbSet<PaymentWebhookEvent> PaymentWebhookEvents { get; }

    /// <summary>Transactions, for the steps of checkout that must commit together.</summary>
    DatabaseFacade Database { get; }

    Task<int> SaveChangesAsync(CancellationToken cancellationToken);
}

/// <summary>Hashes and checks member passwords.</summary>
public interface IPasswordHasher
{
    string Hash(string password);

    bool Verify(string hash, string password);
}

/// <summary>Known breached passwords (L2-001).</summary>
public interface IBreachedPasswords
{
    bool Contains(string password);
}

/// <summary>Sends one email. The send-email-notifications feature replaces the logging adapter.</summary>
public interface IEmailSender
{
    Task SendAsync(EmailMessage message, CancellationToken cancellationToken);
}

public sealed record EmailMessage(string To, string Subject, string Body);

/// <summary>Reads whether a seller finished payout onboarding (L2-031). Owned by seller-payouts.</summary>
public interface ISellerPayoutAccountReader
{
    Task<bool> IsOnboardedAsync(Guid sellerId, CancellationToken cancellationToken);
}

/// <summary>An image identified from its content (magic bytes and header), not its name (L2-017).</summary>
public sealed record ImageInfo(string ContentType, int Width, int Height);

/// <summary>Reads the type and the displayed dimensions of an image without decoding all of it.</summary>
public interface IImageInspector
{
    /// <summary>The image, or null when the content is not JPEG, PNG or WebP.</summary>
    ImageInfo? Inspect(byte[] content);
}

/// <summary>One re-encoded photo version before it is stored.</summary>
public sealed record ProcessedPhotoVersion(int Size, PhotoFormat Format, int Width, int Height, byte[] Content);

/// <summary>
/// Applies the orientation, drops every metadata block (EXIF, XMP, IPTC, GPS, ICC) and re-encodes
/// the photo at each target width as WebP and JPEG, never upscaling (L2-017, L2-059).
/// </summary>
public interface IListingPhotoProcessor
{
    IReadOnlyList<ProcessedPhotoVersion> Process(byte[] original, IReadOnlyList<int> sizes);
}

/// <summary>A stored object and its content type.</summary>
public sealed record StoredObject(byte[] Content, string ContentType);

/// <summary>
/// Photo object storage. Originals are private; versions are public and immutable under their
/// content-addressed key. Real object storage and the CDN stay behind this port.
/// </summary>
public interface IPhotoStorage
{
    Task SaveOriginalAsync(string key, byte[] content, string contentType, CancellationToken cancellationToken);

    Task SavePublicAsync(string key, byte[] content, string contentType, CancellationToken cancellationToken);

    Task<StoredObject?> ReadPublicAsync(string key, CancellationToken cancellationToken);
}

/// <summary>A payment to create at the provider. The key makes a repeated request charge once (L2-030 AC6).</summary>
public sealed record PaymentRequest(Guid PaymentId, Guid CheckoutId, Guid ListingId, decimal Amount, string PaymentMethodToken, Guid IdempotencyKey);

/// <summary>Kinds of provider webhook events 12L acts on.</summary>
public enum PaymentEventType
{
    Succeeded,
    Failed,
}

/// <summary>
/// One verified provider webhook event. PaymentId is the 12L payment ID sent as metadata with the
/// payment; the card brand and last four digits are the only card details it carries (L2-030).
/// </summary>
public sealed record PaymentEvent(
    string EventId,
    PaymentEventType Type,
    Guid PaymentId,
    string ProviderPaymentId,
    string? CardBrand,
    string? CardLast4,
    string? DeclineReason);

/// <summary>
/// The PCI DSS compliant payment provider (L2-030). Card details go from the provider's hosted
/// fields to the provider; 12L only ever holds the payment method token. Tests use a fake.
/// </summary>
public interface IPaymentProvider
{
    /// <summary>Sales tax on item plus shipping for this US address, as the provider computes it.</summary>
    Task<decimal> QuoteTaxAsync(decimal taxableAmount, ShippingAddress address, CancellationToken cancellationToken);

    /// <summary>Asks the provider to charge the token; the result arrives later by webhook. Returns the provider's payment ID.</summary>
    Task<string> CreatePaymentAsync(PaymentRequest request, CancellationToken cancellationToken);

    /// <summary>Refunds a payment in full; the key makes a repeated call refund once. Returns the provider's refund ID.</summary>
    Task<string> RefundAsync(string providerPaymentId, decimal amount, Guid idempotencyKey, CancellationToken cancellationToken);

    /// <summary>The event when the signature over the raw body is valid, otherwise null (L2-030 AC4).</summary>
    PaymentEvent? ReadWebhook(string body, string? signature);
}

/// <summary>Public settings of the application.</summary>
public sealed class AppOptions
{
    /// <summary>Origin of 12L Web, used to build links in emails.</summary>
    public string BaseUrl { get; set; } = "http://localhost:4200";
}
