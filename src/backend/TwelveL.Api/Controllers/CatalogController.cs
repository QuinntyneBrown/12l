using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TwelveL.Api.Auth;
using TwelveL.Api.Http;
using TwelveL.Application.Catalog;

namespace TwelveL.Api.Controllers;

/// <summary>The public catalog: anyone may browse it, signed in or not (L2-022).</summary>
[ApiController]
[AllowAnonymous]
public sealed class CatalogController(ISender sender) : ControllerBase
{
    [HttpGet("api/catalog/listings")]
    public async Task<IActionResult> Listings(int page = 1, int? pageSize = null, string? category = null, CancellationToken cancellationToken = default)
    {
        Response.Headers.CacheControl = "no-store";
        var result = await sender.Send(new BrowseCatalogQuery(page, pageSize, category), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }

    /// <summary>
    /// One listing (L2-025). The session cookie is read when present so the seller is recognised;
    /// a missing or expired one means a visitor, never 401. The body depends on the viewer.
    /// </summary>
    [HttpGet("api/catalog/listings/{reference}")]
    public async Task<IActionResult> Listing(string reference, CancellationToken cancellationToken)
    {
        Response.Headers.CacheControl = "private, no-store";
        Guid? viewerId = User.Identity?.IsAuthenticated == true ? User.MemberId() : null;
        var result = await sender.Send(new GetListingDetailQuery(reference, viewerId), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }
}
