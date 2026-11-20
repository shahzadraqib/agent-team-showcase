"""Classify sample tasks and show which would need human approval."""
from router.policy_engine import approval_required, classify_tier, load_policies

TASKS = [
    "Research three competitors' pricing pages",
    "Draft a blog post about caregiver burnout",
    "Open a pull request with the fix",
    "Publish the post to our social accounts",
    "Send an email to the full client list",
    "Force-push the branch",
]

policies = load_policies()
for task in TASKS:
    tier, triggers = classify_tier(task, policies)
    needs = approval_required(tier, triggers, policies)
    tag = f"  [{', '.join(triggers)}]" if triggers else ""
    print(f"{task:<52} -> Tier {tier}  approval: {'YES' if needs else 'no'}{tag}")
