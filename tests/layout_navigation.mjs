// Exercise the actual adapter with invented DOM controls and scroll positions.
// No website data, browser profile, storage or network is available here.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

let assertions = 0;
const check = (value, label) => { assert.ok(value, label); assertions++; };
const microtasks = [], frames = [], listeners = {};
let active = false, observer, measure, focused, dialog = false, storyScrolls = 0, toolsHeight = 100;
let viewport = {zoom: 2, pan: [12, 34], county: 'Example', view: 'map'};
let reveals = 0;
const classes = new Set(), styles = {};
const page = {scrollX: 0, scrollY: 0, innerHeight: 844, addEventListener(type, callback) { listeners['window-' + type] = callback; }, scrollTo({left, top}) { this.scrollX = left; this.scrollY = top; }};
class Element {
  constructor(id) { this.id = id; this.children = []; this.disabled = false; }
  append(...nodes) { for (const node of nodes) { node.detach(); this.children.push(node); node.parentNode = this; } }
  detach() { if (this.parentNode) this.parentNode.children.splice(this.parentNode.children.indexOf(this), 1); }
  before(node) { const parent = this.parentNode, index = parent.children.indexOf(this); node.detach(); parent.children.splice(index, 0, node); node.parentNode = parent; }
  after(...nodes) { const parent = this.parentNode; let index = parent.children.indexOf(this) + 1; for (const node of nodes) { node.detach(); parent.children.splice(index++, 0, node); node.parentNode = parent; } }
  closest() { return this; }
  matches(selector) { return this.id === 'input' && selector.includes('input'); }
  focus() { focused = this.id; }
  scrollIntoView() { storyScrolls++; page.scrollY = 444; }
  getBoundingClientRect() { return {height: toolsHeight}; }
}
const ids = Object.fromEntries(['nj-name-atlas', 'atlas-map-stepper', 'atlas-story', 'atlas-reading-toggle', 'atlas-reader-show-map', 'atlas-browse-status', 'atlas-prev-town', 'atlas-next-town'].map(id => [id, new Element(id)]));
const root = ids['nj-name-atlas'], tools = new Element('tools'), map = new Element('map');
const stepper = ids['atlas-map-stepper'], status = ids['atlas-browse-status'], toggle = ids['atlas-reading-toggle'];
map.append(stepper, status);
const locator = new Element('locator'); locator.append(ids['atlas-reader-show-map']);
root.classList = {contains: name => name === 'is-reading' ? active : classes.has(name), toggle: (name, on) => on ? classes.add(name) : classes.delete(name)};
root.style = {setProperty: (name, value) => { styles[name] = value; }};
root.querySelector = selector => selector === '.story-tools' ? tools : dialog ? {} : null;
root.addEventListener = (type, listener, capture) => { listeners[type + (capture ? '-capture' : '-bubble')] = listener; };
vm.runInNewContext(fs.readFileSync(new URL('../prototypes/primary-layout/navigation.js', import.meta.url), 'utf8') + '({readViewport, restoreViewport, revealTown});', {
  readViewport: () => structuredClone(viewport),
  restoreViewport: saved => { viewport = structuredClone(saved); },
  revealTown: () => { reveals++; },
  document: {getElementById: id => ids[id], createComment: () => new Element('home')},
  window: page,
  MutationObserver: class { constructor(callback) { observer = callback; } observe() {} },
  ResizeObserver: class { constructor(callback) { measure = callback; } observe() {} },
  queueMicrotask: callback => microtasks.push(callback),
  requestAnimationFrame: callback => frames.push(callback),
});
const flush = () => { while (microtasks.length) microtasks.shift()(); while (frames.length) frames.shift()(); };
function event(type, target, original, extra = {}) {
  if (type === 'click' && target.disabled) return;
  const e = {target, defaultPrevented: false, ...extra};
  listeners[type + '-capture']?.(e);
  // Browsers may flush microtasks between event listeners. Restoration must
  // still follow the original target handler and its queued focus frame.
  while (microtasks.length) microtasks.shift()();
  original(); observer();
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
console.log(JSON.stringify({status: 'PASS', assertions, scope: 'Actual prototype navigation adapter with invented controls and scroll values; no browser storage, historical content or network.'}));
