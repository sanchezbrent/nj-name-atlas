#!/usr/bin/env python3
"""Build an isolated UI preview from an immutable Git content commit.

Never writes docs/, baselines, Git refs, editorial checkpoints or browser storage.
Generated HTML stays outside Git and must not be published before editorial QA.
"""
import argparse
import hashlib
from html.parser import HTMLParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE = ROOT / "prototypes/primary-layout"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ASSETS = (".nojekyll", "404.html", "index.html", "primary/index.html", "robots.txt", "styles.css", "young-explorers/index.html")
MARKER = ".layout-preview.json"


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


class Document(HTMLParser):
    """Locate exact source spans without serializing or normalizing the page."""
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        for match in re.finditer("\n", source):
            self.lines.append(match.end())
        self.nodes, self.stack = [], []
        self.feed(source)
        ids = [n["attrs"]["id"] for n in self.nodes if "id" in n["attrs"]]
        require(len(ids) == len(set(ids)), "Duplicate source DOM IDs; reconcile upstream markup first.")

    def source_offset(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        start = self.source_offset()
        node = {"tag": tag, "attrs": dict(attrs), "start": start,
                "inner": start + len(self.get_starttag_text())}
        self.nodes.append(node)
        if tag in VOID:
            node.update(close=node["inner"], end=node["inner"])
        else:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            node = self.stack.pop()
            node.update(close=node["inner"], end=node["inner"])

    def handle_endtag(self, tag):
        matches = [i for i, node in enumerate(self.stack) if node["tag"] == tag]
        if matches:
            index = matches[-1]
            node = self.stack[index]
            node.update(close=self.source_offset(), end=self.source.index(">", self.source_offset()) + 1)
            del self.stack[index:]

    def one(self, *, tag=None, id=None, cls=None):
        found = [n for n in self.nodes if (tag is None or n["tag"] == tag)
                 and (id is None or n["attrs"].get("id") == id)
                 and (cls is None or cls in n["attrs"].get("class", "").split())]
        require(len(found) == 1 and "end" in found[0],
                "Expected one complete element: " + str((tag, id, cls)))
        return found[0]

    def raw(self, node):
        return self.source[node["start"]:node["end"]]

    def blocks(self, tag):
        return [self.raw(n) for n in self.nodes if n["tag"] == tag]

    def ids(self):
        return {n["attrs"]["id"] for n in self.nodes if "id" in n["attrs"]}


REQUIRED_IDS = ("nj-name-atlas", "explore-heading", "atlas-search", "atlas-county", "atlas-town",
                "atlas-tour-chooser", "atlas-reading-toggle", "atlas-story", "atlas-story-content",
                "atlas-referent", "atlas-origin-note", "atlas-pilot-story", "atlas-name-glance",
                "atlas-events", "atlas-all-sources", "atlas-pilot-data", "atlas-reader-context")


def verify_preservation(source, candidate):
    before, after = Document(source), Document(candidate)
    require(before.blocks("script") == after.blocks("script"),
            "Runtime or embedded content changed; UI integration rejected.")
    original_styles = before.blocks("style")
    require(after.blocks("style")[:-1] == original_styles
            and len(after.blocks("style")) == len(original_styles) + 1,
            "Original styles changed or overlay missing.")
    require(before.ids() <= after.ids(), "An existing DOM ID was removed.")
    require(after.ids() - before.ids() == {"layout-map-heading", "layout-more", "primary-layout-overlay"},
            "Unexpected prototype DOM IDs.")
    before_meta = [before.raw(n) for n in before.nodes if n["tag"] == "meta"]
    after_meta = [after.raw(n) for n in after.nodes if n["tag"] == "meta"]
    require(before_meta == after_meta, "CSP or metadata changed.")
    return {
        "source_sha256": digest(source), "preview_sha256": digest(candidate),
        "original_scripts_identical": True,
        "script_sha256": [digest(x) for x in before.blocks("script")],
        "original_styles_identical": True, "existing_dom_ids_preserved": len(before.ids()),
        "metadata_and_csp_identical": True,
    }


def transform(source, css):
    doc = Document(source)
    for id in REQUIRED_IDS:
        doc.one(id=id)
    root = doc.one(id="nj-name-atlas")
    require(root["attrs"].get("class") == "atlas-sheet", "Expected the unchanged Primary root class.")
    require("primary-layout-overlay" not in doc.ids(), "Prototype is already applied.")
    require("</style" not in css.lower(), "Invalid style overlay.")
    require(len(doc.blocks("script")) == 4, "Unexpected script ownership; review integration contract.")
    head, masthead = doc.one(tag="head"), doc.one(tag="header", cls="masthead")
    expected_masthead = '<header class="masthead">\n    <h1>New Jersey</h1>\n    <p class="subtitle">An atlas of names</p>\n    <p class="edition">564 municipalities <span aria-hidden="true">·</span> 21 counties</p>\n  </header>'
    require(doc.raw(masthead) == expected_masthead, "Masthead changed upstream; reconcile UI copy before applying.")
    explore = doc.one(tag="aside", cls="explore")
    title, search = doc.one(id="explore-heading"), doc.one(id="atlas-search")
    require(source[title["inner"]:title["close"]] == "Explore", "Search heading changed upstream.")
    tour = doc.one(id="atlas-tour-chooser")
    map_panel, origin = doc.one(tag="section", cls="map-panel"), doc.one(cls="referent-block")
    require(source[map_panel["inner"]:map_panel["close"]].lstrip().startswith('<div class="map-browse-toolbar">'), "Map heading changed upstream.")
    filters = doc.one(id="atlas-filters")
    require(filters["tag"] == "details", "Origin legend container changed upstream.")
    filter_summaries = [n for n in doc.nodes if n["tag"] == "summary" and filters["inner"] < n["start"] < filters["close"]]
    require(len(filter_summaries) == 1, "Origin filter heading changed upstream.")
    filter_summary = filter_summaries[0]
    filter_label_end = source.find('<span id="atlas-origin-filter-hint"', filter_summary["inner"], filter_summary["close"])
    require(filter_label_end >= 0, "Origin filter hint moved upstream.")
    require(explore["inner"] < tour["start"] < tour["end"] < explore["close"], "Advanced tools moved upstream.")
    search_tag = source[search["start"]:search["inner"]]
    require(search_tag.count('placeholder="Town or former name"') == 1, "Search markup changed upstream.")
    advanced = source[tour["start"]:explore["close"]]
    edits = [
        (head["close"], head["close"], '<style id="primary-layout-overlay">\n' + css + '\n</style>\n'),
        (root["start"], root["inner"], source[root["start"]:root["inner"]].replace('class="atlas-sheet"', 'class="atlas-sheet primary-layout-preview"')),
        (masthead["start"], masthead["end"], '<header class="masthead">\n    <p class="layout-brand">New Jersey · An Atlas of Names</p>\n    <h1>Why is your town <span>called that?</span></h1>\n    <p class="subtitle">Find a place. Follow its names. Explore the stories behind them.</p>\n  </header>'),
        (title["inner"], title["close"], "Find your town"),
        (filters["start"], filters["inner"], '<section class="origin-filters" id="atlas-filters" aria-label="Map colors and name origins">'),
        (filters["close"], filters["end"], '</section>'),
        (filter_summary["start"], filter_summary["inner"], '<h3 class="layout-legend-heading">'),
        (filter_summary["inner"], filter_label_end, "Map colors: current-name origins"),
        (filter_summary["close"], filter_summary["end"], '</h3>'),
        (search["start"], search["inner"], search_tag.replace('placeholder="Town or former name"', 'placeholder="Search a town or an older name"')),
        (tour["start"], explore["close"], '<details id="layout-more" class="layout-more"><summary>More ways to explore</summary><div class="layout-more-body">\n' + advanced + '\n</div></details>\n    '),
        (map_panel["inner"], map_panel["inner"], '<div class="layout-map-heading"><h2 id="layout-map-heading">Choose a place</h2><p>Select a town to discover its name story.</p></div>'),
        (origin["end"], origin["end"], '<p class="layout-reading-hint">Read the full story, follow earlier names, and explore its sources.</p>'),
    ]
    ordered = sorted(edits)
    require(all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:])), "Overlapping layout transformations.")
    candidate = source
    for start, end, replacement in reversed(ordered):
        candidate = candidate[:start] + replacement + candidate[end:]
    candidate = reader_flow(candidate)
    return candidate, verify_preservation(source, candidate)


