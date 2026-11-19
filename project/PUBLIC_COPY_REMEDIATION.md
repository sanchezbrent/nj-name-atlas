# Public-copy separation — open remediation register

**Status: OPEN — not publication-cleared.** Identified November 19, 2026 from screenshots of the deployed Atlas. This is a process and presentation issue, **not** a request to change historical source authority. See [PUBLICATION_STANDARD.md](PUBLICATION_STANDARD.md).

## Confirmed examples to remediate

- An expandable **“Original research wording”** section is displayed to readers. Remove its visible control and prevent internal/original wording and raw research notes from being delivered in any public HTML, scripts or data payloads. Retain originals privately.
- A **“Name origin and town history”** section displays internal process language about AS-617, Whippanong PDF access, AI-generated HTML, and an uninspected 1720 order. Distinguish historically meaningful uncertainty from unverified source-access status; do not present uninspected documents as evidence or invent historical conclusions.

## Required full-scope review (not yet performed)

| Stage | Requirement | Current status |
| --- | --- | --- |
| Source separation | Identify internal/original text fields in the authoring/export path; verify their private retention | Open |
| Reader-facing UI | Remove original-research controls and process labels in both editions | Open |
| Published bundles | Remove internal-only content from the delivered HTML, JS, JSON, embeds and exported data, not just from the DOM | Open |
| Statewide copy | Review all 564 municipality records in **each** edition, including deep panels and citation views; record exceptions/resolutions | Open |
| Evidence quality | Preserve verified references and real disputes; no fabricated source access or false certainty | Open |
| Test coverage | Automated candidate scan plus manual field-level review, browser/keyboard/mobile and existing source/notes/category guards | Open |
| Publication | Checked PR, successful CI, Pages deployment and independent live-host readback | Open |

**Important:** The most recent completed implementation validated 564 narratives and categories but did not certify public/private copy separation. Do not infer 1,128 records have been audited from prior corpus tests, screenshot samples or the merge/deployment of PR #2.

## Resolution protocol

For each affected municipality and edition, record: identity; reader-facing field; exact problematic text and source location **in private records**; public action (omit, recast or add verified historical context); source/citation effects; editor review; and a final rendered/payload check. Do not put private excerpts, sealed workbooks or audit packs into this public repository merely to document findings. This register tracks status and scope, not source text.

The governing editorial standard may be merged without changing live web assets; **do not mark this register closed or the live Atlas corrected until the publication changes, checks and readback actually happen.**
