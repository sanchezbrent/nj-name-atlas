# New Jersey — An Atlas of Names

[![Atlas quality](https://github.com/sanchezbrent/nj-name-atlas/actions/workflows/quality.yml/badge.svg)](https://github.com/sanchezbrent/nj-name-atlas/actions/workflows/quality.yml)

**[Open the atlas](https://sanchezbrent.github.io/nj-name-atlas/)** ·
[The Atlas](https://sanchezbrent.github.io/nj-name-atlas/primary/) ·
[Young Explorers](https://sanchezbrent.github.io/nj-name-atlas/young-explorers/)

Explore the name journeys of all 564 New Jersey municipalities. Both editions
include the completed C57 reader stories, summaries, journeys and sidebars.
Review27 covers every category assignment, with 179 guarded display mappings.
Sources, qualified dates and unresolved explanations remain visible.

## Continue the project

- [Current state and remaining work](project/CURRENT_STATE.md)
- [Public editorial and research boundary](project/PUBLICATION_STANDARD.md) · [Open reader-copy cleanup](project/PUBLIC_COPY_REMEDIATION.md)
- [Development and contribution guide](CONTRIBUTING.md)
- [Recovery and rollback](project/RECOVERY.md)
- [Agent working instructions](AGENTS.md)
- [Security and private material](SECURITY.md) · [Rights and reuse](project/RIGHTS.md)

This public repository holds the website, tests and public working guidance. The
complete research authority belongs in the private `nj-name-atlas-research`
companion. Large archive uploads are currently pending at the owner's request;
keep verified local authority packets until remote recovery is verified.

## Local checks and preview

Use Python 3.10+ and Node.js 22+. No npm or pip dependencies are needed.

```sh
python3 scripts/check_project.py
python3 -m unittest discover -s tests -v
node tests/notebook.mjs
node tests/corpus.mjs
python3 scripts/audit_public_copy.py --strict  # intentionally fails while copy candidates remain
python3 scripts/preview.py
```

The preview is available at `http://127.0.0.1:8780/nj-name-atlas/` and serves only
website files. CI checks approved asset identities, private-file boundaries,
564-profile narrative coverage and guarded categories, script syntax, edition links and original notebook
behavior with isolated fake storage. Its negative tests prove that accidental
asset changes and private files are rejected.

The current remediation branch has blocked copy proposals; see
[checkpoint 48](project/PUBLIC_COPY_CHECKPOINT_48.md). Passing integrity tests does
not complete the 564-by-two contextual copy review. The frozen source baseline
and the candidate public projection have separate identity records.

## Notes and publishing

Young Explorers notes stay in your browser when you explicitly choose Save.
Download a copy to keep it. Notes at another address do not migrate automatically.
There is no account-sync or note-transmission service.

GitHub Pages publishes `main` and `/docs`. Keep every font, map and data payload
embedded. Use a branch and checked pull request for changes; do not put private
workbooks or checkpoint archives in public source or website assets. The original
pilot documents are preserved separately. Current public derivatives retain the completed narratives and category review.
See project/release-evidence.json for before/after asset identities.
