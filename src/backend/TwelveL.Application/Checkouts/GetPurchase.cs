using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using TwelveL.Application.Abstractions;
using TwelveL.Application.Catalog;
using TwelveL.Application.Common;
using TwelveL.Application.Listings;
using TwelveL.Domain.Listings;

namespace TwelveL.Application.Checkouts;

/// <summary>
/// One order as its buyer's confirmation page shows it: reference, item, the amount paid with the
/// card brand and last four digits, and the seller's display name. order-history extends it.
/// </summary>
public sealed record PurchaseDto(
    Guid Id,
    string Reference,
    string Status,
    CheckoutItemDto Item,
    string Total,
    string? CardBrand,
    string? CardLast4,
    string SellerDisplayName,
    DateTime PaidAt);

public sealed record GetPurchaseQuery(Guid BuyerId, Guid OrderId) : IRequest<Result<PurchaseDto>>;

public sealed class GetPurchaseQueryHandler(ITwelveLDbContext db, IOptions<PhotoOptions> photoOptions) :
    IRequestHandler<GetPurchaseQuery, Result<PurchaseDto>>
{
    public async Task<Result<PurchaseDto>> Handle(GetPurchaseQuery query, CancellationToken cancellationToken)
    {
        var order = await db.Orders.AsNoTracking().SingleOrDefaultAsync(o => o.Id == query.OrderId && o.BuyerId == query.BuyerId, cancellationToken);
        if (order is null)
        {
            return Error.NotFound("ORDER_NOT_FOUND");
        }

        var listing = await db.Listings.AsNoTracking().SingleAsync(l => l.Id == order.ListingId, cancellationToken);
        var payment = await db.Payments.AsNoTracking().SingleAsync(p => p.Id == order.PaymentId, cancellationToken);
        var seller = await db.Members.AsNoTracking().Where(m => m.Id == order.SellerId).Select(m => m.DisplayName).SingleAsync(cancellationToken);
        var cover = await db.ListingPhotos.AsNoTracking()
            .Where(p => p.ListingId == listing.Id).OrderBy(p => p.Position)
            .FirstOrDefaultAsync(cancellationToken);
        var photo = cover is null ? null : CatalogPhotos.ToDto(cover, string.Empty, photoOptions.Value.PublicBaseUrl.TrimEnd('/'));
        return new PurchaseDto(
            order.Id,
            order.Reference,
            order.Status.ToString(),
            new CheckoutItemDto(listing.Reference, listing.Title ?? string.Empty, listing.Brand ?? string.Empty, listing.Size, listing.Condition?.ToLabel() ?? string.Empty, photo),
            CheckoutMoney.Format(order.Total),
            payment.CardBrand,
            payment.CardLast4,
            seller,
            order.PaidAt);
    }
}
