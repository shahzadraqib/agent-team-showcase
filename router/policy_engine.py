"""Policy engine: machine-readable enforcement of policies.yaml.

Pure functions. The only I/O is loading the YAML file.

    load_policies(path=None) -> dict
    classify_tier(task, policies) -> (tier, triggers)
    approval_required(tier, triggers, policies) -> bool
    can_execute(capability, policies) -> (bool, reason)
    egress_allowed(capability, host, policies) -> (bool, reason)
"""
from __future__ import annotations

import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY_PATH = os.path.join(ROOT, "policies.yaml")


def load_policies(path: str | None = None) -> dict:
    with open(path or POLICY_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def classify_tier(task: str, policies: dict) -> tuple[int, list[str]]:
    """Return the permission tier implied by the task text and any Tier 4 triggers matched."""
    text = task.lower()
    triggers = [
        name
        for name, patterns in policies["tier4_actions"].items()
        if any(re.search(p, text, re.I) for p in patterns)
    ]
    if triggers:
        return 4, triggers
    if re.search(r"\b(staging|sandbox|test account|pull request|open (a )?pr)\b", text):
        return 3, []
    if re.search(r"\b(draft|write|create|generate|build|implement|fix|refactor|save|edit)\b", text):
        return 2, []
    return 1, []


def approval_required(tier: int, triggers: list[str], policies: dict) -> bool:
    """Tier 4 needs approval unless every matched trigger has a standing authorization."""
    if tier < 4:
        return False
    granted = {g.get("action") for g in policies.get("standing_authorizations") or []}
    return not all(t in granted for t in triggers)


def can_execute(capability: dict, policies: dict) -> tuple[bool, str]:
    """A capability runs only if its onboarding state is executable. Everything else fails closed."""
    state = capability.get("onboarding_state")
    if state in policies["executable_states"]:
        return True, f"state {state} is executable"
    return False, f"state {state!r} is not executable"


def egress_allowed(capability: dict, host: str, policies: dict) -> tuple[bool, str]:
    """Unknown network destinations are blocked unless the capability allowlists them."""
    allow = capability.get("egress_allow") or []
    if host in allow:
        return True, f"{host} is allowlisted"
    if policies["egress"]["unknown_destination"] == "block":
        return False, f"{host} is not allowlisted; unknown destinations are blocked"
    return True, "policy permits unknown destinations"
