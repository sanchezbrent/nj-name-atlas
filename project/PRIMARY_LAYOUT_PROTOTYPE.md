# Primary layout — UI checkpoint 1

November 23, 2026. **Interactive local prototype; no production change.**

Latest revision: **UI-1.2**, earlier story entry and compact chronology; see the addenda below.
The original UI-1 evidence and hashes remain recorded as that checkpoint.

The interface and editorial paths remain separate. Editorial PR #5 owns copy,
source questions and its checkpoint sequence. This UI branch owns only the
prototype overlay, deterministic composition tool, boundary tests and its CI job.
The existing editorial branch, PR descriptions, issue #4 and private recovery
records were not written. Existing Young starter placement PR #6 remains separate.

## Recorded starting points and changes

- Production/main base: `8b5597b728731cd6df4ee470caaedbe7041e1ffb`.
- Preview content pin: completed public-copy checkpoint 23,
  `cbc5b9646a866ff03359f94877bc24a130b24d67`.
- Independent later-checkpoint rehearsal: completed public-copy checkpoint 24,
  `726a90d1ef1449f1913aac38db16d805946a71b2`.

The preview retains checkpoint 23 even though the editorial path advanced during
UI work. Both are draft editorial proposals; neither is publication-cleared.

The design puts search across the top, a map beside a selected-town preview, and
the existing reading view behind a prominent “Read the story” button. Additional
browsing tools remain available in a disclosure. The repeated map summary is
hidden while the identical qualified summary remains in the adjacent preview.
The original origin qualification stays visible. Full narratives, historical
names, dates, citations, source holds and category colors keep their original
renderer/guard logic. No new JavaScript or content rewriting is introduced.

All seven committed website assets and both asset/content baselines are unchanged
from main. The prototype is generated outside Git. It is not copied into docs/,
attached as a CI artifact, hosted publicly, merged or deployed.

## Exact composition evidence

Final overlay SHA-256:
`d82c22428ac3082c85512edb659543c504d122b8302e5f5e41f8f9b0ae635a6d`.

Final builder SHA-256:
`c4a6f2d33d1168f72730183117184ae86a5f43da25d59c49cd45543849f4df08`.

| Committed source | Primary before SHA-256 | Generated Primary SHA-256 |
| --- | --- | --- |
| Main base | `56d590582a0d67a08e6a9d0f071a4f88ecd1b68e4f43e55d50fbb1b0e07c2ef2` | `216e80aabf1448bcef079fa19bd7486d919ae9cee403e670ee98ca799f6d2d8e` |
| Editorial checkpoint 23 | `214ec37440200b149700208985d7b8fbb11feb07983dd26806247322c747633c` | `5e0208241e706390deb5a14a0bfb96a0128ea7467c72437166ed676edb395532` |
| Editorial checkpoint 24 | `9a03dfa9b827ae658102a2d019f24b664b1f4025ec24dedb85c5d7ee8dcc39d4` | `3ac49d6a0d015753cb998f967003540fe998a5fb4cd2602f717f6659411fccf6` |

Each composition preserves all four original script blocks byte-for-byte, including
the full embedded data, category overlay, source/copy guards and all runtime code.
All original style blocks and 186 existing DOM IDs are preserved. CSP and metadata
are exact. Three prototype IDs are added. Six other generated website assets,
including Young Explorers, match the selected source commit byte-for-byte.
The local receipt records the individual script/asset hashes and checks.

The selected commit's own project/schema/source checks, six script syntax checks,
16 isolated notebook assertions and statewide corpus checks pass against each
composed preview: 5,921 runtime assertions for the main base and 5,941 for each
editorial checkpoint. Only a disposable verification fixture receives generated
asset hashes; no committed baseline is changed. These are integrity results, not
copy/publication acceptance.