def reader_flow(source):
    """Move existing surfaces, never copy their live state or historical text.

    Keep event entries outside any new disclosure: the original runtime opens
    and focuses those entries directly for routes, timeline jumps and citations.
    Only the alternate glance view gains a native, initially closed disclosure.
    """
    doc = Document(source)
    story, filters = doc.one(id="atlas-story"), doc.one(id="atlas-filters")
    map_panel = doc.one(cls="map-panel")
    tools, title = doc.one(cls="story-tools"), doc.one(id="atlas-title")
    navigation, origin = doc.one(cls="story-navigation"), doc.one(cls="referent-block")
    narrative, glance = doc.one(id="atlas-pilot-story"), doc.one(id="atlas-name-glance")
    glance_title, journey = doc.one(id="atlas-name-glance-title"), doc.one(cls="journey")
    journey_title = doc.one(id="atlas-journey-heading")
    require(filters["end"] < map_panel["start"] < story["start"], "Browse surfaces moved upstream.")
    require(story["inner"] < tools["start"] < tools["end"] < title["start"], "Reading control moved upstream.")
    require(navigation["end"] < origin["start"] < narrative["start"] < glance["start"] < journey["start"],
            "Story surfaces moved upstream.")
    require(glance["tag"] == "section" and glance_title["tag"] == "h3", "Glance disclosure contract changed.")
    require(source[journey_title["inner"]:journey_title["close"]] == "The name journey", "Chronology heading changed upstream.")
    # Transform the story independently before relocating its complete span.
    story_edits = [
        (tools["start"], tools["end"], ""),
        (title["end"], title["end"], "\n" + doc.raw(tools)),
        (navigation["start"], origin["start"], ""),
        (narrative["end"], narrative["end"], "\n" + source[navigation["start"]:origin["start"]]),
        (glance["start"], glance["end"], ""),
        (journey["end"], journey["end"], "\n" +
         '<details id="atlas-name-glance" class="name-glance labeled-disclosure" aria-labelledby="atlas-name-glance-title">' +
         "\n<summary>" + doc.raw(glance_title) + "</summary>" +
         source[glance_title["end"]:glance["close"]] + "</details>"),
        (journey_title["inner"], journey_title["close"], "Chronology"),
    ]
    story_markup = doc.raw(story)
    for start, end, replacement in sorted(story_edits, reverse=True):
        story_markup = story_markup[:start-story["start"]] + replacement + story_markup[end-story["start"]:]
    # DOM and phone order: search, selected story, exposed legend, map. Desktop
    # places the same story beside the map with explicit grid positions.
    edits = [(story["start"], story["end"], ""), (filters["start"], filters["end"], ""),
             (map_panel["start"], map_panel["start"], story_markup + "\n" + doc.raw(filters) + "\n")]
    candidate = source
    for start, end, replacement in sorted(edits, reverse=True):
        candidate = candidate[:start] + replacement + candidate[end:]
    return candidate


