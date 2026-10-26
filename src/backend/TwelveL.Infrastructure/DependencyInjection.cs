using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TwelveL.Application.Abstractions;
using TwelveL.Application.Catalog;
using TwelveL.Application.Listings;
using TwelveL.Application.Notifications;
using TwelveL.Infrastructure.Accounts;
using TwelveL.Infrastructure.Carriers;
using TwelveL.Infrastructure.Email;
using TwelveL.Infrastructure.Payments;
using TwelveL.Infrastructure.Payouts;
using TwelveL.Infrastructure.Persistence;
using TwelveL.Infrastructure.Photos;

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
        services.AddScoped<ISellerPayoutAccountReader, PayoutAccountReader>();
        services.Configure<AppOptions>(configuration.GetSection("App"));
        services.Configure<NotificationOptions>(configuration.GetSection("Notifications"));
        services.Configure<SellingOptions>(configuration.GetSection("Selling"));
        services.Configure<PhotoOptions>(configuration.GetSection("Photos"));
        services.Configure<CatalogOptions>(configuration.GetSection("Catalog"));
        services.Configure<PhotoStorageOptions>(configuration.GetSection("PhotoStorage"));
        services.AddSingleton<IImageInspector, SkiaImageInspector>();
        services.AddSingleton<IListingPhotoProcessor, SkiaPhotoProcessor>();
        services.AddSingleton<IPhotoStorage, FileSystemPhotoStorage>();
        services.AddSingleton<IPaymentProvider, UnconfiguredPaymentProvider>();
        services.AddSingleton<ICarrierTracking, UnconfiguredCarrierTracking>();
        services.AddSingleton<IPayoutProvider, UnconfiguredPayoutProvider>();
        return services;
    }
}
