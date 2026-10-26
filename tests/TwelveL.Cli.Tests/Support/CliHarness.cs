using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;
using TwelveL.Application.Abstractions;
using TwelveL.Infrastructure.Persistence;

namespace TwelveL.Cli.Tests.Support;

/// <summary>
/// Runs TwelveL.Cli against one SQLite in-memory database kept open for the harness's life, a fake
/// photo store and <see cref="EnsureCreatedSchema"/>. No SQL Server, LocalDB or live connection
/// string is used (AGENTS.md). The SQL Server connection string it passes is only printed.
/// </summary>
public sealed class CliHarness : IDisposable
{
    /// <summary>Printed as the reset target; never opened.</summary>
    public const string ConnectionString = "Server=(localdb)\\MSSQLLocalDB;Database=TwelveLDemo;User ID=demo;Password=not-a-real-secret;TrustServerCertificate=True";

    private readonly SqliteConnection _connection = new("DataSource=:memory:");

    public CliHarness()
    {
        _connection.Open();
    }

    public FakePhotoStorage Photos { get; } = new();

    /// <summary>Extra settings for every run, such as Selling:PublishesPerDay.</summary>
    public Dictionary<string, string?> Settings { get; } = new();

    public Task<CliRun> RunAsync(string[] args, string environment = "Development", string? sqliteConnectionString = null) =>
        CliRun.RunAsync(args, ConnectionString, environment, Settings, services =>
        {
            services.RemoveAll<DbContextOptions<TwelveLDbContext>>();
            services.RemoveAll<IDbContextOptionsConfiguration<TwelveLDbContext>>();
            services.AddDbContext<TwelveLDbContext>(options =>
            {
                if (sqliteConnectionString is null)
                {
                    options.UseSqlite(_connection);
                }
                else
                {
                    options.UseSqlite(sqliteConnectionString);
                }
            });
            services.RemoveAll<IPhotoStorage>();
            services.AddSingleton<IPhotoStorage>(Photos);
            services.RemoveAll<IDatabaseSchema>();
            services.AddSingleton<IDatabaseSchema, EnsureCreatedSchema>();
        });

    /// <summary>Reads the database the runs wrote, through a fresh context.</summary>
    public T InDatabase<T>(Func<TwelveLDbContext, T> query)
    {
        using var db = new TwelveLDbContext(new DbContextOptionsBuilder<TwelveLDbContext>().UseSqlite(_connection).Options);
        return query(db);
    }

    public void Dispose() => _connection.Dispose();
}
