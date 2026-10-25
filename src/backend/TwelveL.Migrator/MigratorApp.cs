using Microsoft.EntityFrameworkCore;
using TwelveL.Infrastructure.Persistence;

namespace TwelveL.Migrator;

/// <summary>Applies the EF Core migrations of TwelveL.Infrastructure to 12L database.</summary>
public static class MigratorApp
{
    public const string ConnectionStringVariable = "ConnectionStrings__TwelveL";

    /// <summary>
    /// Applies pending migrations when a connection string is given. Without one it lists the
    /// migrations in this build, connects to nothing and fails, so a misconfigured deploy stops.
    /// </summary>
    public static int Run(TextWriter output, string? connectionString)
    {
        var options = new DbContextOptionsBuilder<TwelveLDbContext>()
            .UseSqlServer(string.IsNullOrWhiteSpace(connectionString) ? "Server=unset" : connectionString)
            .Options;
        using var db = new TwelveLDbContext(options);
        if (string.IsNullOrWhiteSpace(connectionString))
        {
            output.WriteLine($"Set {ConnectionStringVariable} to apply these migrations:");
            foreach (var migration in db.Database.GetMigrations())
            {
                output.WriteLine($"  {migration}");
            }

            return 2;
        }

        db.Database.Migrate();
        output.WriteLine("Migrations applied.");
        return 0;
    }
}
