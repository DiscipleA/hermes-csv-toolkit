# Add opt-in exact numeric sorting with --numeric

AI-assisted demonstration planning artifact. No feature implementation is included.

## Acceptance criteria
- [ ] Default sorting remains stable lexicographic; --numeric uses decimal.Decimal, not float.
- [ ] Handle finite signed decimals and exponents while preserving original field text and stable ties.
- [ ] Reject invalid, empty or non-finite sort keys before any output; document the option and add subprocess tests.

## Test plan
Add behavior tests first, observe failure, implement only the approved enhancement, and rerun the full baseline suite.

## Status
Draft planning only. Waiting for owner authorization; the maintenance job must leave this branch unchanged.
