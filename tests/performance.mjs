// Compare the real original map block and the retained renderer with real data.
// A minimal SVG model measures JS/geometry and deterministic work, not browser paint.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {performance} from 'node:perf_hooks';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = process.argv[2] || fileURLToPath(new URL('..', import.meta.url));
const helper = fs.readFileSync(new URL('../prototypes/performance/map-renderer.js', import.meta.url), 'utf8');
const patchSource = fs.readFileSync(new URL('../scripts/build_performance_prototype.py', import.meta.url), 'utf8');
const oldMenu = patchSource.match(/OLD_MENU = """([\s\S]*?)"""/)[1];
const newMenu = patchSource.match(/NEW_MENU = """([\s\S]*?)"""/)[1];
const makeRetained = vm.runInNewContext(helper + ';createAtlasRetainedMap;');
let assertions = 0;
const same = (a, b, message) => { assert.deepEqual(a, b, message); assertions++; };
const results = [];

class SvgNode {
  constructor(tag, counters) { this.tag = tag; this.attributes = {}; this.children = []; this.parent = null; this.textContent = ''; this.listeners = {}; this.counters = counters; this.style = {setProperty: (key, value) => { this.color = value; }}; counters.nodes++; }
  getAttribute(key) { return this.attributes[key] ?? null; }
  setAttribute(key, value) { this.attributes[key] = String(value); this.counters.attributes++; }
  detach() { if (this.parent) this.parent.children.splice(this.parent.children.indexOf(this), 1); }
  append(...nodes) { for (const node of nodes) { node.detach(); node.parent = this; this.children.push(node); } }
  insertBefore(node, before) { node.detach(); node.parent = this; const i = before ? this.children.indexOf(before) : this.children.length; assert.ok(i >= 0); this.children.splice(i, 0, node); }
  replaceChildren() { for (const child of this.children) child.parent = null; this.children = []; }
  addEventListener(type, fn) { this.listeners[type] = fn; this.counters.listeners++; }
  fire(type) { this.listeners[type]?.(); }
}

