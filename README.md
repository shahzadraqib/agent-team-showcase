# AI Agent Team: a governed multi-agent system

A public, trimmed-down reference of a multi-agent system I designed and directed. A single control plane routes plain-language goals to a small team of specialist AI agents, enforces permission tiers, and requires human approval before anything consequential happens (publishing, spending, messaging, deleting).

The full production system is private. This repo keeps the architecture, agent role definitions, approval policy, and a working policy engine with tests. It contains no credentials, client data, or business-specific workflows.

Built with **Claude Code**. Specified, directed, reviewed, and approved by me.

## My role: product owner and lead

I treated the agents like a team I had to staff, govern, and hold accountable.

| Responsibility | What I did |
|---|---|
| **Defined the mission and roles** | Wrote each agent's mission, boundaries, and handoff rules so no two agents own the same job. 13 roles in the private system, 6 shown here. |
| **Set the governance model** | Designed five permission tiers and a hard rule that consequential actions need my explicit approval every time. Silence is never consent. |
| **Managed risk before adoption** | Evaluated and security-scanned 53 external repositories and set a 12-step onboarding pipeline. Nothing runs until it passes review. |
| **Sequenced delivery in stages** | Preserve first, then the control plane, then the core team, then domain agents, and only build infrastructure the next real workflow needed. |
| **Required evidence, not confidence** | Every task ends with verification that can fail. A separate reviewer agent can block work, and the builder cannot approve its own output. |
| **Built a learning loop under control** | Retrospectives turn outcomes into proposed changes. A change needs two pieces of evidence, a regression test, review, and my approval if it touches core rules. |

## The team (shown here)

| Agent | Role | Permission ceiling | Can it act externally? |
|---|---|---|---|
| **Forge** | Developer | Tier 2 (local write) | No |
| **Scout** | Researcher | Tier 1 (read) | No |
| **Sentinel** | Reviewer | Tier 1 (read), may block | No |
| **Echo** | Self-improvement | Tier 2, proposals only | No |
| **Ember** | Content creator | Tier 2 (drafts) | No |
| **Relay** | Publisher | Tier 3, publishing needs Tier 4 approval | Only with approval |

See [`agents/`](agents/) for the full role definitions.

## How a task flows

```
 goal in plain language
        │
        ▼
 classify project + sensitivity ──▶ policy engine (tier, triggers, approval?)
        │                                   │
        ▼                                   ▼
 pick the minimum agents/skills     Tier 4? ──▶ stop and ask a human
        │
        ▼
 agent executes within its ceiling
        │
        ▼
 verification (evidence that can fail) ──▶ Sentinel review ──▶ run summary
        │
        ▼
 Echo retrospective ──▶ proposed improvement (never auto-applied to core rules)
```

More detail in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and [`docs/APPROVAL_POLICY.md`](docs/APPROVAL_POLICY.md).

## Try the policy engine

```bash
pip install -r requirements.txt
python demo.py
pytest -q
```

`demo.py` classifies sample tasks and shows which ones would be blocked pending human approval:

```
Research three competitors' pricing pages            -> Tier 1  approval: no
Draft a blog post about caregiver burnout            -> Tier 2  approval: no
Open a pull request with the fix                     -> Tier 3  approval: no
Publish the post to our social accounts              -> Tier 4  approval: YES  [public_publishing]
Send an email to the full client list                -> Tier 4  approval: YES  [external_messages]
Force-push the branch                                -> Tier 4  approval: YES  [destructive_operations]
```

## Design principles

1. Inspect before building. Reuse before creating.
2. Load the minimum context a task needs.
3. Measure real outcomes, not model confidence.
4. Self-improvement must be evidence-driven, auditable, and reversible.
5. Consequential actions need explicit human approval, every time.
6. Agents fail closed: a capability that is not approved does not run.

## What is not in this repo

Credentials, API keys, client and business data, internal workflows, third-party code, run logs, and commit history from the private system. This repo starts from a clean history.

## License

MIT
