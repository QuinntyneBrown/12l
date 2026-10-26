using System.Globalization;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using TwelveL.Application.Abstractions;
using TwelveL.Application.Common;
using TwelveL.Application.Listings;
using TwelveL.Domain.Listings;

namespace TwelveL.Application.Catalog;

/// <summary>Paging settings of the catalog (L2-022).</summary>
public sealed class CatalogOptions
{
    public int DefaultPageSize { get; set; } = 24;

    public int MaxPageSize { get; set; } = 48;
}

/// <summary>
/// The cover photo of a card (L2-059): srcset strings of the 400, 800 and 1600 px versions in
/// WebP and JPEG, the 400 px JPEG as src, and the original dimensions for width and height.
/// </summary>
public sealed record CardPhotoDto(int Width, int Height, string Alt, string Src, string Webp, string Jpeg);

/// <summary>One catalog card. Price is a two-place decimal string, so no float crosses the wire (L2-018).</summary>
public sealed record ListingCardDto(
    Guid Id,
    string Reference,
    string Title,
    string Brand,
    string Category,
    string? Subcategory,
    string SizeLabel,
    string Condition,
    string Price,
    string Status,
    DateTime PublishedAt,
    CardPhotoDto? CoverPhoto);

public sealed record CatalogPageDto(IReadOnlyList<ListingCardDto> Items, int Page, int PageSize, int TotalCount);

/// <summary>A page of the catalog, optionally narrowed to one category. Null page size means the default.</summary>
public sealed record BrowseCatalogQuery(int Page, int? PageSize, string? Category) : IRequest<Result<CatalogPageDto>>;

/// <summary>
/// Reads Active and Reserved listings only (<see cref="CatalogVisibility"/>), newest first, with
/// the cover photo at position 0. A page size above the maximum is capped, not refused.
/// </summary>
public sealed class BrowseCatalogQueryHandler(ITwelveLDbContext db, IOptions<CatalogOptions> options, IOptions<PhotoOptions> photoOptions) :
    IRequestHandler<BrowseCatalogQuery, Result<CatalogPageDto>>
{
    public async Task<Result<CatalogPageDto>> Handle(BrowseCatalogQuery query, CancellationToken cancellationToken)
    {
        var settings = options.Value;
        if (query.Page < 1 || query.PageSize < 1)
        {
            return Invalid("Page and page size must be 1 or more");
        }

        if (query.Category is not null && CategoryCatalog.Find(query.Category) is null)
        {
            return Invalid("Choose one of the 4 categories");
        }

        var pageSize = Math.Min(query.PageSize ?? settings.DefaultPageSize, settings.MaxPageSize);
        var visible = db.Listings.AsNoTracking().Where(CatalogVisibility.IsVisible);
        if (query.Category is { } category)
        {
            visible = visible.Where(l => l.Category == category);
        }

        var total = await visible.CountAsync(cancellationToken);
        var listings = await visible
            .OrderByDescending(l => l.PublishedAt).ThenByDescending(l => l.Id)
            .Skip((query.Page - 1) * pageSize).Take(pageSize)
            .ToListAsync(cancellationToken);
        var ids = listings.Select(l => l.Id).ToList();
        var covers = await db.ListingPhotos.AsNoTracking()
            .Where(p => p.ListingId != null && ids.Contains(p.ListingId.Value) && p.Position == 0)
            .ToDictionaryAsync(p => p.ListingId!.Value, cancellationToken);
        var baseUrl = photoOptions.Value.PublicBaseUrl.TrimEnd('/');
        var items = listings.Select(l => ToCard(l, covers.GetValueOrDefault(l.Id), baseUrl)).ToList();
        return new CatalogPageDto(items, query.Page, pageSize, total);
    }

    private static ListingCardDto ToCard(Listing listing, ListingPhoto? cover, string baseUrl) => new(
        listing.Id,
        listing.Reference,
        listing.Title ?? string.Empty,
        listing.Brand ?? string.Empty,
        listing.Category,
        listing.Subcategory,
        CategoryCatalog.Find(listing.Category)?.SizeLabel ?? listing.Size,
        listing.Condition?.ToLabel() ?? string.Empty,
        (listing.Price ?? 0m).ToString("0.00", CultureInfo.InvariantCulture),
        listing.Status.ToString(),
        listing.PublishedAt ?? listing.CreatedAt,
        cover is null ? null : CatalogPhotos.ToDto(cover, $"Photo 1 of {listing.Brand} {listing.Title}", baseUrl));

    private static Error Invalid(string title) => new(400, "VALIDATION_FAILED", title);
}

/// <summary>Maps a stored photo to the srcset strings the frontend renders (L2-059).</summary>
public static class CatalogPhotos
{
    public static CardPhotoDto ToDto(ListingPhoto photo, string alt, string baseUrl)
    {
        string SrcSet(PhotoFormat format) => string.Join(", ", photo.Versions
            .Where(v => v.Format == format).OrderBy(v => v.Size)
            .Select(v => $"{baseUrl}/{v.Key} {v.Width}w"));
        var smallest = photo.Versions.Where(v => v.Format == PhotoFormat.Jpeg).OrderBy(v => v.Size).FirstOrDefault();
        return new CardPhotoDto(photo.Width, photo.Height, alt, smallest is null ? string.Empty : $"{baseUrl}/{smallest.Key}", SrcSet(PhotoFormat.WebP), SrcSet(PhotoFormat.Jpeg));
    }
}
