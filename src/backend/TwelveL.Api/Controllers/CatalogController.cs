using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
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
}
