# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 📝 Document Your Experience

### Game Purpose

Glitchy Guesser is a number guessing game built with Streamlit. The player selects a difficulty level (Easy: 1–20, Normal: 1–100, Hard: 1–500), then tries to guess a randomly generated secret number within a limited number of attempts. After each guess the game shows a hint (higher or lower), tracks a score, and ends when the player wins or runs out of attempts.

---

### Bugs Found

**Bug 1 — Inverted hint logic (`check_guess` in `logic_utils.py`)**
The `check_guess` function had its comparison operators reversed. When `guess > secret` it returned `"Go HIGHER!"` and when `guess < secret` it returned `"Go LOWER!"` — the exact opposite of correct. The fix was swapping the messages so `guess > secret` returns `"Go LOWER!"` and `guess < secret` returns `"Go HIGHER!"`.

**Bug 2 — Attempt counter started at 1 instead of 0**
`st.session_state.attempts` was initialized to `1` in the starter code. This meant the very first guess was already counted as attempt 1 before the player did anything, giving the player one fewer attempt than the difficulty setting advertised. The fix was initializing `attempts` to `0`.

**Bug 3 — New Game button did not reset game state**
The New Game handler only reset `attempts` and regenerated the secret number. It did not clear `score`, `status`, or `history`. This meant a won or lost game stayed in a terminal state and the player could not start fresh. The fix was resetting all five session state keys: `attempts`, `score`, `status`, `history`, and `hint_message`.

**Bug 4 — `parse_guess` accepted decimal numbers**
The starter `parse_guess` converted decimals like `3.5` to integers via `int(float(raw))`, silently accepting an invalid input. The fix was checking for `"."` in the raw string before attempting conversion and returning an error message if found.

**Bug 5 — Info banner always showed "between 1 and 100" regardless of difficulty**
The info banner was hardcoded to `"Guess a number between 1 and 100"`. Switching to Hard (1–500) or Easy (1–20) still showed the wrong range. The fix was using the `low` and `high` values returned by `get_range_for_difficulty(difficulty)`.

---

### Fixes Applied

| Bug | File Changed | What Changed | Why It Works |
|-----|-------------|--------------|--------------|
| Inverted hints | `logic_utils.py` | Swapped `"Go HIGHER!"` and `"Go LOWER!"` in `check_guess` | The comparison `guess > secret` now correctly maps to "go lower" |
| Attempts off-by-one | `app.py` | `st.session_state.attempts` initialized to `0` (was `1`) | Attempt count now starts at zero so the first guess correctly counts as attempt 1 |
| New Game not resetting | `app.py` | New Game handler resets `score`, `status`, `history`, `hint_message` in addition to `attempts` | All state is cleared so a fresh game starts from scratch |
| Decimal inputs accepted | `logic_utils.py` | Added `if "." in raw: return False, None, "Please enter a whole number, not a decimal."` | Decimals are rejected before `int()` conversion, keeping guesses whole numbers only |
| Wrong range in banner | `app.py` | Replaced hardcoded `"1 and 100"` with `f"{low} and {high}"` | Banner now reflects the actual range for the selected difficulty |

---

## 📸 Demo Walkthrough

1. Launch the app with `python -m streamlit run app.py`. The sidebar shows difficulty set to **Normal** (range 1–100, 8 attempts).
2. The info banner reads: *"Guess a number between 1 and 100. Attempts left: 8"*
3. User types `50` and clicks **Submit Guess**. The hint shows **📈 Go HIGHER!** — the secret is above 50.
4. User types `75`. The hint shows **📉 Go LOWER!** — the secret is between 50 and 75. Attempts left: 6.
5. User types `62`. The hint shows **📉 Go LOWER!** — secret is between 50 and 62. Attempts left: 5.
6. User types `55`. The hint shows **📈 Go HIGHER!** — secret is between 55 and 62. Attempts left: 4.
7. User types `59`. The hint shows **📈 Go HIGHER!** — secret is between 59 and 62. Attempts left: 3.
8. User types `61`. Balloons appear and the success message reads: *"You won! The secret was 61. Final score: 50"*
9. User clicks **New Game**. Score resets to 0, attempts reset to 8, a new secret is generated, and the game is ready to play again.

---

## 🧪 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.0.3, pluggy-1.6.0
collected 3 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 33%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 66%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [100%]

============================== 3 passed in 0.06s ==============================
```

## 🚀 Stretch Features

- Enhanced UI: added emoji hints (📈 Go HIGHER! / 📉 Go LOWER!), a collapsible Developer Debug Info panel, difficulty-aware ranges displayed in the sidebar, and a score tracker that updates after every valid guess.
