# AGENT_INSTRUCTIONS.md

Defines the execution entry point for the AI agent.

Follow the workflow defined in AGENTS.md and execute each hook in order.

Workflow:
1. hooks/pre_implementation.md
2. hooks/pre_test_generation.md
3. Implement reconciliation logic
4. hooks/pre_output_validation.md
5. hooks/pre_completion_review.md

Do not proceed to the next step until the current step is satisfied.
