from logic_utils import check_guess, parse_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


def test_empty_input():
    # Empty string should be rejected with an error message
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_non_numeric_input():
    # A non-numeric string like "abc" should be rejected
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


def test_decimal_input():
    # A decimal like "3.5" should be rejected — only whole integers are valid
    ok, value, err = parse_guess("3.5")
    assert ok is False
    assert value is None
    assert err == "Please enter a whole number, not a decimal."
