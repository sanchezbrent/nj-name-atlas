# Primary layout — UI checkpoint 1

November 23, 2026. **Interactive local prototype; no production change.**

Latest revision: **UI-1.5**, a simpler finder and stronger selected-town outline; see the addenda below.
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

## UI-1.3 — next stories and clearer legend filtering

November 26, 2026. Two bounded presentation changes build on UI-1.2, keeping the
same checkpoint 23 pin and all previous UI/content recovery points unchanged.

- The single existing “Continue exploring” navigation moves directly after the
  narrative, before section tools and chronology. Its two original links become
  cards with arrows, a full-card hit area and a visible keyboard focus outline.
  Cards sit side by side on desktop and stack on phone. Original town choices,
  relationship labels, accessible names, URLs and handlers remain unchanged.
  No story synopsis, inferred relationship or new recommendation data is added.
- The exposed legend adds “Choose a category to filter towns.” A selected category
  has a checkmark, accent border and background wash, driven by the original
  `aria-pressed` state. The original reset button is relabeled “Clear origin
  filter,” remains beside the legend and still clears only the origin selection.
  The builder rejects an unexpected upstream reset label before applying this
  UI wording. The runtime still owns counts, selection and all filtering.

### Preservation and checks

Builder SHA-256:
`a002b758ec845658664c7ff21cba91822b77d80a1e8aef6af9b92a62002addb7`.
Overlay SHA-256:
`5f337604397a0fe00560d3c0aec484ca6d1f8dc5e3172f74605841a43020e16c`.

| Composed source | UI-1.3 generated Primary SHA-256 |
| --- | --- |
| Main base, unchanged | `e3cee9b83ed35ddd2efd5c4f84b2cdb4ba8794d1f3a1cd68fee6a0830e94c8bc` |
| Checkpoint 23, still pinned | `dc6a7c63d3bf2ac8410458882c7d4d444b7de4b32e79043aae6b80497b85e23a` |
| Checkpoint 24, independent rehearsal | `d91ca935dc70fea5ab455d52f1539f55c3e456da634b490b2b03a161d9d8f4bc` |

All original scripts/data and styles remain byte-identical, all 186 original IDs
are preserved, and no IDs beyond UI-1's three are introduced. Metadata/CSP and
the six unaffected output assets remain exact. No new JavaScript, dependency,
storage code or schema is added. Published assets, committed baselines, the pin,
the editorial branch and private authority remain unchanged.

All 22 Python tests and the required unchanged publishing-source checks pass.
Each of the three composed sources passes its own project/script checks,
16 fake-storage notebook assertions and statewide corpus checks (5,941 for each
editorial snapshot; 5,921 for main). The report-only audit on the branch's older
published source remains NEEDS_REVIEW with 21,724 heuristic candidates, unchanged;
this is not publication clearance or a statement of the editorial path's latest
review coverage.

Browser QA on checkpoint 23:

- At 320, 390, 768, 900, 1280 and 1600px, browse and reading views have no
  horizontal page overflow. All seven legend buttons remain visible with at
  least 44px height; desktop 1280/1600px retains one horizontal legend row.
- The two story links have at least 44px height at each sampled width. Their
  container starts 24px after the narrative, ahead of the 22 Cinnaminson chronology
  records. The complete chronology and optional alternate view remain available.
- Enter on Palmyra opens its story in reading view. The existing back link returns
  to Cinnaminson. Clicking the card's arrow area also follows the original link.
  Tab exposes the whole-card focus outline; no duplicate link is added.
- All seven filters select/reset with the original statewide counts. Enter can
  activate a category and the reset. Clearing the origin while Burlington County
  and a Cinnaminson search are set retains both, and hides the origin reset again.
- The new card and selected-legend appearances were inspected on phone in light
  and dark modes. Origin citation/return restores reference focus; the timeline
  jump focuses the original T1582 summary and Escape returns to browse.
- Existing browser notes were not inspected, migrated, edited or transmitted.
  Automated notebook checks use invented text and fake storage only.

Screenshots and validation receipts remain outside Git. The wider prior QA limits
still apply: no new full-corpus rendered/editorial review, assistive-technology
certification, native download/print acceptance or checkpoint 24 browser acceptance
is claimed. Young Explorers is unchanged byte-for-byte; its adapted summary was
last rendered in UI-1.2 and was not separately rechecked in this bounded revision.

### Stage and next checkpoint

UI-1.3 implementation, local/browser QA and immutable-source rehearsals are
complete; the interactive prototype is usable. The draft PR records this
checkpoint and CI status. Editorial/research/export work continues independently,
with no new editorial reviews or publication sign-offs from this revision.
Stop for design review. Remaining milestones are layout acceptance, deliberate
selection of a later completed editorial snapshot, a new combined checkpoint,
combined acceptance and separately authorized release/live readback. Provisional
active work remains 30–60 minutes for a bounded design revision or 45–90 minutes
for the selected-source integration rehearsal, excluding waits; no editorial or
publication completion ETA is asserted.

