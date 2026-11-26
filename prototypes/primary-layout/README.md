# Primary layout prototype — checkpoint UI-1.2

This is the separate interface path toward the shared Atlas release. It does not
modify the editorial branch, either published edition, a content checkpoint or an
asset/content baseline. The production website remains unchanged.

## Open the prototype locally

Use Python 3.10+ from this branch. The pinned content commit must be present in
your local Git object database; fetch it read-only if necessary:

```sh
git fetch origin cbc5b9646a866ff03359f94877bc24a130b24d67
python3 scripts/build_layout_prototype.py --output-dir /tmp/atlas-layout-ui1 --verify --serve --port 8941
```

Open `http://127.0.0.1:8941/nj-name-atlas/primary/#town=0308`. Cinnaminson is in
the saved checkpoint's reviewed batch. Other towns remain accessible for layout
testing; this does not certify their copy. A new port/origin avoids loading notes
from a pre-existing browser origin. Do not inspect existing browser notes.

The output must be outside every Git checkout. Existing unmanaged directories,
symlinks and changed source contracts are rejected. The loopback server serves
only the seven existing website assets; it cannot serve Git source, private
records, the integration receipt or arbitrary filesystem paths.

Do not commit generated HTML, copy it into `docs/`, upload it as a CI artifact,
publish it or use it as an editorial source. The source includes copy still under
review. GitHub stores the overlay/tooling and checks, not another content copy.

## What is being tried

- An inviting question and a single search row across the top.
- A map and a distinct selected-town preview instead of three competing columns.
- The same selected-town preview before the map on phone, with its title and
  reading action in the first screen at 390px. No duplicated story or selection.
- A prominent existing “Read the story” control and the existing reading view.
- An exposed, horizontal origin legend that wraps on smaller screens.
- A full-width desktop legend, placed directly before the map on phone.
- Additional browsing controls under “More ways to explore.”
- Narrative before quieter section links; one compact default chronology, with
  each original record expandable. “Names at a glance” is an optional native
  disclosure after that chronology. Every moment remains available; no automatic
  choice of editorial highlights is introduced.
- Existing qualifications remain with the origin explanation; dates, references,
  category colors, deep links, tours and source holds retain their existing logic.

There is no new JavaScript, dependency, content schema, data extraction, note
storage, tracking, hosting or publication configuration. The original map
projection and coordinate geometry are retained. The original runtime owns all
interaction and guard decisions. Young Explorers is copied byte-for-byte for
comparison; the separate starter-section move in PR #6 is not duplicated here.

## Content and integration contract

`checkpoint.json` pins completed **public-copy checkpoint 23**, commit
`cbc5b9646a866ff03359f94877bc24a130b24d67`, from editorial PR #5. Its 255/564 agent
text reviews per edition are draft proposals; human acceptance and release
clearance remain open. The moving editorial branch is never used implicitly.

The builder reads committed blobs and validates all seven source assets against
that commit's own asset baseline. It adds the CSS overlay and bounded UI markup
changes without parsing/repacking embedded data. It rejects missing/duplicate DOM
IDs, unexpected script counts, metadata/CSP drift, changed original styles,
changed original scripts/data, non-Primary inputs and reapplication.

Every build records source commit, source/output asset hashes, all original script
hashes, overlay hash, preserved DOM IDs and `publication_cleared: false` in the
output's `.layout-preview.json`. These hashes include source bindings and the
complete embedded historical data, not just visible story text. Exactly one
generated asset may change: Primary HTML. The other six must remain exact.

To rehearse integration with a newer completed checkpoint, use its full commit:

```sh
python3 scripts/build_layout_prototype.py --source-ref FULL_40_CHARACTER_COMMIT_SHA --verify --output-dir /tmp/atlas-layout-next
```

This creates a new preview and preservation receipt. It does not update the pin,
change either branch, migrate a checkpoint or grant publication approval. Review
the new content checkpoint and repeat browser QA before deliberately changing
the pin in a separate recorded commit. An unchanged DOM contract cannot prove a
future runtime has identical behavioral assumptions; browser validation remains
mandatory after every source/runtime change.

`--verify` requires Node.js 22+. It runs the **selected content commit's own**
project/schema/source, notebook and corpus checks on the composed pages in a
disposable directory. Only that disposable fixture receives proposed asset
hashes; committed baselines and copy proposals remain untouched. Results are
added to the preview receipt. CI verifies both the editorial pin and this branch's
source. It does not upload generated pages or alter the existing quality job.

## Shared-outcome integration procedure

1. Preserve both paths' existing commits, checkpoint records and private authority
   seals. UI work never edits research, source wording, checkpoint counts or copy
   proposals. PR #5 remains the content owner; this draft remains the UI owner.
2. Select the latest completed editorial checkpoint and exact accepted UI commit.
   Create a new integration branch after coordinating the integration window;
   do not push to the active editorial branch or replace an edition with an older
   generated file. The content owner need not interrupt an in-progress batch.
3. Reapply the bounded UI transformation to that selected content. Any contract
   failure stops integration for reconciliation. Never resolve HTML/data
   conflicts by accepting a whole older file or an older baseline.
4. Compare all original scripts/data, six unaffected assets, source/date/category
   guards and notebook behavior against the selected content commit. Generate
   proposed asset hashes from the combined result only; never restore UI-1 hashes
   over a later content baseline. Keep existing strict copy scanning and all
   editorial holds. The prototype does not change release eligibility.
5. Save a **new** integration checkpoint with the content commit, UI commit,
   generated hashes and before/after evidence. Run both editions' project,
   corpus, notebook, strict-copy and browser checks, including source-return
   links, town/event URLs, long/uncertain stories, mobile, keyboard and notes using
   invented data in isolated storage. Obtain the existing publication sign-off
   before a separately authorized merge/deployment and live readback.

Keep prototype acceptance, editorial acceptance and publication acceptance
separate. Design approval never marks the 564-by-two copy review complete.

## Checkpoint and remaining work

UI-1.2 implements the revised reading flow and retains the UI-1 integration
tooling. Research, workbook exports and editorial remediation remain on their existing path. See
[the recorded QA](../../project/PRIMARY_LAYOUT_PROTOTYPE.md) for actual checks and
limits. Remaining milestones are user review of the prototype, a deliberately
chosen later content checkpoint, combined acceptance and release. Allow
provisionally 30–60 active minutes for a bounded UI revision and 45–90 for an
integration rehearsal after the content snapshot is selected, excluding waits.
Editorial completion/publication have no ETA supplied by this UI checkpoint.

The [publication standard](../../project/PUBLICATION_STANDARD.md) and
[open remediation register](../../project/PUBLIC_COPY_REMEDIATION.md) govern this
work. Stop at this prototype checkpoint; do not resume editorial batches here.
