// Exercise the actual adapter with invented DOM controls and scroll positions.
// No website data, browser profile, storage or network is available here.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

let assertions = 0;
const check = (value, label) => { assert.ok(value, label); assertions++; };
const microtasks = [], frames = [], listeners = {};
let active = false, observer, measure, focused, dialog = false, storyScrolls = 0, toolsHeight = 100, mapToolsHeight = 170;
let viewport = {zoom: 2, pan: [12, 34], county: 'Example', view: 'map'};
let reveals = 0, resultOpens = 0, selected = 'example-a';
const listObservers = {};
const classes = new Set(), styles = {};
const page = {scrollX: 0, scrollY: 0, innerHeight: 844, addEventListener(type, callback) { listeners['window-' + type] = callback; }, scrollTo({left, top}) { this.scrollX = left; this.scrollY = top; }};
class Element {
  constructor(id) { this.id = id; this.children = []; this.disabled = false; this.dataset = {}; this.attributes = {}; this.className = ''; this.scrollTop = 0; this.classList = {add: value => { this.className += ' ' + value; }}; }
  append(...nodes) { for (const node of nodes) { node.detach(); this.children.push(node); node.parentNode = this; } }
  detach() { if (this.parentNode) this.parentNode.children.splice(this.parentNode.children.indexOf(this), 1); }
  before(node) { const parent = this.parentNode, index = parent.children.indexOf(this); node.detach(); parent.children.splice(index, 0, node); node.parentNode = parent; }
  after(...nodes) { const parent = this.parentNode; let index = parent.children.indexOf(this) + 1; for (const node of nodes) { node.detach(); parent.children.splice(index++, 0, node); node.parentNode = parent; } }
  closest(selector) { if (selector === 'li') return this.parentNode; if (selector.startsWith('#')) { let node = this; while (node) { if (selector.split(', ').includes('#' + node.id)) return node; node = node.parentNode; } return null; } return this; }
  matches(selector) { return this.id === 'input' && selector.includes('input') || this.className.split(' ').some(c => c && selector.includes('.' + c)); }
  querySelectorAll(selector) { const all = this.children.flatMap(c => [c, ...c.querySelectorAll(selector)]); return all.filter(c => selector === 'a[data-index-town]' ? c.dataset.indexTown : c.className.split(' ').includes(selector.slice(1))); }
  querySelector(selector) { return this.querySelectorAll(selector)[0]; }
  setAttribute(name, value) { this.attributes[name] = value; }
  getAttribute(name) { return this.attributes[name] ?? null; }
  focus() { focused = this.id; }
  scrollIntoView() { storyScrolls++; page.scrollY = 444; }
  getBoundingClientRect() { return {height: this.id === 'map' ? mapToolsHeight : toolsHeight}; }
}
const ids = Object.fromEntries(['nj-name-atlas', 'atlas-map-stepper', 'atlas-story', 'atlas-reading-toggle', 'atlas-reader-show-map', 'atlas-browse-status', 'atlas-prev-town', 'atlas-next-town', 'atlas-search-match-list', 'atlas-town-index-list', 'atlas-state-view', 'atlas-county-view', 'atlas-open-map-story'].map(id => [id, new Element(id)]));
function result(listId, code) {
  const row = new Element('li'), link = new Element('a'); link.dataset.indexTown = code;
  link.id = listId + '-' + code;
  link.className = listId === 'atlas-search-match-list' ? 'search-town-link' : 'index-town-link';
  link.textContent = 'Example town';
  link.href = '#town=' + code; row.append(link); ids[listId].append(row); return {row, link};
}
const searchA = result('atlas-search-match-list', 'example-a'), searchB = result('atlas-search-match-list', 'example-b');
const indexA = result('atlas-town-index-list', 'example-a');
const root = ids['nj-name-atlas'], tools = new Element('tools'), map = new Element('map');
const stepper = ids['atlas-map-stepper'], status = ids['atlas-browse-status'], toggle = ids['atlas-reading-toggle'];
const county = ids['atlas-county-view'], statewide = ids['atlas-state-view'];
county.setAttribute('aria-label', 'Browse Example County'); county.setAttribute('aria-pressed', 'false');
map.append(statewide, county, stepper, status);
const locator = new Element('locator'); locator.append(ids['atlas-reader-show-map']);
root.classList = {contains: name => name === 'is-reading' ? active : classes.has(name), toggle: (name, on) => on ? classes.add(name) : classes.delete(name)};
root.style = {setProperty: (name, value) => { styles[name] = value; }};
root.querySelector = selector => selector === '.story-tools' ? tools : selector === '.layout-map-navigation' ? map : dialog ? {} : null;
root.addEventListener = (type, listener, capture) => { listeners[type + (capture ? '-capture' : '-bubble')] = listener; };
vm.runInNewContext(fs.readFileSync(new URL('../prototypes/primary-layout/navigation.js', import.meta.url), 'utf8') + '({readViewport, restoreViewport, revealTown, resultContext, selectedTown, openResult});', {
  resultContext: () => 'Example County · Borough',
  selectedTown: () => selected,
  openResult: () => { resultOpens++; active = true; frames.push(() => { focused = toggle.id; page.scrollY = 100; }); },
  readViewport: () => structuredClone(viewport),
  restoreViewport: saved => { viewport = structuredClone(saved); },
  revealTown: () => { reveals++; },
  document: {getElementById: id => ids[id], createComment: () => new Element('home'), createElement: tag => new Element(tag)},
  window: page,
  MutationObserver: class { constructor(callback) { this.callback = callback; } observe(target) { if (target === root) observer = this.callback; else listObservers[target.id] = this.callback; } },
  ResizeObserver: class { constructor(callback) { measure = callback; } observe() {} },
  queueMicrotask: callback => microtasks.push(callback),
  requestAnimationFrame: callback => frames.push(callback),
});
const flush = () => { while (microtasks.length) microtasks.shift()(); while (frames.length) frames.shift()(); };
function event(type, target, original, extra = {}) {
  if (type === 'click' && target.disabled) return;
  const e = {target, button: 0, defaultPrevented: false, ...extra};
  listeners[type + '-capture']?.(e);
  // Browsers may flush microtasks between event listeners. Restoration must
  // still follow the original target handler and its queued focus frame.
  while (microtasks.length) microtasks.shift()();
  original(e); observer();
  listeners[type + '-bubble']?.(e);
  listeners['window-' + type]?.(e);
  measure(); flush();
}
function enter(y) {
  page.scrollY = y;
  event('click', toggle, () => { active = true; frames.push(() => { page.scrollY = 100; }); });
}
function originalExit() {
  active = false;
  frames.push(() => { page.scrollY = 99; });
}
check(stepper.parentNode === map, 'Browse navigation starts in its original panel');
enter(850);
check(stepper.parentNode === tools && status.parentNode === tools, 'Reading reuses the navigation and its live status');
check(page.scrollY === 100, 'Entry leaves the runtime scroll behavior intact');
toolsHeight = 300; measure();
check(classes.has('layout-tall-navigation') && styles['--layout-toolbar-offset'] === '12px', 'Oversized navigation stops covering the article');
toolsHeight = 100; measure();
check(!classes.has('layout-tall-navigation') && styles['--layout-toolbar-offset'] === '160px', 'Compact navigation restores sticky-target clearance');
page.scrollY = 1777;
event('click', ids['atlas-next-town'], () => { focused = 'atlas-next-town'; viewport.pan = [99, 88]; });
check(page.scrollY === 444 && storyScrolls === 1, 'Next town opens at the story top');
check(focused === 'atlas-next-town', 'Original navigation focus is retained');
event('click', toggle, originalExit);
check(page.scrollY === 850 && focused === toggle.id, 'Return restores the initial browse position after stepping');
check(viewport.pan[0] === 12 && viewport.pan[1] === 34 && viewport.zoom === 2, 'Return restores the saved map viewport after automatic reframing');
check(stepper.parentNode === map && status.parentNode === map, 'The same controls return to their original panel');
enter(920);
ids['atlas-prev-town'].disabled = true;
event('click', ids['atlas-prev-town'], () => {});
check(storyScrolls === 1, 'Disabled boundary controls do not scroll');
event('keydown', new Element('input'), () => {}, {key: 'Escape'});
check(active && page.scrollY === 100, 'Escape in an input leaves the reader alone');
dialog = true;
event('keydown', toggle, () => {}, {key: 'Escape'});
check(active && page.scrollY === 100, 'Dialog Escape is left to the original dialog');
dialog = false;
event('keydown', toggle, originalExit, {key: 'Escape'});
check(page.scrollY === 920 && focused === toggle.id, 'Escape restores the browse position after original focus work');
enter(1020);
event('click', ids['atlas-reader-show-map'], () => { active = false; viewport.pan = [77, 66]; frames.push(() => { page.scrollY = 700; }); });
check(page.scrollY === 700, 'Explicit Show on map retains its original destination');
check(viewport.pan[0] === 77 && ids['atlas-reader-show-map'].parentNode === locator, 'Show on map keeps the runtime framing and returns its single control home');
check(reveals === 1, 'Explicit map reveal requests the original selected-town framing');
active = true; observer();
event('click', toggle, originalExit);
check(page.scrollY === 99, 'A fresh deep link has no stale browse position to restore');
enter(1120);
event('keydown', toggle, () => {}, {key: 'Escape', defaultPrevented: true});
check(active && page.scrollY === 100, 'An already-handled Escape is not intercepted');
event('click', toggle, () => {});
check(active && page.scrollY === 100, 'A cancelled reading exit does not restore scroll');
event('click', toggle, originalExit);
check(searchA.row.dataset.selected === 'true' && searchA.link.attributes['aria-current'] === 'true' &&
      searchB.row.dataset.selected === 'false', 'Search exposes the original selection without another selection state');