All 22 branch Python tests pass, including 13 new boundary tests covering changed
runtime/content preservation, upstream UI-label/DOM changes, duplicate IDs,
wrong-edition/repeated application, script introduction and unsafe outputs.
The production-source project, notebook and corpus checks also pass unchanged.
The added CI job composes and verifies all three source snapshots independently;
the existing quality workflow and its safeguards are unchanged. Concurrency is
scoped to this UI PR, so it does not cancel editorial PR checks.

## Browser QA performed

In-app browser against checkpoint 23 on a new loopback origin:

- Browse layout at 320, 390, 768, 900, 1280 and 1600px: no horizontal page overflow;
  top search, two desktop panels and stacked smaller-screen panels work.
- Cinnaminson's qualified summary and disputed-origin note remain visible. Reading
  view opens the full narrative; search/map hide and return correctly. Phone
  reading has no horizontal overflow and story-navigation targets are at least
  44px tall.
- Actual map selection switches Madison to Cinnaminson; zoom changes geometry;
  county/state controls, all seven origin filters, town index and “More ways to
  explore” remain usable. The map retains all 564 municipality paths.
- Historical-name search for Bottle Hill returns Madison. Empty search results
  disable reading and show the existing recovery state; clearing restores towns.
- Origin citation opens references. Its return link focuses
  `atlas-note-0308-1-ref`. A historical-name link opens
  `#town=0308&event=T1582` and expands its event. The name-journey dialog opens and
  closes. Escape returns from reading view to the reading control.
- Light/dark appearance retains readable controls and map/category meaning.
  No browser errors were recorded during these sampled interactions.
- The unchanged Young edition opens Madison's starter lesson and references.
  Existing notes were not inspected, migrated, changed or transmitted; notebook
  assertions use fake storage and invented text only.
- Both edition URLs return HTTP 200. Receipt, traversal and Git-config paths
  return HTTP 404 from the loopback server.

Limits: browser sampling does not certify all 564 stories, every device, native
downloads, printing, assistive-technology behavior or all tours. Checkpoint 24 has
composition/runtime verification, not a new full rendered acceptance pass. The
strict-copy gate and all source/editorial holds remain open. Future source/runtime
changes require fresh composition and browser QA even when the DOM contract passes.

## Integration risks and ownership

| Risk | Required handling |
| --- | --- |
| Older prototype HTML overwrites newer editorial copy | Never copy generated HTML back. Compose from an explicitly selected full content commit; compare every original script/data block. |
| Shared HTML/baseline merge conflicts | UI-1 edits neither. Future integration uses a new branch and a new checkpoint; generate proposed asset hashes from the combined result. Never accept an older whole edition or baseline to resolve a conflict. |
| Editorial advances mid-batch | Keep the preview pin stable. Rehearse later completed commits read-only in separate outputs; no implicit pin updates or editorial pushes. |
| Upstream UI or runtime changes | Stop on altered labels/structure/IDs/scripts contract; reconcile and repeat source-specific runtime plus browser checks. A passing structural check alone is insufficient. |
| Accidental public exposure or notes access | Local-only output outside Git, exact serving allowlist, fresh origin and no storage code. No generated pages in public commits or CI artifacts. |
| Prototype approval mistaken for release clearance | Keep UI, editorial and publication acceptance separate. Preserve strict scanning and source holds; require existing publication sign-off and separately authorized release/readback. |

The executable rehearsal and detailed integration procedure are in
[the prototype guide](../prototypes/primary-layout/README.md). Existing checkpoints
remain immutable recovery points. The eventual combined checkpoint must identify
the exact content commit, accepted UI commit, preservation receipt and acceptance
scope. No workbook or private authority seal is changed for this UI task.

## Stage, next checkpoint and ETA

UI-1 implementation, local QA and source-specific integration rehearsals are
complete. GitHub review/CI status is recorded by the dedicated draft PR. The
usable deliverable is the local interactive prototype plus reproducible tooling.
Research, export and editorial progress remain on their existing path; this UI
checkpoint adds no town reviews or publication sign-offs.

