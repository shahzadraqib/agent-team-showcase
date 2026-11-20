# AI Agent Team

A small, ready-to-use framework for running a team of AI agents safely. Each agent has a clear role and a permission limit, and anything consequential (publishing, sending messages, spending, deleting, deploying) is stopped until a human approves it.

Use it as a starting point for your own agent setup, whatever your field.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/shahzadraqib/agent-team-showcase.git
cd agent-team-showcase
pip install -r requirements.txt
python demo.py
```

Output:

```
Research three competitors' pricing pages            -> Tier 1  approval: no
Draft a blog post about our new feature              -> Tier 2  approval: no
Open a pull request with the fix                     -> Tier 3  approval: no
Publish the post to our social accounts              -> Tier 4  approval: YES  [public_publishing]
Send an email to the whole mailing list              -> Tier 4  approval: YES  [external_messages]
Force-push the branch                                -> Tier 4  approval: YES  [destructive_operations]
```

Check any task of your own:

```bash
python demo.py "Delete all records in the production database"
```

Run the tests:

```bash
pytest -q
```

## What's included

| Path | What it is |
|---|---|
| `agents/` | Six agent role definitions you can copy into any AI tool as system prompts |
| `skills/` | Reusable procedures the agents follow (verification, handoffs, minimal changes) |
| `policies.yaml` | The rules: permission tiers and which actions need approval |
| `router/policy_engine.py` | Enforces the rules in code |
| `demo.py` | Command-line checker for any task |
| `docs/` | Architecture and approval policy explained |

## The agents

| Agent | Role | Permission limit |
|---|---|---|
| **Forge** | Developer | Local changes only |
| **Scout** | Researcher | Read only |
| **Sentinel** | Reviewer | Read only, can block work |
| **Echo** | Self-improvement | Proposes changes, never applies core rule changes alone |
| **Ember** | Content creator | Drafts only |
| **Relay** | Publisher | Publishes only after explicit approval |

## Permission tiers

| Tier | Meaning | Needs approval? |
|---:|---|---|
| 0 | Reference only | Cannot run |
| 1 | Read | No |
| 2 | Local or reversible write | No |
| 3 | External but reversible (staging, pull requests) | Depends on project |
| 4 | Consequential (publish, message, spend, delete, deploy, credentials) | **Yes, every time** |

## How a task flows

```
 goal in plain language
        │
        ▼
 policy engine ──▶ tier + triggers ──▶ Tier 4? ──▶ stop and ask a human
        │
        ▼
 pick the fewest agents needed
        │
        ▼
 agent works within its limit
        │
        ▼
 verification (evidence that can fail) ──▶ Sentinel review
        │
        ▼
 Echo retrospective ──▶ proposed improvement (reviewed, never auto-applied)
```

## Customize it

- **Change what needs approval:** edit the patterns under `tier4_actions` in `policies.yaml`.
- **Pre-approve one narrow action:** add an entry to `standing_authorizations` in `policies.yaml` (empty by default).
- **Add an agent:** copy any file in `agents/`, then set its mission, responsibilities, limit, and stop conditions.
- **Use it from your own code:**

```python
from router.policy_engine import load_policies, classify_tier, approval_required

policies = load_policies()
tier, triggers = classify_tier("Send the invoice email to every customer", policies)
if approval_required(tier, triggers, policies):
    print("Ask a human first:", triggers)
```

## Design principles

1. Inspect before building. Reuse before creating.
2. Give each agent only the context it needs.
3. Trust evidence, not model confidence.
4. Improvements must be evidence-based, reviewed, and reversible.
5. Consequential actions need explicit human approval, every time.
6. Fail closed: anything not approved does not run.

## Author

Created and led by **Raqib Shahzad**. I designed each agent's role and limits, the approval model, and the review and verification rules.

## License

MIT