check(searchA.row.querySelector('.layout-result-context').textContent === 'Example County · Borough', 'Search adds county/form context from the read-only bridge');
check(indexA.row.querySelectorAll('.layout-result-context').length === 0, 'Index retains its original context');
check(searchA.link.querySelector('.layout-result-cue').textContent === 'Read story' && searchA.link.href === '#town=example-a', 'The original native link keeps its route and gains a visible action cue');
check(searchA.link.attributes['aria-label'] === 'Example town · Example County · Borough. Read story.', 'Accessible result names include county context and the action');
listObservers['atlas-search-match-list']();
check(searchA.link.querySelectorAll('.layout-result-cue').length === 1 && searchA.row.querySelectorAll('.layout-result-context').length === 1, 'Repeated decoration adds no duplicate cue or context');
for (const extra of [{ctrlKey: true}, {metaKey: true}, {shiftKey: true}, {altKey: true}, {button: 1}]) {
  event('click', searchB.link, () => {}, extra);
}
check(resultOpens === 0 && !active, 'Modified and middle activations retain native link behavior');
event('click', searchB.link, () => {});
check(resultOpens === 0, 'An unhandled result click does not open reading');
viewport.view = 'index'; page.scrollY = 600; ids['atlas-town-index-list'].scrollTop = 275;
event('click', indexA.link, e => { selected = 'example-a'; e.defaultPrevented = true; page.scrollY = 900; });
check(resultOpens === 1 && active && focused === toggle.id, 'A handled result opens reading after original selection and retains original reading focus');
ids['atlas-town-index-list'].scrollTop = 0;
event('click', toggle, originalExit);
check(page.scrollY === 600 && ids['atlas-town-index-list'].scrollTop === 275, 'Returning from an index result restores page and inner index scroll');
check(focused === indexA.link.id, 'Returning from a result restores focus to its current original link');
const fresh = result('atlas-search-match-list', 'example-b'); selected = 'example-b';
listObservers['atlas-search-match-list']();
check(fresh.row.dataset.selected === 'true' && fresh.link.attributes['aria-current'] === 'true', 'New runtime results are decorated with the current selection');
viewport.view = 'map'; measure();
check(!classes.has('layout-tall-map-navigation') && styles['--layout-map-toolbar-offset'] === '194px', 'Compact map controls reserve scroll clearance');
mapToolsHeight = 300; measure();
check(classes.has('layout-tall-map-navigation') && styles['--layout-map-toolbar-offset'] === '12px', 'Oversized map controls scroll normally');
mapToolsHeight = 170; page.innerHeight = 320; listeners['window-resize']();
check(classes.has('layout-tall-map-navigation'), 'A short landscape viewport also disables map stickiness');
page.innerHeight = 844; measure();
check(!classes.has('layout-tall-map-navigation'), 'Restoring viewport space restores compact map navigation');
check(statewide.textContent === 'Reset statewide map' && county.textContent === 'Zoom to Example County', 'Unfiltered map labels identify the reset and county-zoom actions');
county.setAttribute('aria-label', 'Browse Another County'); county.setAttribute('aria-pressed', 'true');
listObservers['atlas-county-view'](); listObservers['atlas-county-view']();
check(statewide.textContent === 'Show all New Jersey' && county.textContent === 'Reset Another County', 'County labels follow runtime changes and remain stable under a second observation');
check(county.getAttribute('aria-pressed') === 'true' && county.getAttribute('aria-label') === county.textContent, 'Relabeling preserves the original pressed state and visible accessible name');
event('click', ids['atlas-open-map-story'], () => { active = true; });
event('click', toggle, originalExit);
check(focused === 'atlas-open-map-story', 'Returning from the map story action restores focus to that original action');
console.log(JSON.stringify({status: 'PASS', assertions, scope: 'Actual prototype navigation adapter with invented controls and scroll values; no browser storage, historical content or network.'}));
