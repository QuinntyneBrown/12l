using Microsoft.EntityFrameworkCore;
using TwelveL.Application.Abstractions;
using TwelveL.Domain.Listings;
using TwelveL.Domain.Members;

namespace TwelveL.Infrastructure.Persistence;

/// <summary>EF Core context over 12L database (SQL Server). LINQ only, so all SQL is parameterised (L2-049).</summary>
public sealed class TwelveLDbContext(DbContextOptions<TwelveLDbContext> options) : DbContext(options), ITwelveLDbContext
{
    public DbSet<Member> Members => Set<Member>();

    public DbSet<EmailVerificationToken> EmailVerificationTokens => Set<EmailVerificationToken>();

    public DbSet<Session> Sessions => Set<Session>();

    public DbSet<Listing> Listings => Set<Listing>();

    public DbSet<ListingPhoto> ListingPhotos => Set<ListingPhoto>();

    protected override void OnModelCreating(ModelBuilder modelBuilder) =>
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(TwelveLDbContext).Assembly);
}
