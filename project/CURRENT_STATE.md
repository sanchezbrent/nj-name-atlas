# Current project state

Public site: https://sanchezbrent.github.io/nj-name-atlas/

**Current remediation candidate:** [Copy proposals checkpoint 50](PUBLIC_COPY_CHECKPOINT_50.md).
Statewide agent text review remains 564/564 per edition across all 21 counties.
Checkpoint 50 adds 26 guarded main/discovery/activity copy proposals, preserving
all 14,655 earlier rows; cumulative total 14,681. The unchanged strict scanner now
passes with zero candidates in each edition. Human/publication sign-offs remain
zero and release remains BLOCKED. Targeted agent rendered QA covers eight towns
per edition on desktop/mobile; broader statewide rendered acceptance remains open.
All source holds continue. Stop after checkpoint 50. Next bounded checkpoint: broaden rendered QA beyond the eight sampled towns, using fresh browser contexts and no existing notes; preserve all source holds and zero human sign-offs. No merge/deploy.
Nothing merged or deployed; the live editions remain unchanged and not copy-cleared.
The implementation/browser statements below describe the earlier publication,
not fresh acceptance of this remediation candidate.

The November 19 candidate brings the completed C57 narratives and Review27
categories into the existing standalone atlas. C21 remains factual authority.
Both editions retain all 564 rewritten stories, summaries, journeys and sidebar
records. Young Explorers keeps its separate adaptations and original browser
note behavior. The category pass covers all 564 municipalities, with zero
pending and 179 guarded display mappings across the seven existing categories.

This implements retained work. It adds no historical decisions, source research,
workbook changes, category reviews or release of curated holds. Uncertain
explanations and dates remain qualified. Completion does not mean every literal
origin is solved or constitute universal reader acceptance.

## Verification and continuation

- project/asset-baseline.json pins the seven publishable files.
- project/content-baseline.json pins every municipality identity, both complete
  editorial corpora, factual source identities and final category counts.
- project/release-evidence.json records old public assets, Review27 source
  identities and the publication-label changes.
- project/browser-qa.json, when present, records current browser checks and limits.
- Run all checks in CONTRIBUTING.md before changing or publishing assets.

The research companion is sanchezbrent/nj-name-atlas-research. Private source
workbooks, audit files, checkpoints and recovery handoffs stay outside this
public tree. Do not recover later private work from an older public commit.
Keep original sealed components immutable and use a new working candidate.

## Outstanding public-copy gate — November 19, 2026

The currently published editions have an identified editorial/privacy-boundary defect: a reader-visible “Original research wording” disclosure and research-process language (including AS-617, uninspected source references and PDF/HTML handling) in town history. These are **not** reader-appropriate. Follow project/PUBLICATION_STANDARD.md and project/PUBLIC_COPY_REMEDIATION.md. The known defects still need remediation in both published HTML editions, plus a documented statewide 564-by-two review of visible text and shipped data. A policy-only change does not correct the live website; previous successful 564-story tests/CI and deployment do not constitute copy clearance.

## Current implementation stage

Candidate verified on update/statewide-narratives-review27. Both editions pass
local coverage, source, category and notebook checks. Current Chrome QA compares
30 full story samples per edition spanning all 21 counties, seven filters per
edition and all 564 computed map colors in light and dark themes. Desktop and
emulated 390px layouts have no horizontal overflow; sampled navigation, historical
search and reference controls pass. See browser-qa.json for scope and limits.

The embedded payloads use lossless shared-string packing and a compressed category
overlay. Both original expanded-data identities and the rewritten story identities
are checked. This keeps each standalone edition below the connector upload limit;
no story, source record, guard or publishing asset was removed. Browser checks of
the compacted files pass in both editions and themes.

Implementation and recorded local/browser QA are complete. The associated GitHub
pull request and Pages workflow establish merge and deployment status. Until
those records confirm completion, the remaining release milestones are required
checks, publication and live-host readback. Provisional release work: 10–20 active
minutes, excluding CI, access and review waits; not a release deadline.
