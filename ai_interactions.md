# AI Interactions Log

---

## Agent Workflow (SF8)

**What task did you give the agent?**

I asked Claude Code to refactor the core game logic out of `app.py` and into `logic_utils.py`, which started as a stub file with `raise NotImplementedError` in all four functions. The instruction was: "Move the game logic functions into logic_utils.py, implement them correctly, fix any bugs in the logic, and update the imports in app.py."

**What did the agent do?**

- Implemented `get_range_for_difficulty` to return correct `(low, high)` tuples for Easy (1–20), Normal (1–100), and Hard (1–500)
- Implemented `parse_guess` to validate user input, reject empty strings, non-numeric text, and decimal numbers
- Implemented `check_guess` to compare the guess to the secret and return the correct `(outcome, message)` tuple with emoji hints
- Implemented `update_score` to award points on a win and apply penalties for incorrect guesses
- Updated `app.py` to remove the inline function definitions and import from `logic_utils` instead

**What did you have to verify or fix manually?**

The agent's initial `update_score` implementation used the formula `points = 100 - 10 * (attempt_number + 1)`, which gave only 90 points for a first-attempt win instead of 100. I caught this by manually calculating the expected output: attempt 1 should give 100 points, attempt 2 should give 90, and so on. The correct formula is `points = 100 - 10 * (attempt_number - 1)`. I asked the agent to apply the correction and verified the math before accepting.

---

## Test Generation (SF7)

**Prompt used:**
> "Generate pytest edge case tests for the `parse_guess` function in `logic_utils.py`. Cover: empty string input, a non-numeric string like 'abc', and a decimal number like '3.5'. For each, assert that `ok` is False, `value` is None, and the correct error message is returned."

| Edge Case | AI-Suggested Test | Did It Pass? | Rationale |
|-----------|-------------------|--------------|-----------|
| Empty string `""` | `ok, value, err = parse_guess("")` → assert `ok is False`, `err == "Enter a guess."` | Yes | Players might click Submit without typing anything; this ensures the game does not crash or count a blank as a guess |
| Non-numeric string `"abc"` | `ok, value, err = parse_guess("abc")` → assert `ok is False`, `err == "That is not a number."` | Yes | Accidental text input should be caught before `int()` conversion raises an unhandled exception |
| Decimal number `"3.5"` | `ok, value, err = parse_guess("3.5")` → assert `ok is False`, `err == "Please enter a whole number, not a decimal."` | Yes | The secret is always an integer; accepting `3.5` and silently rounding to `3` would give misleading feedback |

---

## Linting & Style (SF9)

**Prompt used to generate docstrings:**
> "Add professional PEP 257-style docstrings to all four functions in `logic_utils.py`. Each docstring should include an Args section describing parameter names, types, and meanings, and a Returns section describing the return type and what it represents."

**Linting output (flake8 logic_utils.py) after applying docstrings:**

```
(no output — 0 errors, 0 warnings)
```

**Changes applied:**

- Replaced all single-line docstrings with multi-line docstrings covering Args and Returns
- No variable or function renaming was needed — existing names already followed PEP 8 snake_case conventions
- Line lengths were kept under 79 characters throughout
- Two blank lines between top-level functions were already in place and required no changes

---

## Model Comparison (SF11)

**Task given to both models:** Fix the `update_score` function so that winning on the first attempt gives the maximum possible score.

**Specific bug:** The starter formula `points = 100 - 10 * (attempt_number + 1)` produces 90 points on attempt 1 (the best possible play) instead of 100.

| | Copilot | Claude |
|-|---------|--------|
| **Model** | GitHub Copilot (GPT-4o) | Claude Sonnet (Claude Code) |
| **Suggested formula** | `points = 100 - 10 * (attempt_number + 1)` | `points = 100 - 10 * (attempt_number - 1)` |
| **Score on attempt 1** | 90 (incorrect) | 100 (correct) |
| **Explanation quality** | Suggested the formula without showing expected output per attempt | Showed a table: attempt 1 → 100, attempt 2 → 90, attempt 3 → 80, making the intent immediately verifiable |
| **More Pythonic?** | Both are equally Pythonic as one-liners | Same |
| **Clearer explanation?** | No — the off-by-one error was not visible from the suggestion alone | Yes — the worked example made it easy to spot the correct behavior |

**Conclusion:** Claude's suggestion was correct and its explanation was easier to verify. Copilot's formula had an off-by-one error that I only caught by manually computing the expected output for attempt 1. The worked example Claude provided would have caught the mistake immediately.
