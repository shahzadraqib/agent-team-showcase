import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from router import policy_engine as pe  # noqa: E402


@pytest.fixture(scope="module")
def pol():
    return pe.load_policies()


@pytest.mark.parametrize("task,tier", [
    ("Research competitor pricing", 1),
    ("Draft a newsletter", 2),
    ("Open a pull request with the fix", 3),
    ("Publish the post", 4),
    ("Send an email to all subscribers", 4),
    ("Rotate the API keys", 4),
])
def test_tier_classification(pol, task, tier):
    assert pe.classify_tier(task, pol)[0] == tier


def test_tier4_requires_approval(pol):
    tier, triggers = pe.classify_tier("Publish the post", pol)
    assert pe.approval_required(tier, triggers, pol) is True


def test_lower_tiers_need_no_approval(pol):
    tier, triggers = pe.classify_tier("Draft a newsletter", pol)
    assert pe.approval_required(tier, triggers, pol) is False


def test_standing_authorization_must_cover_every_trigger(pol):
    p = dict(pol, standing_authorizations=[{"action": "public_publishing"}])
    assert pe.approval_required(4, ["public_publishing"], p) is False
    assert pe.approval_required(4, ["public_publishing", "spending"], p) is True


def test_no_standing_authorizations_by_default(pol):
    assert pol["standing_authorizations"] == []


def test_only_enabled_capabilities_execute(pol):
    assert pe.can_execute({"onboarding_state": "ENABLED"}, pol)[0] is True
    for state in ("DISCOVERED", "QUARANTINED", "REFERENCE_ONLY", None):
        assert pe.can_execute({"onboarding_state": state}, pol)[0] is False


def test_unknown_egress_blocked(pol):
    cap = {"egress_allow": ["api.example.com"]}
    assert pe.egress_allowed(cap, "api.example.com", pol)[0] is True
    assert pe.egress_allowed(cap, "evil.example.net", pol)[0] is False
    assert pe.egress_allowed({}, "api.example.com", pol)[0] is False
