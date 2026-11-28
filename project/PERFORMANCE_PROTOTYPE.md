# Runtime performance — checkpoint PERF-1

Stage: implementation and local verification complete. The separate draft PR
records GitHub checks and review. This is a local performance prototype, not a publishing change.
Editorial/source work continues independently. No historical decisions or wording
changes were made. The existing [publication standard](PUBLICATION_STANDARD.md)
and [editorial remediation status](PUBLIC_COPY_REMEDIATION.md) remain in force.

## Scope and separation

- Branch: `prototype/runtime-performance`, based on UI-1.8
  `29505af1e4db824403eaef3b03786e71f128d3e4`; draft PR targets the UI branch in #7.
- Main readback before work: `8b5597b728731cd6df4ee470caaedbe7041e1ffb`.
- Default frozen content: checkpoint 23,
  `cbc5b9646a866ff03359f94877bc24a130b24d67`; its pin is unchanged.
- Rehearsal: checkpoint 24, `726a90d1ef1449f1913aac38db16d805946a71b2`.
- `docs/`, publishing/content baselines, PR #5, PR #7's branch and private
  authority are untouched. No workbook, browser notes, storage migration,
  dependency, network request, tracking or hosting change.
- Each source is validated against its own immutable asset baseline. Generated
  pages and screenshots stay outside Git; no upload/deployment/artifact step.

## Implementation

The original renderer discarded/recreated 564 municipality paths and their
listeners on every redraw. Its title expression called `storyHookFor` twice for
each valid preview, invoking full-record canonical validation each time. It also
serialized unchanged geography while filtering or choosing a town.

The new renderer retains the base-map DOM and validates each title once when its
node is created. It keeps the original source validators themselves unchanged;
hover, story and corpus checks still call those original functions. Records in a
loaded document have no editing API. No cache crosses a document or source
version. Adding live content mutation later requires explicit invalidation.

Each render derives current filter and relationship sets. Fixed handlers consult
those sets, titles update their relationship suffixes, classes update only when
different, and at most two DOM moves preserve selected-last drawing order.
Geometry is keyed by width, height, county and final projection scale/translation
after the original selection-reveal adjustment. Panning still uses the original
projection/path calculations; the smaller label/selection/connection layers still
redraw through their original functions.

The town menu reuses its options when matching codes and county are unchanged.
Selected value, disabled state and search response remain synchronous. No input
debounce, mirrored selected town or replacement routing is introduced.

The performance builder reverses four exact patches and requires full input-byte
recovery. It rejects patch drift, reapplication, script/container changes, writes
inside any checkout, unmanaged outputs, mixed preview ownership and symlinks.
The layout builder only gains an optional receipt filename for reusing its
selected-checkpoint verifier; its default UI behavior and preservation contract
are unchanged. Both original data/library script blocks and appearance script
remain exact. Original data/guard bytes inside the modified runtime remain exact.

## Measurements and checks

Final local Node v24.22.3 comparison against unchanged main-source data used
seven warmed samples per case. Medians cover the original base-map block versus
the retained renderer using actual D3/data/guards and a minimal SVG model:

| Edition / base-map operation | Original | PERF-1 |
| --- | ---: | ---: |
| Primary, unchanged viewport with filter changes | 157.33 ms | 0.15 ms |
| Primary, changing pan | 158.26 ms | 45.58 ms |
| Young Explorers, unchanged viewport with filter changes | 157.28 ms | 0.13 ms |
| Young Explorers, changing pan | 156.77 ms | 45.62 ms |

These are component JavaScript/geometry measurements, not browser frame rates or
whole-application latency. Timings vary with load and are not CI thresholds. The
remaining roughly 45 ms of pan geometry motivates the next checkpoint. Labels,
selection, connected outlines, browser layout and paint are excluded.

Across seven warmed pan operations, the original block created 8,085 base-map
nodes, 11,844 listeners and made 7,896 guarded-title calls; PERF-1 made zero new
allocations/calls in those three categories. It still calculated 4,144 paths.
Unchanged-viewport operations calculated zero paths after warmup. The existing
small overlay layers may still allocate nodes; this is not a whole-map zero-
allocation claim.