def git_bytes(ref, path):
    require(bool(re.fullmatch(r"[0-9a-f]{40}", ref)), "Use an immutable full 40-character commit SHA.")
    return subprocess.check_output(["git", "-C", str(ROOT), "show", ref + ":" + path])


def validate_destination(destination):
    require(not destination.is_symlink(), "Output directory cannot be a symlink.")
    destination = destination.resolve()
    require(not any((p / ".git").exists() for p in [destination, *destination.parents]),
            "Output must be outside every Git checkout; source trees are read-only.")
    if destination.exists() and any(destination.iterdir()):
        marker = destination / MARKER
        require(marker.is_file() and not marker.is_symlink(), "Refusing to overwrite an unmanaged directory.")
        require(json.loads(marker.read_text()).get("generator") == "primary-layout-prototype-v1", "Unknown preview owner.")
        expected = set(ASSETS) | {MARKER}
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file() or p.is_symlink()}
        require(actual <= expected, "Unexpected files in preview; use a fresh output directory.")
    require(not destination.exists() or not any(p.is_symlink() for p in destination.rglob("*")), "Preview contains symlinks.")
    return destination


def build(ref, destination):
    destination = validate_destination(destination)
    baseline = json.loads(git_bytes(ref, "project/asset-baseline.json"))
    expected = {a["path"]: a for a in baseline["assets"]}
    require(set(expected) == set(ASSETS), "Upstream public asset scope changed; review before building.")
    assets = {path: git_bytes(ref, "docs/" + path) for path in ASSETS}
    for path, data in assets.items():
        require(digest(data) == expected[path]["sha256"] and len(data) == expected[path]["bytes"],
                "Source asset disagrees with its checkpoint baseline: " + path)
    primary, report = transform(assets["primary/index.html"].decode(), (PROTOTYPE / "layout.css").read_text())
    result = dict(assets, **{"primary/index.html": primary.encode()})
    report.update(generator="primary-layout-prototype-v1", source_commit=ref,
                  changed_assets=[p for p in ASSETS if result[p] != assets[p]],
                  source_asset_sha256={p: digest(data) for p, data in assets.items()},
                  output_asset_sha256={p: digest(data) for p, data in result.items()},
                  overlay_sha256=digest((PROTOTYPE / "layout.css").read_bytes()),
                  builder_sha256=digest(Path(__file__).read_bytes()),
                  checkpoint_manifest_sha256=digest((PROTOTYPE / "checkpoint.json").read_bytes()),
                  publication_cleared=False)
    require(report["changed_assets"] == ["primary/index.html"], "Unexpected non-Primary asset change.")
    # Validate everything before touching output. No source/baseline/ref writes occur.
    destination.mkdir(parents=True, exist_ok=True)
    for path, data in result.items():
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (destination / MARKER).write_text(json.dumps(report, indent=2) + "\n")
    return report