## UI-1.4 — browser annotation refinements

November 26, 2026. The three owner annotations are implemented on the separate
Primary prototype. The checkpoint 23 content pin and all earlier UI/editorial
recovery points remain unchanged.

- The masthead brand now reads exactly “New Jersey Name Atlas.”
- Legend color blocks stretch from the top to the bottom of their own label's
  text lines, including labels with different line counts in the same row.
  Category names, colors, counts and filtering remain owned by the original
  runtime. Below 400px, counts move below labels and padding is slightly reduced
  to prevent awkward word breaks in the exposed two-column phone legend.
- The extra “Find a place. Follow its names. Explore the stories behind them.”
  tagline is removed. The existing question and “Find your town” controls already
  introduce the experience. No historical narrative or editorial proposal changes.

### Preservation and verification

Builder SHA-256:
`32d1369019a1c517f231ded696f9b400ac5bf87566ac8ee01607a1cc3f669ce7`.
Overlay SHA-256:
`91a5bd8014f00175b83b2bf0a91facee00aee597f2279754255f1328119070c3`.

| Composed source | UI-1.4 generated Primary SHA-256 |
| --- | --- |
| Main base, unchanged | `78f61eb557c3346bdbed7f50bccc42860ffce3c9e103829ef5007e500fb73e9c` |
| Checkpoint 23, still pinned | `f53787c278900e79743078b5b33f250f762985623a40477a56405e0e8ebb83c8` |
| Checkpoint 24, independent rehearsal | `c3e687b9826620d9b6883566b35f12511414d524323fd06e6e0df9c63362e217` |

Each composition preserves all four original scripts/data blocks and original
styles byte-for-byte, all 186 existing IDs, metadata/CSP and the six unaffected
assets, including Young Explorers. No new IDs beyond UI-1's three, JavaScript,
dependencies, schema or storage code are introduced. Published assets, committed
baselines, the content pin and the editorial path remain untouched.

All 22 Python tests and required publishing-source project/script, notebook and
corpus checks pass. The final three compositions each pass their selected
source's project/script checks, 16 fake-storage notebook assertions and statewide
corpus checks: 5,941 assertions for each editorial snapshot, 5,921 for main.
The unchanged older publishing source's report-only public-copy audit still
reports NEEDS_REVIEW with 21,724 heuristic candidates. This is not publication
clearance or a statement of the active editorial path's latest coverage.

Browser QA on checkpoint 23 verifies the exact brand and absent tagline at 320,
390, 768, 900, 1280, 1430 and 1600px. All seven legend blocks match their own
label's top and bottom edges (zero measured difference at these widths). Every
button is at least 44px high and there is no horizontal page overflow. The legend
retains one row at 1280/1430/1600px and two columns on narrow phones. Whole-word
wrapping and selected/unselected light/dark appearances were visually inspected.
All seven filters select with their original counts (42, 153, 148, 115, 23, 28,
55), expose the existing reset and clear normally. Selected blocks still match
their labels. Enter opens Cinnaminson's reading view with its 22 chronology
records; Escape returns to browse. The preview is restored to Cinnaminson in
light appearance and the temporary viewport override is reset.

Screenshots, measured rectangles and preservation receipts remain outside Git.
Existing browser notes were not inspected or changed; notebook checks use fake
storage and invented text only. This bounded revision does not repeat the prior
full interaction pass, Young rendered check, checkpoint 24 browser acceptance,
printing/download checks or assistive-technology certification. Prior QA limits
and publication holds remain in force.

### Stage and remaining milestones

UI-1.4 implementation, targeted browser QA and immutable-source rehearsals are
complete. The draft PR records this checkpoint and its CI status. Stop for design
review; editorial, research and export work continue independently. Remaining
milestones are layout acceptance, deliberate selection of a later completed
editorial snapshot, a new combined integration checkpoint, combined acceptance
and separately authorized release/live readback. Provisional active work remains
30–60 minutes for a bounded design revision or 45–90 minutes for the selected-source
integration rehearsal, excluding waits; no editorial or publication ETA is asserted.

## UI-1.5 — search-led finder and clearer map selection

November 26, 2026. This implements the two approved design experiments on the
separate Primary prototype. The content pin and all earlier UI/content recovery
points remain unchanged.

- Search receives the main space. The existing county and town selects move,
  together with their original labels, into a visibly labeled fieldset under
  “More ways to explore.” They use two columns on desktop and stack on phone.
  The disclosure follows search/count in both DOM and visual order, ahead of
  active filter chips and matching results. No CSS ordering or duplicated fields.
- The original runtime already supplies four matching-name links plus access to
  the full matching index. These remain outside the disclosure, so searching and
  choosing a result do not require opening optional menus. Active filter chips
  and reset actions also stay visible when the menus are closed.
