# Young Explorers starter-story placement

Stage: implementation and local verification complete; pull request and release pending.

The requested “Pick a story to explore” section moves from before `.atlas-columns`
to immediately after it, before the footer. The map and selected-town story now
come first. The three cards and “Find my town” remain together at full width.
The section's 22px spacing moves from its bottom to its top.

## Exact asset evidence for review

Base: `8b5597b728731cd6df4ee470caaedbe7041e1ffb`.

| Asset | Before SHA-256 | After SHA-256 | Bytes before/after |
| --- | --- | --- | --- |
| `docs/young-explorers/index.html` | `5e28671d49921dd6f986d020ef18678848192d2b0a02b361688ada4cdfb7fb60` | `4271a4aa4af9dd8c03c7073b05d8d368861de0c63bebbd0da10e0ecbc0ada280` | 11,797,861 / 11,797,861 |

An exact comparison against the base proves the section markup is identical.
Removing that section from each version and accounting for the single padding
change produces identical bytes. All scripts, embedded data, factual/source/date
guards, lesson text, notebook controller and the primary edition remain exact.
The corresponding asset-baseline hash update is proposed with this evidence.

## Verification

- Project checks pass: seven approved assets, six classic scripts and 564 profiles
  and narratives per edition.
- All nine Python tests, 16 isolated notebook assertions and 5,921 runtime corpus
  assertions pass. Tests use invented notes and fake storage.
- In-app browser at 1280px and 390px: starter choices appear after the map; no
  horizontal page overflow. Cards retain the responsive three-column/stacked layout.
- All three cards open the selected starter in reading view. Returning to the
  atlas restores the choices. “Find my town” focuses search; Tab from that button
  reaches the first card.
- Young lesson evidence and references open. Palmyra town/event links open the
  expected town and historical event in both editions. Primary reference controls
  and its 390px layout also pass the sampled checks.
- A fresh local origin was used. Existing user notes were not inspected, migrated,
  overwritten or transmitted. Native downloads and a full device matrix were not
  retested for this markup-only change.

## Publication and remaining work

The existing [publication standard](PUBLICATION_STANDARD.md) and
[open copy-remediation register](PUBLIC_COPY_REMEDIATION.md) still apply. The
report-only audit returns the unchanged 21,724 duplicate-inclusive candidates;
this is not a new editorial review or publication clearance. Historical research,
workbook exports and copy remediation are outside this layout request.

The usable local preview is complete. Remaining steps are checked PR review and
publication after the existing editorial hold is resolved, followed by live
readback. Allow about 5–10 active minutes for the layout's final release/readback,
excluding CI, review and access waits; the separate editorial hold has no ETA.
This request has no further implementation checkpoints.
