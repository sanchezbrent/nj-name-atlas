# Public-copy separation — open remediation register

**Status: OPEN — not publication-cleared.** Identified November 19, 2026 from screenshots of the deployed Atlas. This is a process and presentation issue, **not** a request to change historical source authority. See [PUBLICATION_STANDARD.md](PUBLICATION_STANDARD.md).

Implementation tracking: [Issue #4](https://github.com/sanchezbrent/nj-name-atlas/issues/4).

## Copy proposals checkpoint — November 20, 2026

[Checkpoint 2](PUBLIC_COPY_CHECKPOINT_2.md) records agent text review of twelve
towns in both editions and 567 explicit proposed field edits, including repeated
timeline and citation contexts. The 552 towns outside this batch remain exact
C57 in each edition; the frozen source records remain unchanged. Historical
search aliases are restored in this batch. Source holds and owner approval remain
open; no human or rendered-browser sign-off is claimed.

| Current measure | Primary | Young Explorers |
| --- | ---: | ---: |
| Agent text reviews | 12 / 564 | 12 / 564 |
| Human/publication sign-offs | 0 / 564 | 0 / 564 |
| Strict scan candidates | 2,601 | 2,431 |

These are candidate/duplicate-inclusive scanner counts, not distinct errors or
reviewed towns. Strict CI remains blocked. The draft is not merged or deployed.

## Structural candidate checkpoint — November 19, 2026

See [checkpoint 1](PUBLIC_COPY_CHECKPOINT_1.md) for the complete change/evidence
map and limitations. The draft candidate removes the original-wording control,
original profile columns, private annotation fields and overwritten fallback
stores. All 1,128 C57 reader records remain exact; no source workbook is changed.
It is **not merged, deployed or publication-cleared**. The broader scan still
finds 2,736 primary and 2,560 Young candidates; strict mode blocks release.
All 1,128 town-edition rows are inventoried privately with contextual review and
human sign-off still pending. These machine counts do not constitute review.

## Confirmed examples to remediate

- An expandable **“Original research wording”** section is displayed to readers. Remove its visible control and prevent internal/original wording and raw research notes from being delivered in any public HTML, scripts or data payloads. Retain originals privately.
- A **“Name origin and town history”** section displays internal process language about AS-617, Whippanong PDF access, AI-generated HTML, and an uninspected 1720 order. Distinguish historically meaningful uncertainty from unverified source-access status; do not present uninspected documents as evidence or invent historical conclusions.

## Initial heuristic baseline (November 19, 2026)

The new scripts/audit_public_copy.py successfully decoded both embedded data payloads during GitHub Actions PR #3 (run 44611587856). It reported **21,724 candidate field-level matches**: 10,896 in primary and 10,828 in Young Explorers. These include repeated source-status and internal-ID strings within nested views/events and a UI label. **They are not 21,724 distinct errors, verified exposures or affected municipalities; some may be duplicate fields or false positives.** This confirms that a UI-only hide is insufficient, while the exact repair scope requires field-by-field review. The test is currently report-only and explicitly returns public_copy_certified=false even on a successful CI run.

## Required full-scope review (not yet performed)

| Stage | Requirement | Current status |
| --- | --- | --- |
| Source separation | Identify internal/original text fields in the authoring/export path; verify their private retention | Structural candidate and sealed retention verified; contextual exceptions open |
| Reader-facing UI | Remove original-research controls and process labels in both editions | Original control removed in draft; other copy and browser QA open |
| Published bundles | Remove internal-only content from the delivered HTML, JS, JSON, embeds and exported data, not just from the DOM | Private field owners/fallbacks removed in draft; remaining free-text candidates open |
| Statewide copy | Review all 564 municipality records in **each** edition, including deep panels and citation views; record exceptions/resolutions | Open |
| Evidence quality | Preserve verified references and real disputes; no fabricated source access or false certainty | Open |
| Test coverage | Automated candidate scan plus manual field-level review, browser/keyboard/mobile and existing source/notes/category guards | Open |
| Publication | Checked PR, successful CI, Pages deployment and independent live-host readback | Open |

**Important:** The most recent completed implementation validated 564 narratives and categories but did not certify public/private copy separation. Do not infer 1,128 records have been audited from prior corpus tests, screenshot samples or the merge/deployment of PR #2.

## Resolution protocol

For each affected municipality and edition, record: identity; reader-facing field; exact problematic text and source location **in private records**; public action (omit, recast or add verified historical context); source/citation effects; editor review; and a final rendered/payload check. Do not put private excerpts, sealed workbooks or audit packs into this public repository merely to document findings. This register tracks status and scope, not source text.

The governing editorial standard may be merged without changing live web assets; **do not mark this register closed or the live Atlas corrected until the publication changes, checks and readback actually happen.**
