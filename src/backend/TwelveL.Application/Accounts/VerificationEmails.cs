using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using TwelveL.Application.Abstractions;
using TwelveL.Domain.Members;

namespace TwelveL.Application.Accounts;

/// <summary>Issues a verification link, revoking every earlier link of the member (L2-002 AC5).</summary>
public sealed class VerificationEmails(ITwelveLDbContext db, IEmailSender email, IOptions<AppOptions> app, TimeProvider clock)
{
    public async Task SendAsync(Member member, CancellationToken cancellationToken)
    {
        var now = clock.GetUtcNow().UtcDateTime;
        var earlier = await db.EmailVerificationTokens
            .Where(t => t.MemberId == member.Id && t.UsedAt == null && t.RevokedAt == null)
            .ToListAsync(cancellationToken);
        earlier.ForEach(t => t.Revoke(now));

        var token = SecureTokens.Create();
        db.EmailVerificationTokens.Add(EmailVerificationToken.Issue(member.Id, SecureTokens.Hash(token), now));
        await db.SaveChangesAsync(cancellationToken);

        var link = $"{app.Value.BaseUrl.TrimEnd('/')}/verify?token={Uri.EscapeDataString(token)}";
        await email.SendAsync(
            new EmailMessage(
                member.Email,
                "Verify your email for 12L",
                $"Hi {member.DisplayName},\n\nOpen this link to verify your email and start buying and selling:\n{link}\n\nThe link works for 24 hours."),
            cancellationToken);
    }
}
