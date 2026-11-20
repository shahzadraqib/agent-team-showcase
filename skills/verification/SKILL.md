# Verification

**Purpose:** Prove a result with evidence that can fail before accepting it.

## Procedure
1. State the acceptance criterion in one sentence.
2. Choose a check that would fail if the work were wrong (a test, a diff, a rendered output, a source).
3. Run it and capture the real output.
4. Redact secrets from any evidence before filing.
5. Report pass or fail with the evidence attached.

## Done when
The evidence exists, was produced by an actual run, and could have shown a failure.

## Fails closed
If no check can fail, the result is reported as unverified, not as passing.
