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

/// <summary>Public settings of the application.</summary>
public sealed class AppOptions
{
    /// <summary>Origin of 12L Web, used to build links in emails.</summary>
    public string BaseUrl { get; set; } = "http://localhost:4200";
}
