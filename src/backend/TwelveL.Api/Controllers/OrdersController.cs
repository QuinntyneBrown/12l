using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using TwelveL.Api.Auth;
using TwelveL.Api.Http;
using TwelveL.Application.Orders;

namespace TwelveL.Api.Controllers;

/// <summary>
/// Order actions (L2-032, L2-033, L2-034): the seller reads the sale and adds tracking; the buyer
/// confirms receipt. 401 for visitors, 404 for anyone but the order's seller or buyer, 409
/// ORDER_INVALID_TRANSITION when the order's status does not allow the action.
/// </summary>
[ApiController]
[Authorize(Policy = Policies.VerifiedMember)]
public sealed class OrdersController(ISender sender) : ControllerBase
{
    [HttpGet("api/sales/{id:guid}")]
    public async Task<IActionResult> Sale(Guid id, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new GetSaleQuery(User.MemberId(), id), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }

    [HttpPost("api/orders/{id:guid}/shipment")]
    public async Task<IActionResult> AddTracking(Guid id, AddTrackingRequest request, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new AddTrackingCommand(User.MemberId(), id, request.Carrier, request.TrackingNumber), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }

    [HttpPost("api/orders/{id:guid}/receipt")]
    public async Task<IActionResult> ConfirmReceipt(Guid id, CancellationToken cancellationToken)
    {
        var result = await sender.Send(new ConfirmReceiptCommand(User.MemberId(), id), cancellationToken);
        return result.IsSuccess ? Ok(result.Value) : this.ToProblem(result.Error!);
    }
}

public sealed record AddTrackingRequest(string? Carrier, string? TrackingNumber);
