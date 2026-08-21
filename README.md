# Vela-HQ

Cloud fleet-management app for Vela devices — view devices remotely, manage
pairing/authorization, and run fleet operations (telemetry, faults/alarms,
logs, OTA updates, backup/restore, provisioning, factory reset, disable,
location).

Status: **planning**. See [PLAN.md](PLAN.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Overview

## Project Summary

Vela-HQ is the cloud fleet-management service for Vela devices. The Python API
under `api/app/` contains authentication and OIDC/session helpers, database
access, middleware, models, and the application entry point. Models cover
devices, alarms, faults, audit logs, backups, credentials, log bundles, and
pending commands. A separate `agent-gateway/` package contains a client,
factories, a `pyproject.toml`, and pytest tests for frames, pairing, and stale
session sweeping. These files demonstrate a substantial service skeleton and
provide direct gateway test evidence.

The product intent includes remote device visibility, authorization, telemetry,
alarms, logs, OTA, backup/restore, provisioning, factory reset, disable, and
location. The original README labels the broader product planning-stage, so a
model or module is not treated as proof of an end-to-end fleet operation.
Database integration, identity-provider behavior, command delivery, and
production deployment remain partial or unknown where local evidence does not
settle them.

The gateway tests give HQ a narrower but concrete validation foothold than the
API model inventory. They can demonstrate frame, pairing, and stale-state
behavior in isolation, while the API still needs tests that connect routes to
database records and authorization decisions. The product-level operations
described by the original README require device protocol contracts and durable
job state; neither follows automatically from model names. Treat PLAN.md and
ARCHITECTURE.md as design authority until implementation and integration tests
cover each operation. Identity-provider configuration, database migrations,
background workers, and deployment secrets are especially important manual
boundaries. This table intentionally uses partial or unknown rather than
claiming the whole fleet workflow is complete.

## Feature Status

| # | Name / Description | Implemented? | Test Coverage? | Manual Test |
|---:|---|---|---|---|
| 1 | Python API application entry point | Implemented | API-wide coverage unknown | [ ] Manual verification required |
| 2 | Authentication, OIDC, and sessions | Implemented | Gateway pairing coverage; API depth unknown | [ ] Manual verification required |
| 3 | Device, credential, audit, alarm, fault, backup, log, and command models | Implemented | Model coverage not identified | [ ] Manual verification required |
| 4 | Database base/dependency layer | Implemented | Integration depth unknown | [ ] Manual verification required |
| 5 | Agent gateway frame handling | Implemented | `test_frames.py` | [ ] Manual verification required |
| 6 | Agent pairing flow | Implemented | `test_pairing.py` | [ ] Manual verification required |
| 7 | Stale-agent/session sweeping | Implemented | `test_stale_sweep.py` | [ ] Manual verification required |
| 8 | Telemetry, alarms, and remote logs | Partial | Models present; E2E coverage unknown | [ ] Manual verification required |
| 9 | OTA, backup/restore, provisioning, reset, disable, and location | Partial | Planning/model evidence; workflow unknown | [ ] Manual verification required |
| 10 | Production identity, database, and deployment integration | Unknown | No deployment verification found | [ ] Manual verification required |

Run gateway tests from `agent-gateway/`; use `PLAN.md` and `ARCHITECTURE.md` to
reconcile planned workflows with the API implementation.
