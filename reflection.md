# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game I immediately noticed that the number of attempts shown in the game did not match the number shown in the settings sidebar. The hint was also not displaying after a guess even when the "Show Hint" checkbox was checked. As I kept playing I found that the hints were giving the wrong direction — telling me to go higher when I should go lower, and vice versa. The New Game button also failed to properly reset the game, leaving the old score and win status in place so I could not start a fresh round.

**Bug Reproduction Log**

**i. Inverted hint logic — `check_guess` in `logic_utils.py` had reversed comparison operators**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 80 (secret is 50) | Hint: Go LOWER | Hint: Go HIGHER | none |
| Guess of 30 (secret is 50) | Hint: Go HIGHER | Hint: Go LOWER | none |

**ii. New Game button not resetting game state — handler in `app.py` only reset `attempts` and `secret`, not `score`, `status`, or `history`**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Click New Game after winning | Score resets to 0, game status resets to playing | Score unchanged, status stays "won", message: "You already won. Start a new game to play again." | none |

**iii. Hint not displaying after guess — `st.session_state.hint_message` not persisted across reruns in `app.py`**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 45 with Show Hint checked | Hint message displayed below the form | No hint displayed | none |

**iv. Attempt count off-by-one — `st.session_state.attempts` initialized to `1` instead of `0` in `app.py`**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Select Hard difficulty (5 attempts allowed in settings) | Game shows 5 attempts remaining at the start | Game shows 4 attempts remaining on first load | none |

---

## 2. How did you use AI as a teammate?

I primarily used Claude Code for most of the work throughout this project, with some additional help from GitHub Copilot and ChatGPT for specific questions.

**Correct AI suggestion:** When I asked the AI to fix the hint logic and the New Game button reset, both suggestions were correct. Before accepting the changes, I reviewed the code to make sure the logic made sense, then ran the app and played multiple games to verify the hints were pointing in the right direction and that the New Game button was fully resetting the score, history, and game status.

**Incorrect or misleading AI suggestion:** When I asked Copilot to suggest a scoring scheme, it proposed a traditional approach using the formula `points = 100 - 10 * (attempt_number + 1)`. At first glance it looked reasonable, but when I checked the math I realized that winning on the very first attempt would only give 90 points instead of 100, which made no intuitive sense. The correct formula turned out to be `points = 100 - 10 * (attempt_number - 1)`, which gives 100 points for a first-attempt win and decreases from there. The AI's formula was off by one and I caught it by manually calculating the expected output before applying the fix.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed by manually playing the game with the specific scenario that triggered the bug in mind. For example, while testing the New Game button fix I kept playing until I won, then clicked New Game and checked that the score reset to zero, the guess history cleared, and I could start a fresh round. During this process I also discovered an additional bug — the guess input box was not clearing after New Game was clicked — so I reported that to the AI and had it fixed as well.

For automated testing, the AI pointed out that the existing pytest tests were broken after the refactor. When `check_guess` was moved into `logic_utils.py` its return type changed from a plain string to a tuple like `("Win", "🎉 Correct!")`, but the tests were still asserting `result == "Win"`. The AI explained the mismatch and suggested changing the assertions to `result[0] == "Win"`. After making that change, all three tests passed.

---

## 4. What did you learn about Streamlit and state?

Every time you click a button or type something in Streamlit, the entire Python script runs again from top to bottom. That means any regular variable you create gets wiped out on every interaction. Session state is like a notepad that survives those reruns — you store things like the secret number and attempt count there so they don't reset every time the page refreshes. Understanding this was key to fixing bugs like the New Game button not resetting properly and the attempt counter starting at the wrong value.

---

## 5. Looking ahead: your developer habits

One strategy I want to carry into future projects is using planning mode before making changes. Being able to read the AI's suggested approach, think it through, and decide whether to accept or adjust it before any code is actually changed saved a lot of time and helped me stay in control of the direction of the work.

Next time I work with AI on a coding task, I would give it more context upfront — sharing all the relevant files at the start rather than one at a time, so the AI can understand how the files relate to each other and avoid suggestions that fix one file while breaking another.

This project changed the way I think about AI-generated code. At first I assumed that if AI writes the code, you just accept whatever it produces and have no real say in the outcome. But I learned that you can actually direct the AI toward your own understanding and stay in control of every decision — the AI is a collaborator, not an autopilot.
