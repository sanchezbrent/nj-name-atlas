# Runtime performance prototype — PERF-1

This separate experiment reduces repeated rendering work in both editions. It is
stacked on the UI-1.8 branch in PR #7. It does not modify `docs/`, content or asset
baselines, the layout's editorial pin, or any editorial branch. No deployment.

From this worktree, with Python 3.10+ and Node.js 22+ on PATH:

```sh
python3 scripts/build_performance_prototype.py --reader-layout --verify --output-dir /tmp/atlas-performance-perf1 --serve --port 8942
```

Open `http://127.0.0.1:8942/nj-name-atlas/primary/#town=0308`. Young Explorers is
at the same origin under `/nj-name-atlas/young-explorers/`. Use a fresh preview
origin; do not inspect existing notes. The default source remains checkpoint 23,
`cbc5b9646a866ff03359f94877bc24a130b24d67`. `--source-ref` accepts a full immutable
commit and validates that commit's own approved asset baseline. `--reader-layout`
first composes Primary UI-1.8; without it both original layouts are retained.

Only runtime operations change:

- Keep municipality, context and county SVG nodes, titles and listeners.
- Validate each municipality's title through the existing guard when its node is
  first created. Those records are immutable for the loaded document; a new
  content checkpoint requires a new build/document and a new renderer. No cache
  is shared between documents, editions, origins or source versions. A future
  live content-editing API would need explicit cache invalidation first.
- Refresh classes and connection suffixes from current filters/selection. Stable
  handlers read the current derived matching/connection sets, so a dimmed town
  cannot retain an earlier active click handler.
- Regenerate base-layer geometry only when size, county or projection changes.
  Original D3 projection, recentering, label, selection, connection, clipping,
  compass and zoom/pan behavior remain owned by the original runtime.
- Keep town dropdown options when matching towns and county labels are unchanged;
  always update its selected value and disabled state immediately.

The builder makes four bounded replacements. Reversing those exact replacements
must recover every byte of its input. It leaves the original decoder, story/date/
category guards, notebook controller, packed payloads, styles and markup intact.
Primary can be checked in two steps: the existing UI contract, then the runtime
contract. Performance composition intentionally changes the runtime; do not claim
its script container is byte-identical. No guard is memoized or removed.

Generated pages and `.performance-preview.json` stay outside Git, have a distinct
owner from UI previews, and cannot overwrite a checkout or unmanaged directory.
Only the existing seven website paths are served over loopback; the receipt and
source tree cannot be served. Generated pages are not published or CI artifacts.
The receipt records source/output identities, helper/builder hashes, selected
checkpoint checks and `publication_cleared: false`.

```sh
python3 -m unittest discover -s tests -v
node tests/performance.mjs
node tests/layout_navigation.mjs
```

`tests/performance.mjs` uses both actual source payloads, existing validation
functions, bundled D3 and the original renderer block. It compares exact base-map
paths, color/class/title values and drawing order over nine state transitions,
plus dropdown and event behavior. It enforces deterministic allocation, guard
and path reuse; timing results are informative. Its minimal SVG model excludes
browser layout/paint, labels, selection and mapped-connection layers. It is not
an end-to-end latency or frame-rate measurement.

See [the checkpoint record](../../project/PERFORMANCE_PROTOTYPE.md) for evidence,
limitations and remaining stages. Publishing remains subject to the existing
[publication standard](../../project/PUBLICATION_STANDARD.md) and independent
editorial release review.
