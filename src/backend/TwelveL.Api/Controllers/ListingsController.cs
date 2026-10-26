using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TwelveL.Api.Auth;
using TwelveL.Api.Http;
using TwelveL.Application.Listings;
using TwelveL.Domain.Listings;

namespace TwelveL.Api.Controllers;

/// <summary>
/// Create, change and publish the caller's listings. Every action needs a verified member
/// (CanSell, L2-003, L2-010): 401 for visitors, 403 EMAIL_NOT_VERIFIED for unverified members.
/// </summary>
[ApiController]
[Authorize(Policy = Policies.CanSell)]
public sealed class ListingsController(ISender sender) : ControllerBase
{
    [HttpPost("api/listings")]
    public async Task<IActionResult> Create(ListingDetailsRequest request, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new CreateListingDraftCommand(User.MemberId(), request.ToDetails(), request.PhotoIds), cancellationToken);
        return result.IsSuccess
            ? Created($"/api/me/listings/{result.Value!.Reference}", result.Value)
            : this.ToProblem(result.Error!);
    }

    [HttpPut("api/listings/{reference}")]
    public async Task<IActionResult> Update(string reference, ListingDetailsRequest request, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new UpdateListingDraftCommand(User.MemberId(), reference, request.ToDetails(), request.PhotoIds), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }

    [HttpPost("api/listings/{reference}/publish")]
    public async Task<IActionResult> Publish(string reference, PublishRequest request, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new PublishListingCommand(User.MemberId(), reference, request.SizeConfirmed), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }

    [HttpPost("api/listings/{reference}/relist")]
    public async Task<IActionResult> Relist(string reference, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new RelistListingCommand(User.MemberId(), reference), cancellationToken);
        return result.IsSuccess ? NoContent() : this.ToProblem(result.Error!);
    }

    [HttpGet("api/me/listings/{reference}")]
    public async Task<IActionResult> GetMine(string reference, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new GetMyListingQuery(User.MemberId(), reference), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }
}

/// <summary>
/// The editable fields. There is no seller, status, confirmation time or timestamp member, so a
/// client cannot set them (mass assignment, L2-049); unknown members are ignored. PhotoIds lists
/// uploaded photos in display order (L2-017); leaving it out keeps the current photos.
/// </summary>
public sealed record ListingDetailsRequest(
    string? Category,
    string? Subcategory,
    string? Size,
    string? Title,
    string? Description,
    string? Brand,
    string? Condition,
    string? Flaws,
    decimal? Price,
    decimal? ShippingCost,
    IReadOnlyList<Guid>? PhotoIds = null)
{
    public ListingDetails ToDetails() => new(Category, Subcategory, Size, Title, Description, Brand, Condition, Flaws, Price, ShippingCost);
}

public sealed record PublishRequest(bool SizeConfirmed);
