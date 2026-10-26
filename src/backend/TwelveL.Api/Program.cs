using TwelveL.Api.Auth;
using TwelveL.Api.Privacy;
using TwelveL.Application;
using TwelveL.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddTwelveLAuth(builder.Configuration);
builder.Services.Configure<StrictlyNecessaryCookieOptions>(builder.Configuration.GetSection(StrictlyNecessaryCookieOptions.Section));

var app = builder.Build();

app.UseMiddleware<CookieAllowListMiddleware>();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();

/// <summary>Entry point, exposed to WebApplicationFactory in TwelveL.Api.Tests.</summary>
public partial class Program;
