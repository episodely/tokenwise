"""Estimate tokens and cost of a prompt without any dependency."""
import re, sys, json, argparse

# USD per 1M tokens (input, output). Edit prices.json-style dict to match current pricing.
PRICES = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-sonnet": (3.00, 15.00),
    "claude-haiku": (0.80, 4.00),
    "gemini-flash": (0.10, 0.40),
}
_WORD = re.compile(r"\w+|[^\w\s]", re.UNICODE)

def estimate_tokens(text: str) -> int:
    """Heuristic: max of chars/4 and ~1.3 tokens per word-piece. Within ~15% for English."""
    if not text:
        return 0
    by_chars = len(text) / 4
    by_words = len(_WORD.findall(text)) * 1.15
    # non-latin scripts (e.g. Arabic) tokenize denser: count them closer to 1 token per 2 chars
    nonlatin = sum(1 for c in text if ord(c) > 0x024F)
    adj = nonlatin / 2 - nonlatin / 4
    return int(round(max(by_chars, by_words) + adj))

def cost(tokens_in: int, tokens_out: int = 0, model: str = "gpt-4o") -> float:
    if model not in PRICES:
        raise ValueError(f"unknown model {model!r}; known: {', '.join(sorted(PRICES))}")
    pin, pout = PRICES[model]
    return (tokens_in * pin + tokens_out * pout) / 1_000_000

def main(argv=None):
    p = argparse.ArgumentParser(prog="tokenwise", description="Estimate tokens and cost.")
    p.add_argument("file", nargs="?", help="file to read (default: stdin)")
    p.add_argument("--out", type=int, default=0, help="expected output tokens")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        text = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    except OSError as e:
        print(f"tokenwise: {e}", file=sys.stderr)
        return 2
    n = estimate_tokens(text)
    rows = {m: round(cost(n, a.out, m), 6) for m in PRICES}
    if a.json:
        print(json.dumps({"tokens": n, "cost_usd": rows}, indent=2))
    else:
        print(f"~{n} tokens ({len(text)} chars)")
        for m, c in sorted(rows.items(), key=lambda x: x[1]):
            print(f"  {m:<14} ${c:.6f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
