using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace TwelveL.Infrastructure.Persistence;

/// <summary>Lets dotnet-ef build the model to add migrations. It never opens a connection.</summary>
internal sealed class DesignTimeDbContextFactory : IDesignTimeDbContextFactory<TwelveLDbContext>
{
    public TwelveLDbContext CreateDbContext(string[] args) =>
        new(new DbContextOptionsBuilder<TwelveLDbContext>().UseSqlServer("Server=design-time;Database=TwelveL").Options);
}
