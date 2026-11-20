# Public-copy remediation — checkpoint 6

November 20, 2026. **Draft proposals; publication BLOCKED.**
Continues [issue #4](https://github.com/sanchezbrent/nj-name-atlas/issues/4) and
[PR #5](https://github.com/sanchezbrent/nj-name-atlas/pull/5).
[Checkpoint 5](PUBLIC_COPY_CHECKPOINT_5.md) remains complete and preserved.

## Completed twelve-town scope

Both editions received agent text review for Andover Borough, Andover Township,
Branchville Borough, Byram Township, Frankford Township, Franklin Borough,
Fredon Township, Green Township, Hamburg Borough, Hampton Township, Hardyston
Township and Hopatcong Borough. Complete summaries, stories, journeys, sidebars,
timeline text, citation descriptions, historical search aliases and embedded
summary fallbacks were examined. Separate Young adaptations and resulting
proposals were read. This is not human acceptance or original-source verification.

The batch adds 380 guarded field proposals: 191 primary and 189 Young, for 2,253
cumulative proposals. All 1,873 earlier rows remain unchanged. Repeated contexts
are included in those counts; they are not counts of errors.

Agent text review is 51/564 per edition: all 39 Morris County towns and twelve
of Sussex County’s 24 towns. There are 513 towns per edition remaining.
Human/publication sign-offs remain zero.

## Preservation and implementation

- C21 factual authority, sealed C57 originals and the content-baseline seals are
  unchanged. Fresh byte hashes match the retained C21 workbooks and C57 payloads.
  No workbook was interpreted, recalculated or written.
- All 513 towns outside the cumulative scope retain their C57 reader fields
  exactly. There are 515 total exact C57 reader records per edition. All prior
  39 reviewed reader/view records and all 552 views outside this new batch are
  unchanged from checkpoint 5.
- Event IDs, years, municipality associations, source IDs/URLs, citation
  bindings, numeric date sequences and date holds are unchanged. All 179
  Review27 mappings and discovery eligibility remain unchanged: ten active
  stops, eleven connections and 36 held items per edition.
- Conflicting postal dates, Franklin’s competing namesakes and election dates,
  Hardyston’s provisional tax spellings and Hopatcong’s attributed meanings
  remain qualified. No original-source inspection or historical adjudication
  is claimed. All source questions and previous holds continue privately.
- Frankford’s edited summary is also explicitly replaced in its embedded
  profile fallback. That field requires a current before-text hash and must
  match the reviewed editorial preview. Regression tests reject stale,
  mismatched and protected-source edits. Earlier profile/view records are exact.
- Only the two edition files changed within the seven-file website allowlist;
  the other five assets remain exact. Original research, exact before text,
  process notes and continuation records remain private.

## Checks and remaining gates

| Current measure | Primary | Young Explorers |
| --- | ---: | ---: |
| Agent text reviews | 51 / 564 | 51 / 564 |
| Human/publication sign-offs | 0 / 564 | 0 / 564 |
| Cumulative proposed fields | 1,138 | 1,115 |
| Strict scan candidates | 2,191 | 2,021 |

Required CLI project/source/schema checks, all 21 Python tests, six actual
script syntax checks, 16 notebook assertions and 5,941 statewide runtime
assertions pass. Notebook checks use invented content and isolated storage only.
No existing browser notes were accessed. Actual discovery guards retain their
previous eligibility and holds.

Strict scanning exits 1 and continues to block release. Counts include duplicate
guards and possible false positives; they are not town counts or clearance.
The new town contexts trigger no heuristic patterns, and an additional contextual
check found no residual process-language matches. Scanner rules, required CI
gates and source protections were not weakened.

Human acceptance, source questions and rendered/mobile/keyboard/search/source
and deep-panel QA remain open. No fresh rendered or live-host acceptance is
claimed. Live Pages is unchanged. Nothing is merged or deployed.

## Standing scope and stopping point

The owner approved this twelve-town batch and gave standing authorization for
agent-selected public-copy remediation batches of at most twelve municipalities
across both editions. Save both PRs and continuation records, update issue #4
and stop at each checkpoint. New historical research or adjudication, authority
workbook changes, deferred archive transfers, merge and deployment remain outside
this authorization. Older handoffs requiring renewed town selection describe
the superseded scope rule.

Stopped after these twelve towns. The remaining twelve Sussex towns are queued
privately but unstarted. Remaining milestones are 513 town pairs, source
questions/holds, human acceptance, full rendered cross-edition QA, passing strict
CI and the separately authorized release process with actual-host readback.

Allow provisionally 45–90 active minutes for the next twelve-town checkpoint,
excluding review, source-access and execution waits. The draft is reviewable now;
statewide publication clearance has no reliable ETA.
