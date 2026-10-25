using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TwelveL.Application.Abstractions;
using TwelveL.Infrastructure.Accounts;
using TwelveL.Infrastructure.Email;
using TwelveL.Infrastructure.Persistence;

namespace TwelveL.Infrastructure;

public static class DependencyInjection
{
    /// <summary>Registers 12L database and the adapters behind the application ports.</summary>
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<TwelveLDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("TwelveL")));
        services.AddScoped<ITwelveLDbContext>(sp => sp.GetRequiredService<TwelveLDbContext>());
        services.AddSingleton(TimeProvider.System);
        services.AddSingleton<IPasswordHasher, IdentityPasswordHasher>();
        services.AddSingleton<IBreachedPasswords, BundledBreachedPasswords>();
        services.AddSingleton<IEmailSender, LoggingEmailSender>();
        services.Configure<AppOptions>(configuration.GetSection("App"));
        return services;
    }
}
