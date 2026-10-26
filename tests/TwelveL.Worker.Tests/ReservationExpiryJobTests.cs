// Unit Test
// Traces to: L2-028
// Description: Each pass of the reservation expiry job sends one ExpireReservationsCommand in its own scope.

using MediatR;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.Extensions.Options;
using TwelveL.Application.Checkouts;
using TwelveL.Worker;

namespace TwelveL.Worker.Tests;

public sealed class ReservationExpiryJobTests
{
    [Fact]
    public async Task A_pass_sends_the_expire_command_and_returns_how_many_ended()
    {
        var sender = new RecordingSender(expired: 3);
        using var services = new ServiceCollection().AddScoped<ISender>(_ => sender).BuildServiceProvider();
        var job = new ReservationExpiryJob(
            services.GetRequiredService<IServiceScopeFactory>(),
            Options.Create(new CheckoutJobOptions()),
            NullLogger<ReservationExpiryJob>.Instance);

        var expired = await job.RunOnceAsync(CancellationToken.None);

        Assert.Equal(3, expired);
        Assert.IsType<ExpireReservationsCommand>(Assert.Single(sender.Sent));
    }

    [Fact]
    public void The_job_runs_well_inside_the_10_minute_reservation()
    {
        Assert.True(new CheckoutJobOptions().ExpiryJobInterval <= TimeSpan.FromSeconds(30));
    }

    private sealed class RecordingSender(int expired) : ISender
    {
        public List<object> Sent { get; } = [];

        public Task<TResponse> Send<TResponse>(IRequest<TResponse> request, CancellationToken cancellationToken = default)
        {
            Sent.Add(request);
            return Task.FromResult((TResponse)(object)expired);
        }

        public Task Send<TRequest>(TRequest request, CancellationToken cancellationToken = default)
            where TRequest : IRequest => throw new NotSupportedException();

        public Task<object?> Send(object request, CancellationToken cancellationToken = default) => throw new NotSupportedException();

        public IAsyncEnumerable<TResponse> CreateStream<TResponse>(IStreamRequest<TResponse> request, CancellationToken cancellationToken = default) =>
            throw new NotSupportedException();

        public IAsyncEnumerable<object?> CreateStream(object request, CancellationToken cancellationToken = default) => throw new NotSupportedException();
    }
}
