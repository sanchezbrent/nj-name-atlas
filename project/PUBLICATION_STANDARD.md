# NJ Name Atlas — Public editorial and research boundary

**Status:** Governing standard for all existing and future Atlas work, effective November 19, 2026. Applies to all 564 municipalities, the primary Atlas, Young Explorers, current and former town names, maps, stories, summaries, journeys, sidebars, deep-reading panels, search results, source lists, exports, embeds, standalone HTML/JavaScript, and every later publication format.

**Reader promise:** Explain what a municipality's name means, where it came from, why it may have changed, and how strongly the evidence supports the story. Do not make readers navigate internal research notes to learn that history.

## Separation of records

Maintain three separate layers, without collapsing or overwriting them:

1. **Authoritative historical research (restricted/internal).** Exact source transcriptions, raw/original research wording, PDFs, workbook notes, disputed-source logs, review statuses, record IDs, audit checkpoints, access limitations, AI-assisted extraction notes, file names, provenance and unresolved research questions. Preserve them exactly in the appropriate private authority/checkpoint; never modify sealed originals to solve a public-display problem. The current remote private companion is not a complete replacement for sealed local authority.
2. **Reviewed public editorial records.** Reader-language summaries, full narratives, name journeys, sidebars, public dates, named competing theories where supportable, appropriately qualified conclusions, and citations to evidence actually reviewed. C21 remains the factual/source baseline, C57 the sealed narrative checkpoint, and Review27 the reviewed category overlay for this publication. Existing baselines are not silently rewritten.
3. **Public presentation/export.** Only explicitly approved reader fields and public references enter the shipped HTML, scripts, data payloads, searches, maps, exports or embeds. Hidden accordions, CSS hiding and inaccessible-looking panels do **not** make embedded data private.

“Original research wording” is an internal preservation and comparison aid, **not a public feature**. Do not include its text, disclosure control or underlying private fields in a public bundle. Retain exact originals in authority records and make any source-derived public quotation a deliberate, cited editorial choice.

## The public editorial test

**Include:** A clear account of the name's origin; historical people, languages, places, events, dates and changes; relevant alternative explanations; the strength/limits of the evidence; primary and reliable secondary source citations; and meaningful uncertainty stated in ordinary language.

**Exclude from every reader-facing field:** Internal IDs (for example, AS-617), batch numbers, AI-generated HTML or PDF handling notes, “uninspected” or “not read” source-status language, conversion/OCR/tool descriptions, local filenames, source-processing attempts, implementation details, author-to-auditor notes, audit/checkpoint bookkeeping and unedited research prose. Research logs may retain all these details internally.

**Distinguish uncertainty from workflow:** “Historians disagree about whether the name refers to X or Y” can be valuable if the supporting evidence is present. “The PDF was not read in this batch” says nothing useful about the actual history and must stay internal. Never turn a researcher-access limitation into an asserted historical dispute, or conceal a real dispute to make copy sound definitive.

**Sources:** Preserve existing source identities, useful citations, authors, work titles, years, page references and links when verified. Never invent citations, imply that an uninspected source was reviewed, or treat AI-generated/extracted text as independent source evidence. Missing verification triggers internal follow-up or an appropriately qualified public statement supported by what *was* reviewed; do not erase evidence because its display is awkward.

**Readability:** Prefer plain English, short direct paragraphs, and context that a general NJ audience can understand. Avoid academic or production jargon in the default story. Young Explorers gets a separately adapted, age-appropriate explanation, not an automatic copy of the primary wording; preserve the same evidentiary limits.

**Editorial examples:** Do not publish “Whippanong PDF was not read ... AS-617 ... AI-generated HTML ... uninspected 1720 order.” If the verified evidence supports it, publish a historical explanation of the competing names or unresolved question, with appropriate citations and without research-process commentary. This is a style example, **not** a new factual conclusion about any specific municipality.

## Mandatory lifecycle gates

1. **Intake/research:** Capture original statements, source provenance, conflicts, verification status and methodology internally. Preserve uncertainty and sealed checkpoints. Keep the existing at-most-twelve-municipality historical/editorial batch safeguards unless separately authorized.
2. **Audit/verification:** Identify what sources actually establish, what remains disputed and what is merely uninspected; make no automatic resolution. Keep audit IDs, file/tool notes and checking history internal. Changes to historical truth or sources require a separately authorized, sourced review.
3. **Narrative editing:** Write a separate public explanation; compare every claim/date/interpretation with the verified research; explicitly preserve qualifying language. Do not paste raw research or audit logs into narrative fields.
4. **Category review:** Preserve Review27 decisions and guarded mapping checks. Category labels and explanations must be reader-relevant; no process-state labels.
5. **Export/build:** Publish from an explicit, audited allowlist of public fields. Do not serialize private annotations, original research text or raw internal records into a downloadable payload, even when a UI control is hidden. Verify both editions and each output format.
6. **Editorial QA:** Inspect **all 564 municipalities in each edition** for public-copy/process leakage (1,128 municipality-edition records), including long-form panels, search, source drawers and deep links. Check automated candidate reports **and** manually review context; simple keyword filters do not prove compliance. Record town/edition, field, issue, evidence, proposed public treatment and resolution.
7. **Pre-release QA:** Confirm that appropriate citations, dates, source/uncertainty controls, town identities, original notebook behavior, all category counts and UI accessibility still work. Inspect the built HTML/JS/data, not only rendered screens. Keep existing baseline/hash and negative-test protections. No research workbook is modified merely for copy cleanup.
8. **Release:** Require a scoped sign-off recording 564/564 per edition, remaining exceptions and deployment/live readback. A copy release with unresolved internal-leak exposure is **blocked**, not “passed with a warning.” If cleanup requires historical interpretation rather than wording removal, escalate it as a separate research review.
9. **Handoff/maintenance:** Every future assistant, contributor, batch and release handoff must link this standard, record public-copy review status independently of factual research and implementation, and carry forward open items. Do not report an editorial clean bill of health based on narrative coverage, CI or successful Pages deployment alone.

## Enforcement and changes

- CONTRIBUTING.md and the PR checklist govern manual sign-off. scripts/audit_public_copy.py produces heuristic candidate findings across both published data bundles. It is report-only while known issues remain; its absence of matches is not proof of full clearance. Strict mode may be used as a supplementary blocking check **after** the existing leakage is repaired and verified.
- The release audit in project/PUBLIC_COPY_REMEDIATION.md is currently **open**. A policy-only PR does not remediate current public HTML.
- Record source/evidence IDs in internal review records; the public need only receive understandable citations. Preserve reviewed C21/C57/Review27 identities and do not silently change their seals.
- When unsure whether text is historical evidence or a process note, retain the original internally, leave unsupported interpretation unasserted, and request editorial/source review before release.
- This policy applies to edits, new research, category changes, UI experiments, project handoffs and all republished derivatives. No publishing exception is implied by past release status.
