# Vela-HQ Build and Deployment

## Purpose and scope

Vela-HQ is the Python cloud fleet-management application: API, agent gateway,
Vue web frontend, migrations, and local Postgres/MinIO/Redis/Keycloak services.
The root Makefile is the development orchestrator and uses a `.venv`, npm, and
the `infra/docker-compose.yml` project named `velahq`.

## 1. Prerequisites

- Docker and Docker Compose, Python 3.12+, Node.js/npm, and GNU Make.
- Network access to pull development images and Python/npm dependencies.
- Development secrets/configuration for any non-local deployment. Compose
  defaults (`admin/admin`, `velahq-dev-secret`, and local database passwords)
  are for a trusted development network only.

## 2. Setup

Run `make doctor`, then `make install` to create `.venv`, install editable API
and gateway packages with dev dependencies, and run `npm install` in `web/`.
`make db-up` starts the compose services, waits for Postgres, creates
`velahq_test`, prepares the MinIO bucket, and waits for Keycloak.

## 3. Build and compile

`make build` runs `npm run build` in `web/` and creates the production frontend
bundle. The API and gateway are Python packages and are installed by `make
install`; there is no separate C++ or Rust compile target in this Makefile.

## 4. Tests and lint

- `make test-api` and `make test-gateway` run pytest with the configured test
  database and S3 endpoint; `make test-web` runs `npx vitest run`.
- `make test` runs all three suites.
- `make lint-api` and `make lint-gateway` run Ruff; `make lint-web` runs npm
  lint and `vue-tsc --noEmit`; `make lint` runs all three.

## 5. Packaging and artifacts

The web production output is `web/dist`; local Python environments and package
metadata remain in the repository workspace. The compose file provides named
Postgres, MinIO, and Keycloak volumes, which persist data across `db-down`.
No root Makefile image build or release packaging target is defined.

## 6. Deployment, install, and run

Apply migrations with `make migrate`. Seed a development admin invitation with
`make seed EMAIL=admin@example.com`. `make run` starts the database, migrates,
and launches API, gateway, and web in `.run/`; it prints LAN URLs for ports
8000, 50051, 5173, and Keycloak 8081. Use `make logs` to tail service logs and
`make stop` to stop application processes. `make db-down` stops compose.

## 7. Cleanup

`make stop` leaves database containers running. Use `make db-down` to stop
them; named volumes persist unless removed with an explicit Docker volume
operation. `make clean` removes `.venv`, `.run`, `web/node_modules`, `web/dist`,
caches, and Python cache directories.

## 8. Hardware, cloud, and manual verification caveats

This is a cloud/service leaf, but end-to-end operation requires a reachable
database, object store, OIDC provider, gateway client, and correct secrets.
The compose credentials and HTTP Keycloak setup are development-only. Verify
OIDC redirects, cookies, authorization, migrations, background operations, and
device/gateway connectivity manually before exposing the service outside a
trusted local network.