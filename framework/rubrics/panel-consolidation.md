---
rubric_id: panel-consolidation
version: 1.0.0
source_rubric: submission-evaluation@1.0.0
judge_weighting: equal
minimum_panel: 2
aligned_max_range: 1
material_max_range: 2
outlier_distance: 2
---

# Panel Consolidation Policy

The consolidator is a neutral packager, not a fifth judge.

## Preconditions

Require all configured reports to reference the same team, commit, evidence package, and rubric version. Required fields and arithmetic must validate. Malformed reports return to the originating judge. Any `NE` pauses final scoring for more evidence or adjudication.

## Calculation

For each criterion, compute the arithmetic mean of valid raw judge scores, then apply the source-rubric weight. Preserve each source score, minimum, maximum, range, and confidence. The consolidated total is the sum of the consolidated weighted criterion points.

The consolidator may not replace or adjust an individual score. An adjudicator may add a documented resolution; the original reports remain unchanged.

## Agreement levels

These thresholds are declared in this file's front matter and read from there by
`atj.scoring`. The prose below restates them; the front matter defines them.

- **Aligned:** maximum minus minimum is at most `aligned_max_range`.
- **Material disagreement:** range is at most `material_max_range`.
- **Severe disagreement:** range exceeds `material_max_range`.
- **Possible outlier:** one judge is at least `outlier_distance` points from the median.

Material disagreement requires explanation. Severe disagreement, contradictory factual findings, or a possible outlier with result-changing impact requires adjudication.

## Evidence synthesis

Repeated wording is not independent confirmation. Consolidate the best supporting and contradicting evidence, identify whether disagreement arose from evidence selection, interpretation, persona emphasis, factual error, ambiguity, or missing evidence, and preserve justified minority concerns.

The report must contain an executive summary, deterministic score table, agreement analysis, confirmed strengths, confirmed weaknesses, unresolved questions, prioritized improvements, evidence index, and calculation audit.
