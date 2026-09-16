# 20-team bracket fixture

Synthetic. Twenty invented teams across five affiliation groups, with a previous
champion (`team-01`) and runner-up (`team-02`).

| Property | Value |
|---|---|
| Bracket slots | 32 |
| Preliminary matches | 4 |
| Preliminary participants | 8 |
| Byes into the round of 16 | 12 |
| Bye policy | performance-qualified |
| Seed | `twenty-team-fixture-2026` |
| Input digest | `464de0ad34aa35b9` |
| Feasible | True |

Reproduce and verify:

```bash
python3 -m atj bracket build --input tests/fixtures/bracket-20-team/roster.json \
  --seed twenty-team-fixture-2026 --output /tmp/bracket.json
python3 -m atj bracket verify tests/fixtures/bracket-20-team/bracket.json \
  --reproduce tests/fixtures/bracket-20-team/roster.json
```

The constraint audit inside `bracket.json` records previous-finalist separation
and same-affiliation separation explicitly, including any exception.
