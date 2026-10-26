# Builds the three backend services from one restore. Build context: src/backend.
#   docker build -f ../../deploy/backend.Dockerfile --target api .
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY Directory.Build.props global.json TwelveL.sln ./
COPY TwelveL.Domain/TwelveL.Domain.csproj TwelveL.Domain/
COPY TwelveL.Application/TwelveL.Application.csproj TwelveL.Application/
COPY TwelveL.Infrastructure/TwelveL.Infrastructure.csproj TwelveL.Infrastructure/
COPY TwelveL.Api/TwelveL.Api.csproj TwelveL.Api/
COPY TwelveL.Worker/TwelveL.Worker.csproj TwelveL.Worker/
COPY TwelveL.Migrator/TwelveL.Migrator.csproj TwelveL.Migrator/
RUN dotnet restore TwelveL.Api/TwelveL.Api.csproj \
 && dotnet restore TwelveL.Worker/TwelveL.Worker.csproj \
 && dotnet restore TwelveL.Migrator/TwelveL.Migrator.csproj
COPY . .
RUN dotnet publish TwelveL.Api/TwelveL.Api.csproj -c Release --no-restore -o /out/api \
 && dotnet publish TwelveL.Worker/TwelveL.Worker.csproj -c Release --no-restore -o /out/worker \
 && dotnet publish TwelveL.Migrator/TwelveL.Migrator.csproj -c Release --no-restore -o /out/migrator

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS api
WORKDIR /app
COPY --from=build /out/api .
RUN mkdir -p /data/photos && chown app:app /data/photos
ENV ASPNETCORE_URLS=http://+:8080 DOTNET_ENVIRONMENT=Production
EXPOSE 8080
USER app
ENTRYPOINT ["dotnet", "TwelveL.Api.dll"]

FROM mcr.microsoft.com/dotnet/runtime:10.0 AS worker
WORKDIR /app
COPY --from=build /out/worker .
RUN mkdir -p /data/photos && chown app:app /data/photos
ENV DOTNET_ENVIRONMENT=Production
USER app
ENTRYPOINT ["dotnet", "TwelveL.Worker.dll"]

FROM mcr.microsoft.com/dotnet/runtime:10.0 AS migrator
WORKDIR /app
COPY --from=build /out/migrator .
USER app
ENTRYPOINT ["dotnet", "TwelveL.Migrator.dll"]
