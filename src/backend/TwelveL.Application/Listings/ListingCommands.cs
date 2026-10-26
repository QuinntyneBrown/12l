using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using TwelveL.Application.Abstractions;
using TwelveL.Application.Common;
using TwelveL.Domain.Listings;

namespace TwelveL.Application.Listings;

/// <summary>The seller's own view of a listing, returned by every listings command.</summary>
public sealed record MyListingDto(
    string Reference,
    string Status,
    string Category,
    string? Subcategory,
    string Size,
    string? Title,
    string? Description,
    string? Brand,
    string? Condition,
    string? Flaws,
    decimal? Price,
    decimal? ShippingCost,
    DateTime CreatedAt,
    DateTime UpdatedAt,
    DateTime? PublishedAt)
{
    public static MyListingDto From(Listing l) => new(
        l.Reference, l.Status.ToString(), l.Category, l.Subcategory, l.Size, l.Title, l.Description, l.Brand,
        l.Condition?.ToLabel(), l.Flaws, l.Price, l.ShippingCost, l.CreatedAt, l.UpdatedAt, l.PublishedAt);
}

public sealed record PublishListingResult(string Reference, string Status, bool PayoutOnboardingRequired);

/// <summary>Creates a draft; only an accepted category is required (L2-019). The size comes from the category (L2-013).</summary>
public sealed record CreateListingDraftCommand(Guid SellerId, ListingDetails Details) : IRequest<Result<MyListingDto>>;

/// <summary>Replaces the fields of the caller's draft. Editing an active listing belongs to edit-and-withdraw-listing.</summary>
public sealed record UpdateListingDraftCommand(Guid SellerId, string Reference, ListingDetails Details) : IRequest<Result<MyListingDto>>;

/// <summary>Publishes the caller's draft under the L2-014 to L2-018 rules and the daily limit of L2-051.</summary>
public sealed record PublishListingCommand(Guid SellerId, string Reference, bool SizeConfirmed) : IRequest<Result<PublishListingResult>>;

public sealed record GetMyListingQuery(Guid SellerId, string Reference) : IRequest<Result<MyListingDto>>;

public sealed class ListingCommandHandlers(
    ITwelveLDbContext db,
    ISellerPayoutAccountReader payouts,
    IOptions<SellingOptions> options,
    TimeProvider clock) :
    IRequestHandler<CreateListingDraftCommand, Result<MyListingDto>>,
    IRequestHandler<UpdateListingDraftCommand, Result<MyListingDto>>,
    IRequestHandler<PublishListingCommand, Result<PublishListingResult>>,
    IRequestHandler<GetMyListingQuery, Result<MyListingDto>>
{
    /// <summary>First listing number; references start at L-10001.</summary>
    public const long FirstNumber = 10001;

    public async Task<Result<MyListingDto>> Handle(CreateListingDraftCommand command, CancellationToken cancellationToken)
    {
        if (ToError(Listing.CheckDraft(command.Details)) is { } error)
        {
            return error;
        }

        var now = clock.GetUtcNow().UtcDateTime;
        var last = await db.Listings.MaxAsync(l => (long?)l.Number, cancellationToken);
        var listing = Listing.CreateDraft(command.SellerId, (last ?? FirstNumber - 1) + 1, command.Details, now);
        db.Listings.Add(listing);
        await db.SaveChangesAsync(cancellationToken);
        return MyListingDto.From(listing);
    }

    public async Task<Result<MyListingDto>> Handle(UpdateListingDraftCommand command, CancellationToken cancellationToken)
    {
        var listing = await FindOwnAsync(command.SellerId, command.Reference, cancellationToken);
        if (listing is null)
        {
            return Error.NotFound("LISTING_NOT_FOUND");
        }

        if (listing.Status != ListingStatus.Draft)
        {
            return NotDraft;
        }

        if (ToError(Listing.CheckDraft(command.Details)) is { } error)
        {
            return error;
        }

        listing.UpdateDetails(command.Details, clock.GetUtcNow().UtcDateTime);
        await db.SaveChangesAsync(cancellationToken);
        return MyListingDto.From(listing);
    }

    public async Task<Result<PublishListingResult>> Handle(PublishListingCommand command, CancellationToken cancellationToken)
    {
        var listing = await FindOwnAsync(command.SellerId, command.Reference, cancellationToken);
        if (listing is null)
        {
            return Error.NotFound("LISTING_NOT_FOUND");
        }

        if (listing.Status != ListingStatus.Draft)
        {
            return NotDraft;
        }

        var now = clock.GetUtcNow().UtcDateTime;
        var dayStart = now.Date;
        var publishedToday = await db.Listings.CountAsync(
            l => l.SellerId == command.SellerId && l.PublishedAt >= dayStart, cancellationToken);
        if (publishedToday >= options.Value.PublishesPerDay)
        {
            return Error.TooManyRequests(dayStart.AddDays(1) - now, $"That's {options.Value.PublishesPerDay} listings today");
        }

        if (ToError(listing.Publish(command.SizeConfirmed, now)) is { } error)
        {
            return error;
        }

        await db.SaveChangesAsync(cancellationToken);
        var onboarded = await payouts.IsOnboardedAsync(command.SellerId, cancellationToken);
        return new PublishListingResult(listing.Reference, listing.Status.ToString(), !onboarded);
    }

    public async Task<Result<MyListingDto>> Handle(GetMyListingQuery query, CancellationToken cancellationToken)
    {
        var listing = await FindOwnAsync(query.SellerId, query.Reference, cancellationToken);
        return listing is null ? Error.NotFound("LISTING_NOT_FOUND") : MyListingDto.From(listing);
    }

    private static readonly Error NotDraft = new(409, "LISTING_NOT_DRAFT", "This listing is not a draft");

    /// <summary>Another member's listing answers as missing so its existence is not revealed (L2-010).</summary>
    private Task<Listing?> FindOwnAsync(Guid sellerId, string reference, CancellationToken cancellationToken) =>
        db.Listings.SingleOrDefaultAsync(l => l.Reference == reference && l.SellerId == sellerId, cancellationToken);

    /// <summary>
    /// Maps rule violations to a 422. The top-level code is CATEGORY_INVALID or SIZE_NOT_ACCEPTED
    /// when those rules fail, the field's own code when only one field fails, else LISTING_INVALID.
    /// </summary>
    private static Error? ToError(IReadOnlyList<RuleViolation> violations)
    {
        if (violations.Count == 0)
        {
            return null;
        }

        var errors = violations.ToDictionary(v => v.Field, v => new FieldError(v.Code, v.Message));
        var code = violations.Any(v => v.Code == "CATEGORY_INVALID") ? "CATEGORY_INVALID"
            : violations.Any(v => v.Code == "SIZE_NOT_ACCEPTED") ? "SIZE_NOT_ACCEPTED"
            : violations.Count == 1 ? violations[0].Code
            : "LISTING_INVALID";
        return Error.Invalid(code, errors);
    }
}
