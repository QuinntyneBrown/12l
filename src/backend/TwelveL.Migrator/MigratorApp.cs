namespace TwelveL.Migrator;

/// <summary>Applies EF Core migrations. No migrations exist until the first entity is added.</summary>
public static class MigratorApp
{
    public static int Run(TextWriter output)
    {
        output.WriteLine("No migrations to apply.");
        return 0;
    }
}
