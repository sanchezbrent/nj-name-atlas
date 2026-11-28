#!/usr/bin/env python3
"""Compose a local performance experiment without writing publishing sources.

Reversible runtime patches only; content, guards, styles and markup stay exact.
The default is the layout prototype's explicit frozen editorial checkpoint.
"""
import argparse
import json
from pathlib import Path
import sys
from http.server import ThreadingHTTPServer

import build_layout_prototype as layout

ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE = ROOT / "prototypes/performance"
MARKER = ".performance-preview.json"

OLD_MAP = """    $('atlas-land-mask').setAttribute('d',path(njLand));
    const context=$('atlas-context'),shapes=$('atlas-municipalities'),boundaries=$('atlas-boundaries'),labels=$('atlas-labels'),selection=$('atlas-selection');
    for(const layer of [context,shapes,boundaries,labels,selection])layer.replaceChildren();
    data.context.features.forEach(f=>context.append(svgEl('path',{d:path(f),class:'map-context'})));
    const matches=new Set(state.matching);
    const sorted=features.slice().sort((a,b)=>Number(a.properties.code===state.town)-Number(b.properties.code===state.town));
    sorted.forEach(f=>{
      const code=f.properties.code,p=profiles[code],active=matches.has(code),selected=code===state.town,connected=!!mapConnectionForCode(code);
      const shape=svgEl('path',{d:path(f),class:'municipality'+(active?'':' is-dimmed')+(selected?' is-selected':active&&state.town?' is-muted':'')+(connected?' is-connected':''),'data-code':code,'data-origin':p.current_origin});
      shape.style.setProperty('--origin-color',colorFor(code));
      shape.append(svgEl('title',{},p.name+' · '+p.county+' County · '+byTheme[p.current_origin].label+(storyHookFor(code)?' · '+storyHookFor(code):'')+(connected?' · Connected name history: '+mapConnectionForCode(code).label:'')));
      if(active||connected)shape.addEventListener('click',()=>{if(!drag.didMove)activateMappedTown(code);});
      shape.addEventListener('pointerenter',()=>showMapPreview(code,active));
      shape.addEventListener('pointerleave',()=>{$('atlas-map-hover').hidden=true;});
      shapes.append(shape);
    });
    data.counties.features.forEach(f=>boundaries.append(svgEl('path',{d:path(f),class:'county-boundary'})));"""

NEW_MAP = """    const context=$('atlas-context'),shapes=$('atlas-municipalities'),boundaries=$('atlas-boundaries'),labels=$('atlas-labels'),selection=$('atlas-selection');
    labels.replaceChildren();selection.replaceChildren();
    const matches=new Set(state.matching);
    atlasRetainedMap({key: JSON.stringify([width,height,state.county,projection.scale(),projection.translate()]),
      path,context,shapes,boundaries,mask:$('atlas-land-mask'),matches,selected:state.town,
      connections:relatedMapConnections()});"""

OLD_MENU = """    const select=$('atlas-town');select.replaceChildren(option('','Choose a town'));
    state.matching.forEach(code=>select.append(option(code,displayName(code)+(!state.county?' · '+profiles[code].county:''))));"""
NEW_MENU = """    const select=$('atlas-town');
    const menuSignature=JSON.stringify([state.county,state.matching]);
    if(menuSignature!==atlasTownMenuSignature){
      select.replaceChildren(option('','Choose a town'));
      state.matching.forEach(code=>select.append(option(code,displayName(code)+(!state.county?' · '+profiles[code].county:''))));
      atlasTownMenuSignature=menuSignature;
    }"""


def patches():
    helper = (PERFORMANCE / "map-renderer.js").read_text()
    layout.require("</script" not in helper.lower(), "Invalid performance helper.")
    insertion = helper + """
  const atlasRetainedMap=createAtlasRetainedMap({features,contextFeatures:data.context.features,
    countyFeatures:data.counties.features,land:njLand,profiles,byTheme,colorFor,storyHookFor,svgEl,
    activate:code=>{if(!drag.didMove)activateMappedTown(code);},
    preview:showMapPreview,hidePreview:()=>{$('atlas-map-hover').hidden=true;}});
"""
    return [
        ("  function drawMap(){", insertion + "  function drawMap(){"),
        (OLD_MAP, NEW_MAP),
        ("  function refresh(routeMode='replace'){", "  let atlasTownMenuSignature='';\n  function refresh(routeMode='replace'){"),
        (OLD_MENU, NEW_MENU),
    ]


def transform(source):
    layout.require('createAtlasRetainedMap' not in source, "Performance prototype already applied.")
    candidate = source
    for before, after in patches():
        layout.require(candidate.count(before) == 1, "Runtime contract changed; reconcile performance patch: " + before[:70])
        candidate = candidate.replace(before, after, 1)
    verify_preservation(source, candidate)
    return candidate


