# ghs-token-check

Run your token redaction and validation rules against real GitHub App installation tokens, without ever printing a token.

Since October 2, 2026, GitHub issues installation tokens (including the Actions `GITHUB_TOKEN`) in a new `ghs_<app id>_<JWT>` format. This repo uses the workflow's own `GITHUB_TOKEN` as the test subject.

## Run it

1. Fork this repo (or copy `.github/workflows`, `scripts/` and `patterns.txt`).
2. Add your own rules to `patterns.txt`, one `name<TAB>regex` per line (Python `re` syntax).
3. Run the workflows from the Actions tab or the CLI:

```bash
gh workflow run check.yml    # one token: shape, your patterns, gitleaks, trufflehog, detect-secrets, Postgres and MySQL columns
gh workflow run sample.yml   # 40 tokens, one per job: how often each pattern redacts the whole token
```

To summarise a sample run:

```bash
gh run view <run-id> --log | grep -o 'SAMPLE {.*}' | sed 's/^SAMPLE //' > samples.jsonl
cd scripts && python3 aggregate.py ../samples.jsonl
```

## What each script does

- `scripts/shape.py`: length, separators, segment lengths, the decoded JWT header and the payload claim names. It never prints the payload values or the signature.
- `scripts/regex_check.py`: for each pattern, whether it matches and how many token characters fall outside the first match. For patterns that start with `ghs_`, which appears once per token, that equals what a `re.sub` redaction leaves visible.
- `scripts/sample.py`: the same per job, plus a short hash of the public `ghs_<app id>_<header>` prefix to show it never changes.
- `.github/workflows/check.yml` also runs the latest gitleaks, trufflehog and detect-secrets on a file that holds the token, and inserts it into `VARCHAR(40)` and `VARCHAR(255)` columns on Postgres 17 and MySQL 8.4.

## Results from 2026-10-05

`results/` holds the recorded output: one full check and a 40-token sample. In short:

| Pattern | Whole token redacted | Most characters left visible |
| --- | --- | --- |
| `ghs_[0-9a-zA-Z]{36}` (legacy, and gitleaks 8.30.1) | 0 of 40 | 377 of 377 |
| `(?:ghu\|ghs)_[A-Za-z0-9_]{36}` | 0 of 40 | 337 |
| trufflehog 3.97.9 detector regex | 0 of 40 | 331 |
| GitHub's first recommended regex (May 15) | 8 of 40 | 86 |
| GitHub's corrected regex (May 26) | 40 of 40 | 0 |

The write-up: https://devops-daily.com/posts/github-app-installation-tokens-redaction

## License

MIT
