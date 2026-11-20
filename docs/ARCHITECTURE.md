# Architecture

## Layers

1. **Control plane.** Takes a goal, identifies the project and data sensitivity, and builds a *capability plan*: which agents, which skills, which tools, which permission tier, and whether approval is required.
2. **Policy engine.** Pure functions that classify a task into a permission tier, match consequential-action triggers, and check capability state and network egress. Policy lives in `policies.yaml`, so changing a rule is a reviewed change, not a code edit.
3. **Agents.** Specialists with a written contract: mission, personality, responsibilities, non-responsibilities, allowed and forbidden tools, permission ceiling, handoff rules, stop conditions, and definition of done.
4. **Skills.** Reusable procedures an agent follows. A skill names the tools it may use and fails closed if one is not approved.
5. **Verification and review.** Work is checked with evidence that can fail, then reviewed by a separate agent that is allowed to block.
6. **Learning loop.** A retrospective agent proposes improvements from evidence. Proposals are not applied automatically.

## Key decisions

- **Least privilege by default.** Each agent has a ceiling. Reading and local drafting are free; external and irreversible actions are gated.
- **Separation of duties.** The agent that builds a thing cannot approve it. The agent that researches cannot act on its own findings.
- **Minimum context.** Only the skills, memory, and history a task needs are loaded.
- **Scoped handoffs.** Agents pass compact, scoped packets to each other, never full transcripts.
- **Human in the loop at real boundaries.** Approval is requested for consequential actions only, so it stays meaningful.
