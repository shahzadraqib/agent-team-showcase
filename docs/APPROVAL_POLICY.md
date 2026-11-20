# Approval Policy

`policies.yaml` is authoritative and machine-enforced by `router/policy_engine.py`. This file is the human-readable mirror.

| Tier | Name | Examples | Approval |
|---:|---|---|---|
| 0 | Reference | Patterns and catalogs | Cannot execute |
| 1 | Read | Research, inspect code, analysis | None |
| 2 | Local write | Files, code, drafts, local tests | None |
| 3 | External reversible | Staging, test accounts, pull requests, draft scheduling | Project ceiling |
| 4 | Consequential | Publishing, external messages, production deploys, spending, destructive operations, credential changes | **Explicit approval every time** |

## How approval works

1. The router produces a plan with the tier, matched triggers, and `approval_required`.
2. The owning agent states exactly what will happen, where, whether it is reversible, and the rollback.
3. A human replies with an explicit approval, which is recorded before execution.
4. After the action, verification captures proof (an ID or URL).
5. **Silence is not consent.** A timed-out prompt is a no. A declined action is never retried by rewording it.

## Standing authorizations

None by default. A grant is narrow (one trigger, one scope, a date, an optional expiry) and is added only by the human editing policy, never by an agent.

## Refused outright

Running any capability that has not passed onboarding, and writing secrets into the repository.
