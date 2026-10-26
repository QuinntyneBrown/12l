using MediatR;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.AspNetCore.TestHost;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using Microsoft.Extensions.Time.Testing;
using TwelveL.Application.Abstractions;
using TwelveL.Application.Orders;
using TwelveL.Infrastructure.Persistence;

namespace TwelveL.Api.Tests.Support;

/// <summary>
/// Hosts TwelveL.Api in memory with SQLite in-memory in place of SQL Server, a captured email
/// sender, in-memory photo storage, a fake payment provider, a fake carrier tracking service and a controllable clock. No real database or external system is touched (AGENTS.md).
/// </summary>
public sealed class TwelveLApiFactory : WebApplicationFactory<Program>
{
    private readonly SqliteConnection _connection;
    private readonly string? _sharedDatabase;

    /// <summary>
    /// One in-memory database on one connection. With <paramref name="concurrent"/>, every
    /// DbContext opens its own connection to a shared-cache in-memory database instead, so
    /// parallel requests run in parallel as they would against SQL Server.
    /// </summary>
    public TwelveLApiFactory(bool concurrent = false)
    {
        _sharedDatabase = concurrent ? $"Data Source=file:twelvel-{Guid.NewGuid():N}?mode=memory&cache=shared" : null;
        _connection = new SqliteConnection(_sharedDatabase ?? "DataSource=:memory:");
        _connection.Open();
    }

    /// <summary>Starts at the real time, because the cookie container expires cookies by the real clock.</summary>
    public FakeTimeProvider Clock { get; } = new(DateTimeOffset.UtcNow);

    public CapturingEmailSender Email { get; } = new();

    public FakePhotoStorage Photos { get; } = new();

    public FakePaymentProvider Payments { get; } = new();

    public FakeCarrierTracking Carriers { get; } = new();

    public RecordingOrderCompleted Completed { get; } = new();

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.UseEnvironment("Testing");
        builder.UseSetting("Auth:SigningKey", "test-signing-key-that-is-at-least-32-bytes-long");
        builder.UseSetting("App:BaseUrl", "https://12l.test");
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<DbContextOptions<TwelveLDbContext>>();
            services.RemoveAll<IDbContextOptionsConfiguration<TwelveLDbContext>>();
            services.AddDbContext<TwelveLDbContext>(options =>
            {
                if (_sharedDatabase is null)
                {
                    options.UseSqlite(_connection);
                }
                else
                {
                    options.UseSqlite(_sharedDatabase);
                }
            });
            services.RemoveAll<TimeProvider>();
            services.AddSingleton<TimeProvider>(Clock);
            services.RemoveAll<IEmailSender>();
            services.AddSingleton<IEmailSender>(Email);
            services.RemoveAll<IPhotoStorage>();
            services.AddSingleton<IPhotoStorage>(Photos);
            services.RemoveAll<IPaymentProvider>();
            services.AddSingleton<IPaymentProvider>(Payments);
            services.RemoveAll<ICarrierTracking>();
            services.AddSingleton<ICarrierTracking>(Carriers);
            services.AddSingleton<INotificationHandler<OrderCompleted>>(Completed);
        });
    }

    /// <summary>Creates the schema once the host is built.</summary>
    public void EnsureDatabase()
    {
        using var scope = Services.CreateScope();
        scope.ServiceProvider.GetRequiredService<TwelveLDbContext>().Database.EnsureCreated();
    }

    /// <summary>An HTTPS client that keeps cookies, so Secure session cookies round-trip.</summary>
    public HttpClient CreateMemberClient()
    {
        EnsureDatabase();
        return CreateClient(new WebApplicationFactoryClientOptions { BaseAddress = new Uri("https://localhost") });
    }

    public void InDatabase(Action<TwelveLDbContext> action)
    {
        using var scope = Services.CreateScope();
        action(scope.ServiceProvider.GetRequiredService<TwelveLDbContext>());
    }

    protected override void Dispose(bool disposing)
    {
        base.Dispose(disposing);
        if (disposing)
        {
            _connection.Dispose();
        }
    }
}