def verify_preservation(source, candidate):
    restored = candidate
    for before, after in reversed(patches()):
        layout.require(restored.count(after) == 1, "Performance patch missing, moved or modified.")
        restored = restored.replace(after, before, 1)
    layout.require(restored == source, "Change outside the approved performance patches.")
    # Parsing also rejects duplicate IDs and malformed/missing script containers.
    before, after = layout.Document(source), layout.Document(candidate)
    layout.require(len(before.blocks('script')) == len(after.blocks('script')) == 4, "Script ownership changed.")
    layout.require(before.blocks('script')[:-1] == after.blocks('script')[:-1], "Content or libraries changed.")


def validate_destination(destination):
    layout.require(not destination.is_symlink(), "Output directory cannot be a symlink.")
    destination = destination.resolve()
    layout.require(not any((p / '.git').exists() for p in [destination, *destination.parents]),
                   "Output must be outside every Git checkout.")
    if destination.exists() and any(destination.iterdir()):
        marker = destination / MARKER
        layout.require(marker.is_file() and not marker.is_symlink(), "Refusing to overwrite an unmanaged directory.")
        layout.require(json.loads(marker.read_text()).get('generator') == 'atlas-performance-prototype-v1', "Unknown preview owner.")
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file() or p.is_symlink()}
        layout.require(actual <= set(layout.ASSETS) | {MARKER}, "Unexpected preview files.")
    layout.require(not destination.exists() or not any(p.is_symlink() for p in destination.rglob('*')), "Preview contains symlinks.")
    return destination


def build(ref, destination, *, reader_layout=False):
    destination = validate_destination(destination)
    baseline = json.loads(layout.git_bytes(ref, 'project/asset-baseline.json'))
    expected = {a['path']: a for a in baseline['assets']}
    layout.require(set(expected) == set(layout.ASSETS), "Upstream publishing scope changed.")
    assets = {path: layout.git_bytes(ref, 'docs/' + path) for path in layout.ASSETS}
    for path, data in assets.items():
        layout.require(layout.digest(data) == expected[path]['sha256'] and len(data) == expected[path]['bytes'],
                       "Source asset disagrees with its own baseline: " + path)
    result, changes, layout_report = dict(assets), {}, None
    for edition in ['primary', 'young-explorers']:
        path = edition + '/index.html'
        source = assets[path].decode()
        if reader_layout and edition == 'primary':
            source, layout_report = layout.transform(source, (layout.PROTOTYPE / 'layout.css').read_text())
        candidate = transform(source)
        result[path] = candidate.encode()
        changes[edition] = {'source_runtime_sha256': layout.digest(layout.Document(source).blocks('script')[-1]),
                            'performance_runtime_sha256': layout.digest(layout.Document(candidate).blocks('script')[-1]),
                            'reversible_runtime_patch': True, 'embedded_content_and_original_guards_preserved': True}
    report = {'generator': 'atlas-performance-prototype-v1', 'checkpoint': 'PERF-1', 'source_commit': ref,
              'reader_layout': reader_layout, 'publication_cleared': False, 'editions': changes,
              'source_asset_sha256': {p: layout.digest(b) for p, b in assets.items()},
              'output_asset_sha256': {p: layout.digest(b) for p, b in result.items()},
              'builder_sha256': layout.digest(Path(__file__).read_bytes()),
              'renderer_sha256': layout.digest((PERFORMANCE / 'map-renderer.js').read_bytes()),
              'layout_builder_sha256': layout.digest((ROOT / 'scripts/build_layout_prototype.py').read_bytes()),
              'layout_composition': layout_report,
              'layout_input_sha256': {name: layout.digest((layout.PROTOTYPE / name).read_bytes())
                                      for name in ['layout.css', 'navigation.js', 'checkpoint.json']} if reader_layout else None}
    layout.require([p for p in layout.ASSETS if assets[p] != result[p]] == ['primary/index.html', 'young-explorers/index.html'],
                   'Unexpected changed asset set.')
    destination.mkdir(parents=True, exist_ok=True)
    for path, data in result.items():
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (destination / MARKER).write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-ref', default=json.loads((layout.PROTOTYPE / 'checkpoint.json').read_text())['content_commit'])
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--reader-layout', action='store_true', help='Compose Primary UI-1.8 before the runtime experiment.')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=8942)
    args = parser.parse_args()
    try:
        report = build(args.source_ref, args.output_dir, reader_layout=args.reader_layout)
        if args.verify:
            # Share the selected-checkpoint checks, but keep distinct preview ownership.
            # Its temporary fixture is the only place proposed asset hashes change.
            layout.verify_runtime(args.source_ref, args.output_dir.resolve(), report, marker=MARKER)
        print(json.dumps(report), flush=True)
        if args.serve:
            print(f"Performance preview: http://127.0.0.1:{args.port}/nj-name-atlas/primary/#town=0308", flush=True)
            ThreadingHTTPServer(('127.0.0.1', args.port), layout.preview_handler(args.output_dir.resolve())).serve_forever()
    except layout.ContractError as error:
        parser.exit(1, 'Performance contract failed: ' + str(error) + '\n')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
