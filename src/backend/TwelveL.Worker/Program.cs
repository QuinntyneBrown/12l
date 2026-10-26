using TwelveL.Application;
using TwelveL.Infrastructure;
using TwelveL.Worker;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.Configure<CheckoutJobOptions>(builder.Configuration.GetSection("Checkout"));
builder.Services.AddHostedService<Worker>();
builder.Services.AddHostedService<ReservationExpiryJob>();

var host = builder.Build();
host.Run();
