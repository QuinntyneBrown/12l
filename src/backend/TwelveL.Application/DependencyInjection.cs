using Microsoft.Extensions.DependencyInjection;
using TwelveL.Application.Accounts;

namespace TwelveL.Application;

public static class DependencyInjection
{
    /// <summary>Registers the MediatR handlers and application services.</summary>
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(config => config.RegisterServicesFromAssemblyContaining(typeof(DependencyInjection)));
        services.AddScoped<VerificationEmails>();
        services.AddScoped<Notifications.IEmailOutbox, Notifications.EmailOutbox>();
        services.AddScoped<Listings.ListingPhotoAttacher>();
        return services;
    }
}