Stop at UI-1 for design review. Remaining milestones are a bounded UI revision if
requested, selection of a completed editorial snapshot for integration, a new
combined checkpoint, combined acceptance and separately authorized release/live
readback. Provisional active work: 30–60 minutes for a bounded UI revision and
45–90 minutes for a source-specific integration rehearsal, excluding waits.
No editorial completion or publication ETA is asserted.

The [publication standard](PUBLICATION_STANDARD.md) and
[open copy-remediation register](PUBLIC_COPY_REMEDIATION.md) continue to govern.

## UI-1.1 — exposed horizontal legend

November 23, 2026. The origin legend now occupies the full width below search.
All seven categories share one row at 1280px and wrap into two columns on narrow
screens. The overlay explicitly overrides the inherited column direction.
The legend is a labeled section rather than a disclosure, so the original
runtime's phone-startup disclosure reset cannot hide it. Existing IDs, category
buttons, counts, labels and filtering handlers remain in place. The original
four script blocks and all embedded content remain byte-identical.

Content pin remains checkpoint 23. The builder SHA-256 is
`36374493051188c9698062cb71ebf8628af05d98905880ef79292048e525f76c`;
overlay SHA-256 is
`a74250adc47681bcf7063a84b62dc91e0ceb8337f11b2e919cfb70f793e3318d`.
Generated Primary SHA-256 is
`7141e86ffd9301fedcceec73074f161406491acd2e125a3eb8c0b3a5d1646f4a`;
its source remains
`214ec37440200b149700208985d7b8fbb11feb07983dd26806247322c747633c`.

All 22 Python tests and the composed checkpoint's own project checks, 16 fake-note
assertions and 5,941 runtime assertions pass. Browser checks confirm seven entries
on one desktop row, visible legend after fresh phone loads at 390px and 320px,
two-column phone wrapping, no horizontal page overflow, working filter/reset
and keyboard movement between category buttons. No existing notes were accessed.
The existing GitHub integration workflow will verify main and both editorial pins
on this revision. Published files, committed baselines and editorial work remain
unchanged. The wider UI-1 browser/download/printing limits still apply.

This bounded revision is complete and the updated preview is usable now. Next
milestone is design review; the later integration milestone and provisional
45–90 active-minute rehearsal estimate remain unchanged, excluding waits.

## UI-1.2 — earlier story entry and one default chronology

