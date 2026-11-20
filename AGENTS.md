# Public atlas working instructions

Read README.md, CONTRIBUTING.md, project/CURRENT_STATE.md, project/PUBLICATION_STANDARD.md and project/PUBLIC_COPY_REMEDIATION.md before changing files.
This repository contains the public standalone atlas and development safeguards.
Research authority and full checkpoint recovery live in the separate private
`sanchezbrent/nj-name-atlas-research` repository and sealed local checkpoints.

- Preserve the accepted atlas design, source wording, uncertainty and date forms.
- Apply the public/private editorial boundary at every research, writing, export, UI, release and handoff stage. Original research wording, process/audit notes, AI/PDF/HTML handling status and internal IDs belong only in private authority, **never** in reader views or delivered public HTML/JS/data, even behind a collapsed panel. Preserve cited historical evidence and genuinely disputed explanations in plain language.
- The statewide public-copy remediation register is OPEN. Existing 564-story coverage and passing CI do not certify copy separation. A public-copy release requires 564/564 manually reviewed in each edition plus payload and live readback; do not claim completion until verified.
- All 564 municipalities have completed C57 reader stories in both editions and
  an individual Review27 category decision. Preserve the rewrites. Completion
  does not resolve every uncertain origin or imply universal reader acceptance.
  Public-copy remediation has standing owner authorization for agent-selected
  runs of at most 24 municipalities across both editions, saved and validated
  in checkpoints of at most twelve. Continue through the authorized run without
  renewed town-selection approval, then stop after 24. New historical research or adjudication still needs an
  explicit scope.
- C21 is factual authority. C57 is the frozen narrative/source baseline and
  Review27 supplies the guarded category display overlay. Never recalculate or
  roundtrip authority workbooks as part of a website task.
- Keep source/date/lesson guards and original notebook semantics and storage key.
  Never inspect, migrate, relabel, sync or transmit existing browser notes implicitly.
- Do not put workbooks, raw exports, audit files, checkpoint archives, credentials,
  private handoffs or unrelated NJ PBS repository source into this public Git tree.
- `docs/` is an exact allowlist. `project/asset-baseline.json` records approved
  bytes; changing a baseline needs explicit review and a before/after evidence map.
- Make changes on a branch, run checks and use a pull request. Do not bypass
  required checks, force-push protected branches or weaken protection to land work.
- Avoid dependency additions unless they solve a concrete need. This site has no
  build dependencies. No analytics, trackers, new hosting, messages or schedules
  are implied by routine maintenance.
- Each checkpoint completion and saved handoff must show current stage, changes,
  remaining agreed milestones/checkpoint range, and a provisional active-work ETA
  for the next checkpoint and usable deliverable. Exclude review/access/wait time.
  Keep research/export/editorial/implementation/testing/release progress distinct.
- Stop at the agreed checkpoint. Re-read live main and preserve intervening edits.
