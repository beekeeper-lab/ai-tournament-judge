# Release Checklist

Work top to bottom. A failure stops the release; it does not become an advisory.

## 1. Clean checkout

- [ ] `git status --porcelain` is empty
- [ ] On a feature branch, not `main`
- [ ] `python3 -m atj rubric` prints the rubric you intend to ship

## 2. Automated verification

```bash
python3 -m pytest tests/ -q \
  && python3 -m atj release-check \
  && python3 -m atj demo check \
  && python3 -m atj event validate events/sample-mock-2026 \
  && python3 -m atj validate reports events/sample-mock-2026 \
  && python3 -m atj bracket verify tests/fixtures/bracket-20-team/bracket.json \
       --reproduce tests/fixtures/bracket-20-team/roster.json \
  && python3 tools/check_placeholders.py
```

- [ ] Every command exits 0
- [ ] The test count has not silently dropped
- [ ] `python3 -m atj demo build && git diff --exit-code` shows no change

## 3. Versioning

- [ ] `VERSION` is updated
- [ ] `pyproject.toml` mirrors it in PEP 440 form
- [ ] `CHANGELOG.md` has an entry for this version, including its limitations
- [ ] Any rubric or policy change carries its own version increment
- [ ] Any agent or skill change carries a bump in `framework/personas.md`, and
      `python3 -m atj personas` passes

## 4. Claude components

- [ ] `python3 -m atj release-check` reports `claude components PASS`
- [ ] Hooks tested against the installed Claude Code version
- [ ] `.claude/settings.json` parses and depends on nothing in
      `permissions.allow`, which Claude Code ignores until the workspace is
      trusted

## 5. Safety

- [ ] `python3 -m atj sandbox preflight` output recorded in the release notes
- [ ] If isolation is unavailable, the release states that executable evidence is
      unavailable and affected criteria must be `NE`
- [ ] Prompt-injection fixture tests pass
- [ ] No credential appears anywhere: `git grep -nE 'AKIA|-----BEGIN|sk-ant-'`

## 6. Publication boundary

- [ ] Every artifact in `events/*/public/` passes `atj validate publication`
- [ ] The ceremony view regenerates and contains no private shape
- [ ] Every dossier is `visibility: team` and approved

## 7. Documentation

- [ ] `README.md` commands all run as written
- [ ] `docs/implementation-detail.md` matches what was built
- [ ] `docs/final-audit.md` states PASS or PASS WITH ADVISORIES
- [ ] Known limitations are stated, not omitted

## 8. Package

```bash
pip install build && python3 -m build
```

- [ ] `dist/` contains a wheel and an sdist
- [ ] `pip install dist/*.whl` into a clean environment, then `atj release-check`
      from outside the repository

## 9. Tag

- [ ] Tag only after every box above is ticked
- [ ] Record the framework commit officials will pin events to
