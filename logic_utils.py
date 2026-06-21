def get_range_for_difficulty(difficulty: str):
    """Return the valid guess range for a given difficulty level.

    Args:
        difficulty (str): One of "Easy", "Normal", or "Hard".

    Returns:
        tuple[int, int]: A (low, high) pair representing the inclusive
        range of valid guesses. Defaults to (1, 100) for unknown values.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """Parse raw text input from the user into a validated integer guess.

    Rejects empty input, decimal numbers, and non-numeric strings.
    Only whole integers are considered valid guesses.

    Args:
        raw (str): The raw string entered by the user in the guess field.

    Returns:
        tuple[bool, int | None, str | None]: A three-element tuple of
        (ok, guess_int, error_message). If ok is True, guess_int holds
        the parsed integer and error_message is None. If ok is False,
        guess_int is None and error_message describes the problem.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    if "." in raw:
        return False, None, "Please enter a whole number, not a decimal."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a player's guess against the secret number.

    Args:
        guess (int): The integer value the player guessed.
        secret (int): The secret number the player is trying to find.

    Returns:
        tuple[str, str]: A (outcome, message) pair. outcome is one of
        "Win", "Too High", or "Too Low". message is a human-readable
        hint string with an emoji (e.g., "📉 Go LOWER!").
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update the player's score based on the outcome of a guess.

    Winning awards points that decrease with each additional attempt.
    Incorrect guesses apply a penalty that increases after attempt 3.

    Args:
        current_score (int): The player's score before this guess.
        outcome (str): The result of the guess — "Win", "Too High",
            or "Too Low".
        attempt_number (int): The 1-based count of guesses made so far.

    Returns:
        int: The updated score, clamped between 0 and 100 on a win,
        or floored at 0 on a penalty.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        new_score = current_score + points
        return min(100, max(0, new_score))

    if outcome in ["Too High", "Too Low"]:
        penalty = -10 if attempt_number <= 3 else -15
        return max(0, current_score + penalty)

    return current_score
