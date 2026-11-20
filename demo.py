"""Check which permission tier a task falls in and whether it needs human approval.

Usage:
    python demo.py                          # run the built-in examples
    python demo.py "Publish the release notes"   # check your own task
"""
import sys

from router.policy_engine import approval_required, classify_tier, load_policies

EXAMPLES = [
    "Research three competitors' pricing pages",
    "Draft a blog post about our new feature",
    "Open a pull request with the fix",
    "Publish the post to our social accounts",
    "Send an email to the whole mailing list",
    "Force-push the branch",
]


def main() -> None:
    tasks = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else EXAMPLES
    policies = load_policies()
    for task in tasks:
        tier, triggers = classify_tier(task, policies)
        needs = approval_required(tier, triggers, policies)
        tag = f"  [{', '.join(triggers)}]" if triggers else ""
        print(f"{task:<52} -> Tier {tier}  approval: {'YES' if needs else 'no'}{tag}")


if __name__ == "__main__":
    main()
