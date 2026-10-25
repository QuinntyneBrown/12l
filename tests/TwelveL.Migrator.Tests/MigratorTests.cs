namespace TwelveL.Migrator.Tests;

public sealed class MigratorTests
{
    [Fact]
    public void Run_reports_no_migrations_and_succeeds()
    {
        using var output = new StringWriter();

        var exitCode = TwelveL.Migrator.MigratorApp.Run(output);

        Assert.Equal(0, exitCode);
        Assert.Contains("No migrations", output.ToString());
    }
}
