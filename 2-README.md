# tokenwise

Estimate how many tokens a prompt is and what it costs on popular LLMs. Pure Python, no dependencies, no network.

```
$ echo "Summarize this article in three bullet points." | python -m tokenwise
~12 tokens (46 chars)
  gemini-flash   $0.000001
  ...
```

## Usage

```
python -m tokenwise prompt.txt --out 500      # include expected output tokens
python -m tokenwise prompt.txt --json
```

```python
from tokenwise import estimate_tokens, cost
n = estimate_tokens(text)
cost(n, 500, "claude-sonnet")
```

## Accuracy

It is a heuristic (chars/4 and word-piece blend, denser for non-Latin scripts like Arabic). Expect roughly 15% error against real tokenizers. Good for budgeting, not billing. Prices live in the `PRICES` dict at the top of `tokenwise/__init__.py`; update them to match current provider pricing.

## Test

```
python -m pytest
```

MIT licensed.
