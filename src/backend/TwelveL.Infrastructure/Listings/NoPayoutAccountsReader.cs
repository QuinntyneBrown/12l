using TwelveL.Application.Abstractions;

namespace TwelveL.Infrastructure.Listings;

/// <summary>
/// Until seller-payouts connects the payment provider, no seller has finished payout onboarding,
/// so every publish prompts for it (L2-031 AC1).
/// </summary>
internal sealed class NoPayoutAccountsReader : ISellerPayoutAccountReader
{
    public Task<bool> IsOnboardedAsync(Guid sellerId, CancellationToken cancellationToken) => Task.FromResult(false);
}
