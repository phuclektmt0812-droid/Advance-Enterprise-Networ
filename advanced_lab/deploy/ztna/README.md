# OpenZiti ZTNA lab bootstrap

This folder prepares the official OpenZiti Docker Compose learning quickstart.
It is a practical lab bootstrap, not a production-hardened deployment.

## Prerequisites

- Docker Desktop with Linux containers and Docker Compose V2.
- Enough free memory for the containers; on an 8 GB host, stop GNS3 nodes and
  other memory-heavy applications first.
- A local-only test service. Do not publish private services directly to the
  public Internet for this exercise.

## Prepare

From PowerShell at the repository root:

```powershell
Set-Location advanced_lab/deploy/ztna
.\prepare-openziti.ps1
```

The script downloads the current official quickstart Compose file and
environment template. It creates `.env` only if one does not already exist.
Review the advertised controller/router addresses and credentials in `.env`
before starting. Do not commit `.env`, JWT enrollment files, certificates,
or private keys.

## Start / stop

```powershell
docker compose up -d
docker compose ps
docker compose logs --tail 100
docker compose down
```

Do not use `docker compose down -v` unless you intentionally want to erase
the lab's persistent controller database and PKI.

## Configure a named private service

Use the Ziti CLI inside the controller container after logging in. The
official OpenZiti "Your First Service" guide is the authoritative, versioned
procedure for creating:
1. an intercept.v1 config for the client-side name and port;
2. a host.v1 config for the private application address and port;
3. a service that binds those configs;
4. a Dial policy for the authorized client identity;
5. a Bind policy for the designated server/edge-router identity;
6. edge-router and service-edge-router policies required by the deployment.

Use the lab service name `tvi-inventory` and target only the private test
application TCP/8080. Assign a role attribute to the authorized test identity
(e.g. `tvi-staff`) and a different role attribute to the service-hosting
identity. Do not authorize all identities or publish the whole 10.43.0.0/16
network.

The exact CLI command sequence is intentionally not duplicated here because
OpenZiti CLI flags and bootstrap defaults can change by release. Follow the
official docs linked below and record the installed image version with the
test evidence.

## Acceptance

- Authorized enrolled identity can reach only `tvi-inventory`.
- Unenrolled identity cannot reach the service.
- Authorized identity cannot route or ping arbitrary private subnets through
  the overlay.
- Controller and router show healthy status and service-policy decisions are
  visible in logs.

## Official references

- Docker Compose quickstart: https://openziti.io/docs/learn/quickstarts/network/local-docker-compose/
- Docker controller deployment: https://openziti.io/docs/guides/deployments/docker/controller/
- Docker router deployment: https://openziti.io/docs/guides/deployments/docker/router/
- First service and Dial/Bind policy: https://openziti.io/docs/learn/quickstarts/services/ztha/
