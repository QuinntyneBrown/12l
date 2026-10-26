# Deployment

12L runs in production on one small Azure Linux VM with Docker Compose, backed by an Azure SQL
Database. Every push to `main` deploys automatically.

## Topology

| Piece                  | Where                                   | Notes                                                                 |
| ---------------------- | --------------------------------------- | --------------------------------------------------------------------- |
| `web` (Caddy)          | VM, ports 80/443                        | Serves the Angular build, terminates TLS (Let's Encrypt), proxies `/api` and `/photos` to `api` |
| `api`                  | VM, internal port 8080                  | `TwelveL.Api`; photos on the `photos` Docker volume at `/data/photos` |
| `worker`               | VM                                      | `TwelveL.Worker`; shares the `photos` volume                          |
| `migrator`             | VM, run once per deploy                 | `TwelveL.Migrator`; applies EF Core migrations before `api` restarts  |
| Database               | Azure SQL Database, Basic tier          | Firewall allows only the VM's public IP                               |
| DNS                    | Namecheap                               | `A` records for `@` and `www` point at the VM's static public IP      |

All of it is defined in [`deploy/`](../deploy):

- `backend.Dockerfile` builds `api`, `worker` and `migrator` from one restore (context `src/backend`).
- `web/Dockerfile` builds the Angular workspace and packages it with Caddy and `web/Caddyfile` (context: repository root).
- `docker-compose.yml` is the production stack; the deploy workflow copies it to `/opt/12l` on the VM.
- `.env.example` lists the settings the stack needs; the real `/opt/12l/.env` lives only on the VM.
- `cloud-init.yaml` is the VM's first-boot script (Docker, swap, `/opt/12l`).

## Continuous deployment

[`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml) runs on every push to `main`:

1. Builds the four images and pushes them to GitHub Container Registry, tagged with the commit SHA and `latest`.
2. Over SSH: copies `docker-compose.yml`, pulls the new images, runs the migrator, restarts the stack, prunes old images.
3. Polls `https://12l.ca/api/health` until it returns 200.

Secrets, in the repository's `production` environment:

| Secret           | Value                                                     |
| ---------------- | --------------------------------------------------------- |
| `DEPLOY_HOST`    | Public IP of the VM                                       |
| `DEPLOY_SSH_KEY` | Private key whose public half is in `azureuser`'s `authorized_keys` |
| `SITE_HOST`      | `12l.ca`                                                  |

## Operating the server

```bash
ssh azureuser@<vm-ip>
cd /opt/12l
docker compose ps                 # status
docker compose logs -f api        # or worker, web
docker compose run --rm migrator  # apply migrations by hand
docker compose up -d              # restart with the tags in .env
```

Photos live in the `12l_photos` Docker volume. Back it up with
`docker run --rm -v 12l_photos:/data -v "$PWD":/backup alpine tar czf /backup/photos.tgz -C /data .`.

## Rebuilding from scratch

1. Create a resource group, a Basic Azure SQL server and database, and an Ubuntu VM with a static
   public IP, using `deploy/cloud-init.yaml` as custom data. Open ports 22, 80 and 443.
2. Add the VM's public IP to the SQL server firewall.
3. On the VM, create `/opt/12l/.env` from `deploy/.env.example` with real values.
4. Point `12l.ca` and `www.12l.ca` at the VM's IP.
5. Set the three GitHub secrets and push to `main` (or run the Deploy workflow by hand).
