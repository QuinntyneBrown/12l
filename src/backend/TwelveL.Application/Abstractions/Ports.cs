using Microsoft.EntityFrameworkCore;
using TwelveL.Domain.Listings;
using TwelveL.Domain.Members;

namespace TwelveL.Application.Abstractions;

/// <summary>The unit of work over 12L database. Implemented by TwelveLDbContext in Infrastructure.</summary>
public interface ITwelveLDbContext
{
    DbSet<Member> Members { get; }

    DbSet<EmailVerificationToken> EmailVerificationTokens { get; }

    DbSet<Session> Sessions { get; }

    DbSet<Listing> Listings { get; }

    DbSet<ListingPhoto> ListingPhotos { get; }

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

/// <summary>Public settings of the application.</summary>
public sealed class AppOptions
{
    /// <summary>Origin of 12L Web, used to build links in emails.</summary>
    public string BaseUrl { get; set; } = "http://localhost:4200";
}
