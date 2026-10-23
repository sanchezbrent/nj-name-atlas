# New Jersey — An Atlas of Names

[![Atlas quality](https://github.com/sanchezbrent/nj-name-atlas/actions/workflows/quality.yml/badge.svg)](https://github.com/sanchezbrent/nj-name-atlas/actions/workflows/quality.yml)

**[Open the atlas](https://sanchezbrent.github.io/nj-name-atlas/)** ·
[The Atlas](https://sanchezbrent.github.io/nj-name-atlas/primary/) ·
[Young Explorers](https://sanchezbrent.github.io/nj-name-atlas/young-explorers/)

Explore the name journeys of New Jersey municipalities. This is a research pilot:
twelve profiles reflect the current review, and 552 retain earlier records.
Sources, qualified dates and unresolved questions stay visible in the atlas.
Publication does not imply that every profile has received the current review.

## Continue the project

- [Current state and remaining work](project/CURRENT_STATE.md)
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
python3 scripts/preview.py
```

The preview is available at `http://127.0.0.1:8780/nj-name-atlas/` and serves only
website files. CI checks approved asset identities, private-file boundaries,
twelve-profile payload scope, script syntax, edition links and original notebook
behavior with isolated fake storage. Its negative tests prove that accidental
asset changes and private files are rejected.

## Notes and publishing

Young Explorers notes stay in your browser when you explicitly choose Save.
Download a copy to keep it. Notes at another address do not migrate automatically.
There is no account-sync or note-transmission service.

GitHub Pages publishes `main` and `/docs`. Keep every font, map and data payload
embedded. Use a branch and checked pull request for changes; do not put private
workbooks or checkpoint archives in public source or website assets. The original
pilot documents are preserved separately. Current public derivatives change only
the visible “Private pilot” label to “Research pilot.”
