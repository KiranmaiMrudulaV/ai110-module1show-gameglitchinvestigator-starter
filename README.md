# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The purpose of the game is to guess a randomly generated secret number using the hints provided by the application. After each guess, the game tells the player whether they should guess higher or lower until the correct number is found. The game also tracks progress and allows the player to start a new game after winning.
- [ ] Detail which bugs you found.
Incorrect Hint Logic
The game displayed the wrong hint direction. When a guess was higher than the secret number, it showed "Go HIGHER" instead of "Go LOWER," and vice versa.
New Game Button Not Resetting the Game
Clicking the New Game button did not properly reset the game state. Previous guesses, scores, and win status remained, preventing a fresh game from starting correctly.
Hint Display Bug
When the "Show Hint" checkbox was enabled and a guess was submitted, the expected hint was not displayed to the user.
- [ ] Explain what fixes you applied.
Fixed Incorrect Hint Logic
I corrected the comparison logic responsible for generating hints. Previously, when a guess was higher than the secret number, the game incorrectly displayed "Go HIGHER," and when a guess was lower, it displayed "Go LOWER." After updating the conditions, the game now provides the correct higher/lower guidance to the player.
Verification
I tested multiple guesses above and below the secret number and confirmed that the correct hint is displayed in each case. This resolved the misleading feedback issue and made the game playable as intended.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
