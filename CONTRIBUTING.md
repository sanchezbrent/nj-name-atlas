# Working on the atlas

Start with [the current state](project/CURRENT_STATE.md). Use a branch and a pull
request for every change. The owner can merge their own PR after the required
checks pass; a second person's review is encouraged when available.

Run `python3 scripts/check_project.py` and
`python3 -m unittest discover -s tests -v` and `node tests/notebook.mjs` from the repository root. Python 3.10+
and Node.js 22+ are sufficient; there is nothing to install from npm or pip.
Run `python3 scripts/preview.py` for a loopback preview at
`http://127.0.0.1:8780/nj-name-atlas/`. The preview serves only website files.

The automated checks protect the exact publishing asset list, reviewed bytes,
twelve-profile payload scope, authoritative data identities, embedded-resource
policy, edition links and JavaScript syntax. Negative tests prove corruption and
accidental private-file additions are rejected. These checks supplement browser
review; they do not certify historical truth, all devices or native downloads.

For an atlas-content change, first obtain its factual authority from the private
research repository. Preserve raw wording and uncertainty; distinguish a date's
reported form from a chosen normalization. Save exact before/after mappings and
source references. Update approved asset identities only after that review.
Never upload source workbooks or internal audit material to demonstrate a PR.

For UI changes, inspect both editions, a current and older record, town/event deep
links, phone layout, keyboard focus and source/lesson controls. Use invented notes
only, and do not inspect or overwrite existing notes. Record what was actually
tested and what remains uncertain. Check the real Pages address after deployment.

Report bugs with the issue forms. For historical corrections provide public source
links, quoted wording and the uncertainty; a proposed correction is not a fact.
Do not file new issues or send messages automatically on someone else's behalf.

Checkpoint handoffs must include the general progress tracker and active-work ETA,
with research coverage separated from website and release work. Stop at checkpoints.