- The original selected-town halo grows from 4.5px to 6.5px, and its outline from
  1.5px to 2.5px using the existing theme-aware green accent. The existing
  non-scaling strokes keep that thickness through zoom. Category fill, geometry,
  callout placement, selection, panning and zoom logic remain unchanged.
- Moving the controls is bounded by new upstream label/group/order checks. A new
  negative boundary test proves a later control inserted into the moved span
  stops integration instead of being silently discarded. No runtime patch or
  focus-repair script is needed: the existing direct town-focus path belongs to
  the recent-town clear action inside the same open disclosure.

### Preservation and automated checks

Builder SHA-256:
`5a624c7529229d73e7028fd6ca833aac842eab15fcb127d77896a3dcde9ba984`.
Overlay SHA-256:
`e774298fd8e504da49b17c1cec894a0ab8d2fc48aeeeedd07ba503c735cad10c`.

| Composed source | UI-1.5 generated Primary SHA-256 |
| --- | --- |
| Main base, unchanged | `dc8b0b35374d4d3891f0a0bfe26eac36d1e4948c8d0edf3d0e78d6925e6cf6a9` |
| Checkpoint 23, still pinned | `832fd18d4b2f3492283e2a721809407260310df71b1b633a3e86a0c1ac843fb1` |
| Checkpoint 24, independent rehearsal | `1917fc7857242adbf794ee96d475933831fcfc2c57b6545791de84587f89c16b` |

All four original scripts/data blocks, original styles, metadata/CSP and 186
existing IDs are preserved in each composition. There are no new IDs beyond
UI-1's three. Only generated Primary HTML changes; the other six assets remain
exact. No new JavaScript, dependency, schema, storage code or publication setting.
Published files, committed baselines, the manifest and the editorial path remain
untouched.

All 23 Python tests pass, including the added upstream-control preservation test.
Required publishing-source checks pass. Each of the three final compositions
passes its own source's project/script checks, 16 fake-storage notebook assertions
and corpus checks (5,941 per editorial snapshot; 5,921 for main). The unchanged
older publishing source's report-only copy audit still reports NEEDS_REVIEW with
21,724 heuristic candidates; it grants no publication clearance and does not
describe the active editorial path's current review coverage.

### Browser checks on checkpoint 23

- Closed and open finder layouts have no horizontal page overflow at 320, 390,
  768, 900, 1280, 1430 and 1600px. Original menu labels are visible when open;
  both selects are 46px high. The exposed legend retains its earlier wrapping
  and targets of at least 44px. At 1430px, search is about 1,023px wide, compared
  with about 429px in UI-1.4. At 390px, Cinnaminson's reading action starts around
  495px, still in the first screen. The earlier 660px phone measurement belongs
  to UI-1.2, before the tagline removal; it is not a UI-1.4 comparison.
- With menus closed, Bottle Hill finds Madison through the existing historical
  match and its link works with Enter. Washington returns 43 matches, four
  immediate links and a working full-index action (12 entries on the first page).
  An unmatched query shows zero matches/disabled reading; clearing restores browse.
- The grouped county/town menus select Burlington (40 towns) and Palmyra, updating
  the map and preview together. With the menus closed, county view, actual map
  selection of Cinnaminson and zoom work. The selected outline remains 2.5px
  with non-scaling strokes. Origin-only reset retains Burlington and the typed
  query; visible filter chips identify both while optional menus remain closed.
- Keyboard Tab reaches the disclosure after search; Enter opens it, then Tab
  reaches county followed by town. Clearing the prototype's recent-town list
  focuses the town menu inside the still-open disclosure. Enter opens the existing reading view and
  Escape returns. Cinnaminson retains all 22 chronology records. Origin citation
  return restores its reference focus, and the timeline jump focuses an original
  event summary. A fresh town/event URL opens T1582 (the qualified 1655 record)
  with the alternate glance still closed.
- Phone finder, optional menus and selected-map light/dark appearances were
  inspected. Young Explorers remains byte-identical and opens Madison with its
  original adapted Bottle Hill summary and no prototype overlay. No existing
  browser notes were inspected, changed, migrated or transmitted.

Local screenshots, measurements and receipts stay outside Git. This is sampled
QA; the prior limits for printing, native downloads, assistive technology, all
tours, full-corpus rendered/editorial acceptance and checkpoint 24 rendered
acceptance continue. This revision does not repeat every earlier filter/card test.

### Stage and next milestone

UI-1.5 implementation, local/browser QA and immutable-source rehearsals are
complete; the updated preview is usable. The draft PR records the checkpoint and
CI status. Stop for design review. Editorial/research/export work stays on its
independent path, with no new copy reviews or publication sign-offs here. Remaining
milestones are layout acceptance, deliberate selection of a completed editorial
snapshot, a new combined integration checkpoint, combined acceptance and separately
authorized release/live readback. Provisional active work remains 30–60 minutes
for a bounded revision or 45–90 minutes for selected-source integration, excluding
waits; no editorial/publication completion ETA is asserted.
