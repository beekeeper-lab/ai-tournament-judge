# Recovery and Resume

`events/<event>/status.md` is the recovery ledger. Every completed unit records its input identity, output paths, audit result, and timestamp. A unit is complete only when its artifacts exist and its audit passes.

After interruption:

1. Read status and run validators.
2. Compare recorded inputs with current event, framework, commit, and evidence identities.
3. Resume the first incomplete unit.
4. Repair partial output rather than treating it as final.
5. Do not rerun an audited unit unless its inputs changed or a human invalidated it.

If inputs changed, mark dependent work stale. A changed evidence package invalidates its judgments, consolidation, dependent matchups, dossier, and potentially bracket qualification. Preserve old artifacts with versioned names rather than overwriting the audit trail.
