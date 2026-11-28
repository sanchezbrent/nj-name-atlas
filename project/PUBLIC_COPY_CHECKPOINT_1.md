# Public-copy remediation — structural checkpoint 1

**Candidate only. Publication BLOCKED. Live Pages has not been changed.**
November 19, 2026. Tracks [issue #4](https://github.com/sanchezbrent/nj-name-atlas/issues/4).

## Source and preservation

Inputs are the exact two website assets at policy main
`8b5597b728731cd6df4ee470caaedbe7041e1ffb`, also present unchanged in the retained
`25916f0d564577a8f9f3d791b968396a87bf9f9f` checkout. That checkout is read only.
Both C21 native workbook SHA256 values match the sealed C57 authority record.
Every C57 reader record was compared directly with the sealed C57 projections:
564/564 exact in each edition after excluding only source-view guard bindings.
No historical or editorial correction, workbook write, recalculation, category
decision, source-access claim or source inspection was made.

The immutable `content-baseline.json` remains the original C21/C57/Review27 seal.
`public-copy-baseline.json` separately pins this derivative and its before/after
asset identities. `asset-baseline.json` pins candidate bytes, not publication
approval. A private retention receipt records exact source locations and hashes.

## Implemented in the candidate

- Remove the original-wording disclosure and its original profile-field owners.
- Export profile, event and citation objects through explicit field allowlists.
  Private profile prose, cautions, event notes, evidence grades, row numbers and
  source contribution/limitation annotations are omitted from those objects and
  their serialized comparison guards.
- Remove the overwritten legacy profiles/events/sources/workbook dataset. Retain
  map geometry, county counts and boundary retrieval date. Remove retired
  replacement dictionaries, unused old story hooks and unreachable old journeys.
- Preserve all 4,919 town-associated event records and 4,117 town-associated
  citations per edition (shared records repeat across towns). Preserve every
  existing C57 reader string and all 179 Review27 decisions. Rebind source-view,
  date, category and three Young activity guards to the public projection.
- Replace discovery's raw source-field comparison text with source-value hashes;
  retain existing hold dispositions and public discovery text. These surfaces
  still need contextual review.
- Expand the scanner to inspect both embedded datasets, the compressed map
  fallback, compressed category overlay, discovery, hooks, retired literal
  stores and Young activity data. CI now runs strict scanning as a release block.

This is structural separation, not a statement that all remaining free text is
appropriate. Original/process language still occurs within retained event
descriptions, source citation strings and some C57 passages. Those require
explicit contextual treatment; this checkpoint does not silently edit C57.

## Scope and open gates

| Measure | Primary | Young Explorers |
| --- | ---: | ---: |
| Town records inventoried by code | 564 | 564 |
| C57 reader records preserved exactly | 564 | 564 |
| Towns contextually signed off | 0 | 0 |
| Enhanced scanner candidates before projection | 18,796 | 18,621 |
| Enhanced scanner candidates after projection | 2,736 | 2,560 |

Candidate counts include repeated guards and false-positive candidates. They are
not distinct errors, affected-town counts or manual review counts. The new
37,417 baseline is broader than the policy PR's older 21,724 baseline.

The private ledger contains 1,128 explicit **NOT STARTED / not signed off** rows,
field paths, exact candidate excerpts and pending evidence/resolution fields.
No per-town internal excerpts are placed in this public repository.

## Verification actually performed

- Asset allowlist, payload identities, private-field schema and frozen C57/source
  bindings pass; 11 Python tests pass, including hidden compressed-store and
  identity-corruption cases.
- Six actual inline classic scripts pass JavaScript parsing.
- Original notebook controller: 16 assertions with fake storage/invented text.
- Actual statewide runtime: 5,941 assertions across both editions, including
  564 profiles each, all 179 mappings, stale narratives/categories, public-view
  mutations, date-context rejection and the three original Young activities.
- Before/after execution of discovery guards preserves all ten currently active
  tour stops and eleven active connections in each edition, including holds.
- Strict scanner exits **1**, as required with unresolved candidates.
- Direct Python CLI syntax checking could not locate a Node executable locally.
  JavaScript syntax and modules were exercised in the available JavaScript
  runtime with the required web APIs. GitHub Actions runs the ordinary commands.
- Browser preview is **not run**: the local sandbox forbids binding the loopback
  server, and browser security policy blocks local-file URLs. No permission or
  browser security setting was changed. Earlier browser receipts are not fresh
  QA for this candidate. Mobile, keyboard, rendered deep panels and live-host
  readback remain open.

## Continue

The next checkpoint is a bounded contextual review of at most twelve towns in
both editions, starting with the reported Morris County example. Compare actual
source evidence; make explicit public-copy corrections only where justified;
retain exact before/after text privately. Rebuild from immutable inputs plus
reviewed corrections, update the private ledger and aggregate register, and
rerun checks. All remaining towns, cross-edition browser QA, human sign-off,
passing strict CI, merge, Pages deployment and actual-host inspection remain.

Provisional next checkpoint: 45–90 active minutes, excluding source-access,
review and execution waits. The draft structural candidate is available now.
An ETA for a publication-cleared statewide edition is not yet established.
