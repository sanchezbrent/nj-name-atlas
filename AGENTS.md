# Public atlas working instructions

Read README.md, CONTRIBUTING.md and project/CURRENT_STATE.md before changing files.
This repository contains the public standalone atlas and development safeguards.
Research authority and full checkpoint recovery live in the separate private
`sanchezbrent/nj-name-atlas-research` repository and sealed local checkpoints.

- Preserve the accepted atlas design, source wording, uncertainty and date forms.
- Twelve profiles have the current review; 552 retain older records. Never imply
  statewide review completion. A historical/editorial batch may cover at most
  twelve municipalities and must be explicitly requested.
- C13 is factual authority: exact C5 workbooks, C6 export, C8/C9 originals. C14
  public derivatives change only a visible pilot label. Never recalculate or
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
