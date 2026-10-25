namespace TwelveL.Worker.Tests;

public sealed class AssemblyTests
{
    [Fact]
    public void Worker_type_belongs_to_the_worker_assembly()
    {
        Assert.Equal("TwelveL.Worker", typeof(TwelveL.Worker.Worker).Assembly.GetName().Name);
    }
}