for (const edition of ['primary', 'young-explorers']) {
  const html = fs.readFileSync(path.join(root, 'docs', edition, 'index.html'), 'utf8');
  assert.ok(html.includes(oldMenu), 'actual original menu matches bounded patch');
  function menuHarness(cached) {
    let allocations = 0;
    const select = {children: [], replaceChildren(...options) { this.children = options; }, append(option) { this.children.push(option); }};
    const draw = vm.runInNewContext("(()=>{let atlasTownMenuSignature='';return ({state,$,option,displayName,profiles})=>{" +
      (cached ? newMenu : oldMenu) + '\nselect.value=state.town;select.disabled=!state.matching.length;};})()');
    return {select, allocations: () => allocations, draw(state) { draw({state, $: () => select,
      option: (value, text) => { allocations++; return {value, text}; }, displayName: code => 'Town ' + code,
      profiles: {a: {county: 'One'}, b: {county: 'Two'}}}); }};
  }
  const oldDropdown = menuHarness(false), newDropdown = menuHarness(true);
  let firstOptions;
  for (const [i, state] of [
    {matching: ['a', 'b'], county: '', town: 'a'}, {matching: ['a', 'b'], county: '', town: 'b'},
    {matching: ['a', 'b'], county: 'One', town: 'b'}, {matching: ['a'], county: 'One', town: 'a'},
    {matching: [], county: 'One', town: ''}, {matching: ['a', 'b'], county: '', town: 'a'},
  ].entries()) {
    oldDropdown.draw(state); newDropdown.draw(state);
    const menuState = h => ({children: h.select.children, value: h.select.value, disabled: h.select.disabled});
    same(menuState(newDropdown), menuState(oldDropdown), edition + ' exact dropdown state ' + i);
    if (i === 0) firstOptions = newDropdown.select.children;
    if (i === 1) same(newDropdown.select.children === firstOptions, true, edition + ' selection-only change retains options');
  }
  same(newDropdown.allocations(), oldDropdown.allocations() - 3, edition + ' unchanged dropdown allocates no options');
  const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)];
  const decode = vm.runInNewContext(html.slice(html.indexOf('async function decodeAtlasPacked('), html.indexOf('\n  let data;')) + ';decodeAtlasPacked;',
    {Uint8Array, atob, Response, Blob, DecompressionStream, TextDecoder, TextEncoder, crypto: globalThis.crypto});
  const packed = JSON.parse(scripts.find(s => s[1].includes('atlas-pilot-data'))[2]);
  const pilot = await decode(packed.payload, packed.sha256);
  const base = html.match(/data=await decodeAtlasPacked\("([^"]+)",\s*"([^"]+)"\)/);
  const data = await decode(base[1], base[2]);
  const packedOverlay = JSON.parse(html.split('  const packedCategoryOverlay=')[1].split(';\n')[0]);
  const overlay = await decode(packedOverlay.payload, packedOverlay.sha256);
  const makeCore = vm.runInNewContext(html.slice(html.indexOf('function createAtlasPilotCore('), html.indexOf('\n  const packedPayload=')) + ';createAtlasPilotCore;');
  const core = makeCore(pilot, data);
  const themes = vm.runInNewContext(html.match(/const themes=\[[\s\S]*?\n  \];/)[0] + ';themes;');
  const byTheme = Object.fromEntries(themes.map(t => [t.id, t]));
  const apply = vm.runInNewContext(html.slice(html.indexOf('function applyReviewedCategoryOverlay('), html.indexOf('\n\n  const packedCategoryOverlay=')) + ';applyReviewedCategoryOverlay;');
  const sourceProfiles = {...data.profiles, ...Object.fromEntries(Object.keys(pilot.views).map(c => [c, core.profileFor(c)]))};
  const profiles = apply(sourceProfiles, core, pilot, overlay);
  const libraryContext = {}; vm.runInNewContext(scripts[1][2], libraryContext);
  const d3 = libraryContext.d3;
  const ringStart = html.indexOf('    function decodeRing(s)');
  const decodeRing = vm.runInNewContext(html.slice(ringStart, html.indexOf('\n    for(const collection', ringStart)) + ';decodeRing;');
  for (const collection of [data.geography, data.counties, data.context]) for (const feature of collection.features) {
    const g = feature.geometry; g.coordinates = g.type === 'Polygon' ? g.coordinates.map(decodeRing) : g.coordinates.map(p => p.map(decodeRing));
    for (const p of g.type === 'Polygon' ? [g.coordinates] : g.coordinates) if (d3.geoArea({type: 'Polygon', coordinates: p}) > 2 * Math.PI) p.forEach(r => r.reverse());
  }
  const features = data.geography.features, codes = features.map(f => f.properties.code);
  const njLand = data.context.features.find(f => f.id === '34');
  const start = html.indexOf("    $('atlas-land-mask').setAttribute('d',path(njLand));", html.indexOf('  function drawMap(){'));
  const end = html.indexOf('\n    if(!state.county&&state.zoom<1.5', start);
  assert.ok(start > 0 && end > start, 'original renderer boundary');
  const originalBlock = vm.runInNewContext('(api)=>{const {$,path,njLand,data,features,state,profiles,byTheme,svgEl,colorFor,storyHookFor,mapConnectionForCode,drag,activateMappedTown,showMapPreview}=api;' + html.slice(start, end) + '\n}');

  function harness(retained) {
    const counters = {nodes: 0, listeners: 0, attributes: 0, guards: 0, paths: 0};
    const events = [];
    const svgEl = (tag, attrs, text) => { const node = new SvgNode(tag, counters); for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v); if (text !== undefined) node.textContent = String(text); return node; };
    const layers = Object.fromEntries(['atlas-land-mask', 'atlas-context', 'atlas-municipalities', 'atlas-boundaries', 'atlas-labels', 'atlas-selection', 'atlas-map-hover'].map(id => [id, svgEl('g')]));
    let matches, connections;
    const drag = {didMove: false};
    const activateMappedTown = code => events.push(['activate', code]);
    const showMapPreview = (code, active) => events.push(['preview', code, active]);
    const storyHookFor = code => { counters.guards++; return core.hasPilot(code) ? core.editorialFor(code)?.preview || '' : ''; };
    const colorFor = code => byTheme[profiles[code].current_origin].color;
    const render = makeRetained({features, contextFeatures: data.context.features, countyFeatures: data.counties.features, land: njLand, profiles, byTheme, colorFor, storyHookFor, svgEl,
      activate: code => { if (!drag.didMove) activateMappedTown(code); }, preview: showMapPreview, hidePreview: () => { layers['atlas-map-hover'].hidden = true; }});
    return {counters, layers, events, drag, draw(frame) {
      matches = new Set(frame.matching); connections = new Map(frame.connections.map(c => [c.other, c]));
      const projection = d3.geoMercator().fitExtent([[50, 24], [550, 757]], njLand).scale(frame.scale).translate(frame.translate);
      const geoPath = d3.geoPath(projection);
      const path = feature => { counters.paths++; return geoPath(feature); };
      if (retained) render({key: JSON.stringify([frame.scale, frame.translate]), path, context: layers['atlas-context'], shapes: layers['atlas-municipalities'], boundaries: layers['atlas-boundaries'], mask: layers['atlas-land-mask'], matches, selected: frame.town, connections: frame.connections});
      else originalBlock({$: id => layers[id], path, njLand, data, features, state: {town: frame.town, matching: frame.matching}, profiles, byTheme, svgEl, colorFor, storyHookFor,
        mapConnectionForCode: code => connections.get(code), drag, activateMappedTown, showMapPreview});
    }};
  }
  const original = harness(false), retained = harness(true);
  const baseProjection = d3.geoMercator().fitExtent([[50, 24], [550, 757]], njLand);
  const defaults = {matching: codes, town: codes[0], connections: [], scale: baseProjection.scale(), translate: baseProjection.translate()};
  const subset = codes.filter((c, i) => i % 3 === 0);
  const frames = [defaults, {...defaults, matching: subset}, {...defaults, town: codes[3], connections: [{other: codes[1], label: 'Test relationship'}]},
    {...defaults, town: codes[2]}, {...defaults, town: codes[0]}, {...defaults, matching: [], town: ''},
    {...defaults, translate: [defaults.translate[0] + 47, defaults.translate[1] - 21]},
    {...defaults, scale: defaults.scale * 1.6}, defaults];
  const snapshot = h => Object.fromEntries(['atlas-land-mask', 'atlas-context', 'atlas-municipalities', 'atlas-boundaries'].map(id => {
    const layer = h.layers[id]; return [id, {attributes: {...layer.attributes}, children: layer.children.map(n => ({attributes: {...n.attributes}, color: n.color, title: n.children[0]?.textContent}))}];
  }));
  let firstNode;
  for (let i = 0; i < frames.length; i++) {
    original.draw(frames[i]); retained.draw(frames[i]);
    same(snapshot(retained), snapshot(original), edition + ' exact paths/order/classes/titles frame ' + i);
    const code = codes[1];
    const oldNode = original.layers['atlas-municipalities'].children.find(n => n.attributes['data-code'] === code);
    const newNode = retained.layers['atlas-municipalities'].children.find(n => n.attributes['data-code'] === code);
    firstNode ||= newNode;
    same(newNode === firstNode, true, edition + ' retains the same municipality node');
    original.events.length = retained.events.length = 0;
    oldNode.fire('click'); newNode.fire('click'); oldNode.fire('pointerenter'); newNode.fire('pointerenter');
    same(retained.events, original.events, edition + ' fresh filter/connection handlers frame ' + i);
  }
  original.drag.didMove = retained.drag.didMove = true;
  original.events.length = retained.events.length = 0;
  for (const h of [original, retained]) h.layers['atlas-municipalities'].children[0].fire('click');
  same(retained.events, [], edition + ' drag never activates a town');
  same(retained.counters.guards, 564, edition + ' exactly one guarded title per town per document');
  same(retained.counters.listeners, 564 * 3, edition + ' listeners allocated only once');
  const warm = {...retained.counters}; retained.draw(defaults);
  same(retained.counters.paths, warm.paths, edition + ' unchanged viewport serializes no paths');
  same(retained.counters.nodes, warm.nodes, edition + ' unchanged viewport allocates no nodes');

  const median = values => values.sort((a, b) => a - b)[Math.floor(values.length / 2)];
  function measure(retain, pan) {
    const h = harness(retain); h.draw(defaults);
    const before = {...h.counters}, times = [];
    for (let i = 0; i < 7; i++) {
      const frame = pan ? {...defaults, translate: [defaults.translate[0] + (i + 1) * 3, defaults.translate[1] + i]} : {...defaults, matching: i % 2 ? codes : subset};
      const t = performance.now(); h.draw(frame); times.push(performance.now() - t);
    }
    return {median_ms: +median(times).toFixed(2), totals: Object.fromEntries(Object.entries(h.counters).map(([k, v]) => [k, v - before[k]]))};
  }
  const unchanged = {before: measure(false, false), after: measure(true, false)};
  const panning = {before: measure(false, true), after: measure(true, true)};
  for (const [name, sample] of [['unchanged viewport', unchanged], ['panning', panning]]) {
    for (const counter of ['nodes', 'listeners', 'guards']) same(sample.after.totals[counter], 0, edition + ' ' + name + ' reuses ' + counter);
  }
  results.push({edition, profiles: codes.length, frames_compared: frames.length,
    unchanged_viewport: unchanged, panning});
}
console.log(JSON.stringify({status: 'PASS', assertions, scope: 'Actual source data, guards, D3 geometry and original renderer block; minimal SVG model, excludes browser layout/paint and other map layers. Timings informative, deterministic allocation/path/guard assertions enforced.', results}, null, 2));
