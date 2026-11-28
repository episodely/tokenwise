from tokenwise import estimate_tokens, cost
def test_empty(): assert estimate_tokens("") == 0
def test_english():
    n = estimate_tokens("The quick brown car jumps over the lazy bridge.")
    assert 8 <= n <= 14
def test_arabic_denser():
    assert estimate_tokens("بسم الله الرحمن الرحيم") > len("بسم الله الرحمن الرحيم") / 4
def test_cost(): assert abs(cost(1_000_000, 0, "gpt-4o") - 2.5) < 1e-9

# regression tests: review findings
def test_unknown_model_friendly():
    import pytest
    with pytest.raises(ValueError, match="unknown model"):
        cost(10, 0, "no-such-model")
def test_cli_missing_file(capsys):
    from tokenwise import main
    assert main(["/no/such/file.txt"]) == 2
