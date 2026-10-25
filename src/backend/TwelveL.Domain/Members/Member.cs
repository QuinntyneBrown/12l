namespace TwelveL.Domain.Members;

/// <summary>A registered person who can buy and sell once their email is verified (L2-001, L2-002, L2-003).</summary>
public sealed class Member
{
    private Member()
    {
    }

    public Guid Id { get; private set; }

    public string DisplayName { get; private set; } = string.Empty;

    /// <summary>Upper-cased display name, unique, so names compare ignoring case.</summary>
    public string NormalizedDisplayName { get; private set; } = string.Empty;

    public string Email { get; private set; } = string.Empty;

    /// <summary>Upper-cased email, unique, so addresses compare ignoring case.</summary>
    public string NormalizedEmail { get; private set; } = string.Empty;

    public string PasswordHash { get; private set; } = string.Empty;

    public DateTime CreatedAt { get; private set; }

    public DateTime? EmailVerifiedAt { get; private set; }

    public bool IsEmailVerified => EmailVerifiedAt is not null;

    public static Member Register(string displayName, string email, string passwordHash, DateTime now) => new()
    {
        Id = Guid.NewGuid(),
        DisplayName = displayName,
        NormalizedDisplayName = Normalize(displayName),
        Email = email,
        NormalizedEmail = Normalize(email),
        PasswordHash = passwordHash,
        CreatedAt = now,
    };

    public static string Normalize(string value) => value.Trim().ToUpperInvariant();

    public void MarkEmailVerified(DateTime now)
    {
        EmailVerifiedAt ??= now;
    }
}