November 26, 2026. This implements the two proposals recorded in
[the design review](https://github.com/sanchezbrent/nj-name-atlas/pull/7#issuecomment-7194282229).
The content pin, its status, the original UI-1/UI-1.1 evidence and both editorial
recovery points remain unchanged.

### Presentation changes and integration decision

- The existing story card moves before the legend/map in DOM and phone order.
  Desktop uses the same card beside the map. Its original reading button now
  follows the town heading; no story markup or live selection state is cloned.
- The masthead and map controls use less space. The preview keeps the original
  complete origin summary, qualification and citation, with fewer boxed labels.
  Related-town links remain in reading view. All seven legend categories remain
  exposed: one row at 1280/1600px, wrapping on smaller screens. On phone the legend
  immediately precedes the map panel.
- The narrative precedes section navigation; the five existing actions become
  quieter text controls with 44px minimum targets. The default chronology retains
  every source record and qualified date, using compact rows with each original
  event's native expansion. The alternate “Names at a glance” grid follows it in
  an initially closed native disclosure. Its complete contents remain available.
- An extra outer accordion around all event records was rejected during
  implementation: the unchanged runtime opens/focuses individual event summaries
  directly and does not open a newly added ancestor. Keeping those entries in the
  visible chronology preserves event routes, timeline jumps and citation returns
  without new JavaScript or an asynchronous focus repair. No curated key-moment
  selection, editorial rewrite, record deletion or sorting was introduced.

### Preservation and automated verification

Builder SHA-256:
`25d03dba6643128b777b7e802b3298ac9df3e63d907ec9d10ce198bb765b0c2b`.
Overlay SHA-256:
`b7dc5df1e6800a44f7615f53cdfee9e3411e3e7533eeec8f78b51b40fd77a7b1`.

| Composed source | Source Primary SHA-256 | UI-1.2 generated Primary SHA-256 |
| --- | --- | --- |
| Main base | `56d590582a0d67a08e6a9d0f071a4f88ecd1b68e4f43e55d50fbb1b0e07c2ef2` | `eacde76c20e150e4c9d3735adacd1c70b660f7799df4ffaf333e2e4667646928` |
| Checkpoint 23, still pinned | `214ec37440200b149700208985d7b8fbb11feb07983dd26806247322c747633c` | `803b309b35c576a4eae00dd970667ca184578c6614fd9de3d51468776f03366d` |
| Checkpoint 24, separate rehearsal | `9a03dfa9b827ae658102a2d019f24b664b1f4025ec24dedb85c5d7ee8dcc39d4` | `3c51b226dd73630f4e5c6f8421aa105b805bf4e76b892d5ddfc46531e7ce2ec4` |

All four original scripts/data blocks, original style blocks, metadata/CSP and 186
existing IDs remain exact/preserved. No IDs are added beyond UI-1's three. Six
other output assets, including Young Explorers, remain byte-identical to their
selected source. The seven committed publishing assets, content/asset baselines,
checkpoint manifest and editorial branch were not changed.

All 22 Python tests pass. Each composed source passes its own project/script,
16 isolated notebook and corpus checks: 5,941 assertions for each editorial
snapshot, 5,921 for main. Required checks against this branch's unchanged published
source also pass. The report-only public-copy scan still reports NEEDS_REVIEW
(21,724 heuristic candidates on this branch's older published source); it grants
no clearance and does not describe new UI defects or the editorial path's latest
coverage. Existing publication holds remain open.

### Browser checks performed on checkpoint 23

- No horizontal page overflow at 320, 390, 768, 900, 1280 or 1600px. The single
  story precedes the map in DOM order; desktop places it alongside the map.
- At 390 × 844, Cinnaminson's heading begins around 574px and its reading action
  around 660px, compared with roughly 1,964px and 1,824px in UI-1.1. Both are now
  in the first screen. The full origin explanation remains below the action.
- All seven exposed legend filters return the original counts and reset correctly;
  Burlington county view, actual map selection of Cinnaminson, historical search
  for Bottle Hill/Madison, the filtered town index, empty-search recovery and the
  disabled reading control in the empty state work.
- Enter opens reading view. Narrative precedes the quieter section links.
  Cinnaminson retains 22 chronology records and Madison eight. The alternate
  glance disclosure starts closed and opens normally.
- Origin note and event-source return links restore focus to their original
  reference anchors. A glance link opens/focuses T1582; a fresh
  `#town=0308&event=T1582` URL opens the record with the alternate glance still
  closed. Timeline, full-history, name-journey dialog and Escape/return controls
  work. The record chronology has no new hidden ancestor.
- Light/dark phone appearance remains readable. Young Explorers still opens
  Madison with its original adapted summary. Existing browser notes were not
  inspected or changed; notebook assertions use fake storage only.

Local screenshots and validation receipts are stored outside Git. This is sampled
browser QA, not assistive-technology certification, every-device coverage or a
564-story editorial review. Printing, downloads, all tours and checkpoint 24's
rendered acceptance were not retested in this revision. The original integration
risks and release boundaries continue to apply.

### Stage and remaining milestones

UI-1.2 implementation, local QA and immutable-source rehearsals are complete;
the interactive preview is usable. The draft PR records this checkpoint and its
CI status. Research, workbook/export authority and ongoing editorial work remain
on their separate path, with no new content reviews or sign-offs from this UI
revision. Stop here for design review. Remaining milestones are acceptance of the
layout, deliberate selection of a later completed editorial checkpoint, a new
combined integration checkpoint and separately authorized release/live readback.
Provisional active work after review remains 30–60 minutes for a bounded revision
and 45–90 minutes for a selected-source integration rehearsal, excluding waits;
no editorial or publication completion ETA is asserted.
