namespace TwelveL.Worker;

/// <summary>Host for background jobs. No job exists until the first feature needs one.</summary>
public sealed class Worker : BackgroundService
{
    protected override Task ExecuteAsync(CancellationToken stoppingToken) => Task.CompletedTask;
}
