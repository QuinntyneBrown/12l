using TwelveL.Api.Auth;
using TwelveL.Application;
using TwelveL.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddTwelveLAuth(builder.Configuration);

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();

/// <summary>Entry point, exposed to WebApplicationFactory in TwelveL.Api.Tests.</summary>
public partial class Program;
