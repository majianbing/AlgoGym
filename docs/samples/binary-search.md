# Binary Search

Binary search applies when the answer space is ordered or when a predicate changes from false to true once.

## Recognition Signals

- The problem asks for the minimum feasible value or maximum valid value.
- A brute force scan tests each candidate independently.
- A helper function can answer whether a candidate works.

## Practice Notes

Track `left`, `right`, and the meaning of each bound before writing code. Most mistakes come from unclear invariants rather than the midpoint formula.

## Review Prompts

- What predicate did you define?
- Was the predicate monotonic?
- Which bound stayed valid after each update?
