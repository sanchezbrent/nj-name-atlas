# Primary layout — UI checkpoint 1

November 23, 2026. **Interactive local prototype; no production change.**

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
