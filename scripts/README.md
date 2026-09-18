# scripts/

The v0.1.0-alpha scripts have been replaced by the `atj` command line, which is
the single supported entry point for every deterministic operation.

They were retired rather than kept because each one held its own copy of official
facts and they could not see each other's output:

| Retired script | Why | Replacement |
|---|---|---|
| `calculate_scores.py` | Accepted caller-supplied `weights`, silently overriding the rubric; hard-coded the 0–5 scale | `atj score` |
| `build_bracket.py` | Duplicated the bye-policy list; emitted output that failed `bracket.schema.json`; broke previous-finalist separation at every size except 32 slots | `atj bracket build` |
| `validate_configuration.py` | Never parsed YAML; accepted an invalid `event_id`, an invalid bye policy and a wrong-typed judge list | `atj event validate` |
| `validate_reports.py` | Substring checks only; an empty report and a public artifact containing a credential both passed | `atj validate reports` |
| `initialize_event.py` | Left placeholders behind and ran no validation | `atj event init` |

The compatibility shims below accept the old invocations and forward to `atj`.
They print a deprecation notice and will be removed in v0.3.

Run `atj --help` for the full command set.
