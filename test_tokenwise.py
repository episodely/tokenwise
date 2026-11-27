from tokenwise import estimate_tokens, cost
def test_empty(): assert estimate_tokens("") == 0
def test_english():
    n = estimate_tokens("The quick brown fox jumps over the lazy dog.")
    assert 8 <= n <= 14
def test_arabic_denser():
    assert estimate_tokens("بسم الله الرحمن الرحيم") > len("بسم الله الرحمن الرحيم") / 4
def test_cost(): assert abs(cost(1_000_000, 0, "gpt-4o") - 2.5) < 1e-9
