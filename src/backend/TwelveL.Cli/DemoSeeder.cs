using System.Text.Json;
using System.Web;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using TwelveL.Application.Accounts;
using TwelveL.Application.Common;
using TwelveL.Domain.Members;
using TwelveL.Domain.Notifications;
using TwelveL.Infrastructure.Persistence;

namespace TwelveL.Cli;

/// <summary>
/// Loads the demo catalogue through the same MediatR commands as the API, so every account,
/// listing and photo rule applies (L2-074, L2-075). Runs once: an existing demo is left alone (L2-076).
/// </summary>
public sealed class DemoSeeder(ISender sender, TwelveLDbContext db, SeedClock clock, IConfiguration configuration)
{
    /// <summary>The demo members register this long before the seed, before their first listing.</summary>
    public static readonly TimeSpan MembersJoinedBefore = TimeSpan.FromDays(31);

    private const string SuppressionReason = "Demo member verified by TwelveL.Cli";

    /// <summary>Where the seed photos are: Seed:PhotosPath, or SeedPhotos next to the tool.</summary>
    public string PhotosPath => configuration["Seed:PhotosPath"] is { Length: > 0 } path ? path : Path.Combine(AppContext.BaseDirectory, "SeedPhotos");

    /// <summary>The first seed photo that is not on disk, or null when every one is (L2-077).</summary>
    public string? FindMissingPhoto() =>
        DemoCatalogue.PhotoFiles.Select(f => Path.Combine(PhotosPath, f)).FirstOrDefault(p => !File.Exists(p));

    public async Task SeedAsync(TextWriter output, CancellationToken cancellationToken)
    {
        var marker = Member.Normalize(DemoCatalogue.Members[0].Email);
        if (await db.Members.AnyAsync(m => m.NormalizedEmail == marker, cancellationToken))
        {
            output.WriteLine("Demo data already exists. Run seed --reset for a fresh demo.");
            return;
        }

        var start = clock.GetUtcNow();
        try
        {
            clock.Set(start - MembersJoinedBefore);
            foreach (var member in DemoCatalogue.Members)
            {
                await AddMemberAsync(member, cancellationToken);
            }
        }
        finally
        {
            clock.Release();
        }

        output.WriteLine($"Seeded {DemoCatalogue.Members.Count} members and {DemoCatalogue.Listings.Count} listings.");
    }

    /// <summary>Registers the member, verifies them with the link from their queued email, then suppresses that email.</summary>
    private async Task AddMemberAsync(DemoMember member, CancellationToken cancellationToken)
    {
        var memberId = Expect(
            await sender.Send(new RegisterMemberCommand(member.DisplayName, member.Email, DemoCatalogue.Password, AgeConfirmed: true, TermsAccepted: true), cancellationToken),
            $"Registering {member.Email}");
        var email = await db.OutboxMessages.SingleAsync(
            m => m.RecipientMemberId == memberId && m.NotificationType == NotificationType.EmailVerification && m.Status == OutboxMessageStatus.Pending,
            cancellationToken);
        Expect(await sender.Send(new VerifyEmailCommand(TokenFrom(email.Payload)), cancellationToken), $"Verifying {member.Email}");

        var now = clock.GetUtcNow().UtcDateTime;
        email.Claim(now);
        email.Suppress(SuppressionReason);
        await db.SaveChangesAsync(cancellationToken);
    }

    /// <summary>The raw token in the verification link of an EmailVerificationEmail payload.</summary>
    private static string TokenFrom(string payload)
    {
        using var json = JsonDocument.Parse(payload);
        var link = new Uri(json.RootElement.GetProperty("link").GetString()!);
        return HttpUtility.ParseQueryString(link.Query)["token"]
            ?? throw new InvalidOperationException("The verification email has no token.");
    }

    /// <summary>The value of a successful result; a refused command stops the seed with its code.</summary>
    private static T Expect<T>(Result<T> result, string step) =>
        result.IsSuccess ? result.Value! : throw new InvalidOperationException($"{step}: {result.Error!.Code} {result.Error.Title}");
}