def verify_runtime(ref, destination, report):
    """Run the selected content checkpoint's own checks against composed pages."""
    node = shutil.which("node")
    require(node is not None, "Node.js 22+ is required for --verify.")
    available = set(subprocess.check_output(["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", ref]).decode().splitlines())
    files = ("scripts/check_project.py", "scripts/project_public_copy.py", "tests/corpus.mjs",
             "tests/notebook.mjs", "project/asset-baseline.json", "project/content-baseline.json",
             "project/public-copy-baseline.json", "project/public-copy-corrections.json")
    results = []
    with tempfile.TemporaryDirectory(prefix="atlas-ui-validation-") as folder:
        fixture = Path(folder)
        for path in files:
            if path in available:
                target = fixture / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(git_bytes(ref, path))
        for path in ASSETS:
            target = fixture / "docs" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((destination / path).read_bytes())
        # Only this disposable fixture's asset hashes describe the proposed UI.
        # The content baseline, copy proposals and source checkout stay unchanged.
        baseline_path = fixture / "project/asset-baseline.json"
        baseline = json.loads(baseline_path.read_text())
        for asset in baseline["assets"]:
            data = (fixture / "docs" / asset["path"]).read_bytes()
            asset.update(bytes=len(data), sha256=digest(data))
        baseline_path.write_text(json.dumps(baseline))
        commands = ([sys.executable, "scripts/check_project.py"],
                    [node, "tests/notebook.mjs"], [node, "tests/corpus.mjs"])
        for command in commands:
            result = subprocess.run(command, cwd=fixture, capture_output=True, text=True)
            require(result.returncode == 0, "Selected checkpoint validation failed: " + command[-1] + "\n" + result.stdout + result.stderr)
            results.append({"check": command[-1], "result": json.loads(result.stdout)})
    report["selected_checkpoint_validation"] = results
    (destination / MARKER).write_text(json.dumps(report, indent=2) + "\n")


def preview_handler(destination):
    class Preview(BaseHTTPRequestHandler):
        def do_GET(self):
            path = unquote(urlsplit(self.path).path)
            base = "/nj-name-atlas/"
            if path == "/":
                self.send_response(302)
                self.send_header("Location", base + "primary/#town=0308")
                self.end_headers()
                return
            if not path.startswith(base):
                self.send_error(404)
                return
            rel = path[len(base):]
            if not rel or rel.endswith("/"):
                rel += "index.html"
            if rel not in ASSETS:
                self.send_error(404)
                return
            data = (destination / rel).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(rel)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
    return Preview


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", default=json.loads((PROTOTYPE / "checkpoint.json").read_text())["content_commit"])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--verify", action="store_true", help="Run this content commit's own project, notebook and corpus checks on the composed preview.")
    parser.add_argument("--port", type=int, default=8941)
    args = parser.parse_args()
    try:
        report = build(args.source_ref, args.output_dir)
        if args.verify:
            verify_runtime(args.source_ref, args.output_dir.resolve(), report)
        print(json.dumps(report), flush=True)
        if args.serve:
            print(f"Local UI prototype: http://127.0.0.1:{args.port}/nj-name-atlas/primary/#town=0308", flush=True)
            ThreadingHTTPServer(("127.0.0.1", args.port), preview_handler(args.output_dir.resolve())).serve_forever()
    except ContractError as error:
        parser.exit(1, "Integration contract failed: " + str(error) + "\n")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
