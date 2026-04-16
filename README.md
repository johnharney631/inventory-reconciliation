# Inventory Reconciliation

This repository contains my solution to an inventory reconciliation take-home exercise.

The implementation follows a test-first workflow and includes a small set of control artifacts to demonstrate an AI-forward, harnessed approach to software delivery. The goal was to keep the Python implementation simple while making the project structure, validation, and execution flow explicit.

The project is intentionally structured so the control artifacts define the work and the Python implementation remains minimal.

## Project Structure

- `reconcile.py` — reconciliation script
- `tests/` — test coverage for reconciliation logic and anomaly handling
- `output/` — generated reconciliation report
- `NOTES.md` — key decisions, assumptions, data-quality findings, and approach
- `AGENT_INSTRUCTIONS.md`, `AGENTS.md`, and supporting control artifacts — workflow and validation context for AI-directed implementation

## How to Run

Install dependencies, then run:

```bash
pytest
python reconcile.py
```
