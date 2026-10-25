var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

var app = builder.Build();

app.MapControllers();

app.Run();

/// <summary>Entry point, exposed to WebApplicationFactory in TwelveL.Api.Tests.</summary>
public partial class Program;