Local verification:

- 37 Python tests pass, including nine new runtime/output boundary tests.
- 92 renderer/dropdown assertions pass for both editions: exact paths,
  drawing order, titles, classes, colors, selection, changed filters/connections,
  empty matches, pan/zoom, preserved nodes and current event handlers.
- Existing 40 navigation assertions pass with invented controls; no live notes.
- Three generated compositions pass their selected commit's own project/script
  checks, 16 fake-storage notebook assertions and corpus checks: 5,941 assertions
  for checkpoint 23 and checkpoint 24, 5,921 for main. Content identities and all
  564 municipality stories/categories per edition remain checked.
- Checkpoint 23 and 24 include UI-1.8 before the runtime patches; main-source
  rehearsal retains the original layouts to exercise independent composition.
- Original source/public-copy report remains report-only, with release status
  unchanged. No editorial certification is inferred from these runtime tests.

Sampled browser QA on the checkpoint-23 combined preview:

- Primary: Cinnaminson, Newark search, no-result search/reset, statewide and
  county scopes, native municipality click, zoom, native drag without town
  activation, reading/stepping/return and retained zoom. Event deep link
  `#town=0308&event=T1582` opens the original record in reading view.
- Primary at 390x844: all 564 municipality paths remain present, origin filter
  yields 42 matches/522 dimmed towns, dark appearance works, no horizontal
  overflow. Desktop check at 1280x720 also has no overflow.
- Young Explorers: Madison initial route, Palmyra town-menu selection, Burlington
  scope, zoom, 390x844 reflow and original reading action. No notebook opened or
  existing note inspected/changed. Both sampled tabs report no console errors.
- Native assistive technology, all tours/history/source combinations, print and
  downloads, whole-browser latency and checkpoint-24 rendered acceptance were
  not certified by these sampled checks.

Reproduction identities for the final local candidate:

- Performance builder SHA-256:
  `ae4efef38d206e0e8245edfc294578b0ef5ad8ffb530a82bd1228b6dad244ac4`.
- Shared renderer SHA-256:
  `2d082b0ab6e3bdd66a776bd48a9c6ba67827bb2edf8b355b340219bd6aaf0efa`.
- Checkpoint-23 composed Primary output SHA-256:
  `76f0dc9de7ce9b64f352286d1ad853033b770b9eeeba5c99904fc988e6a4ca92`.
- Checkpoint-23 Young output SHA-256:
  `0ce5ad2d19bbadfab99be0662b295bcca9425d6514a090e275eb1cd01f8e273d`.
- All three local receipts include exact source/output identities, UI composition
  evidence when selected, builder/helper/layout-input hashes and selected-source
  validation results. Refreshing receipt metadata left generated HTML hashes
  unchanged after browser QA. The source and UI branch readbacks remain the
  commits listed above. Screenshots stay local under `name-atlas-primary-review/`.
- The first GitHub quality run caught a new unit-test assumption about full Git
  history. Unit tests now use the current immutable HEAD or synthetic later
  source; actual checkpoint-23/24 integration remains mandatory in the dedicated
  workflow with full history. The existing shallow quality checkout is retained,
  with no skipped tests, relaxed guards or broader history fetch in that job.
  A fresh depth-one local clone with the corrected tests passes the project check
  and all 37 Python tests, reproducing that checkout constraint before push.

## Remaining milestones and provisional active-work estimates

Stop at PERF-1 for review after the draft PR and its checks are recorded.

1. PERF-2: reduce remaining pan geometry work and profile the full refresh path;
   assess selective updates for connections, index and reading locator. Add
   comparable correctness checks before accepting further caching. Estimated
   2–4 active hours for the next usable performance checkpoint, excluding waits.
2. After a deliberate editorial snapshot selection: combine accepted UI and
   performance changes against that snapshot, recheck content identities and
   repeat browser acceptance. Estimated 45–90 active minutes after inputs are
   selected; no editorial completion date is implied.
3. Packaging/source consolidation follows the editorial handoff, with preserved
   standalone delivery and explicit integrity mappings. Scope/estimate pending
   that handoff. Release and live-host readback remain separately authorized.
