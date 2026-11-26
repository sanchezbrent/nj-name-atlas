/* Prototype navigation only. The original runtime owns towns, filters and maps.
   No content parsing, storage, network, history or duplicated selection state. */
((viewportApi) => {
  'use strict';
  const {readViewport, restoreViewport, revealTown} = viewportApi;
  const root = document.getElementById('nj-name-atlas');
  const stepper = document.getElementById('atlas-map-stepper');
  const tools = root?.querySelector('.story-tools');
  const story = document.getElementById('atlas-story');
  const toggle = document.getElementById('atlas-reading-toggle');
  const status = document.getElementById('atlas-browse-status');
  const showMap = document.getElementById('atlas-reader-show-map');
  if (!root || !stepper || !tools || !story || !toggle || !status || !showMap) return;

  const home = document.createComment('Original town navigation position');
  stepper.before(home);
  const mapHome = document.createComment('Original locator action position');
  showMap.before(mapHome);
  const reading = () => root.classList.contains('is-reading');
  let wasReading = reading();
  let browseReturn = null;
  const placeNavigation = () => {
    const active = reading();
    if (active && stepper.parentNode !== tools) tools.append(showMap, stepper, status);
    if (!active && stepper.parentNode !== home.parentNode) {
      home.after(stepper, status);
      mapHome.after(showMap);
    }
    if (active !== wasReading) {
      if (!active) browseReturn = null;
      wasReading = active;
    }
  };
  new MutationObserver(placeNavigation).observe(root, {attributes: true, attributeFilter: ['class']});
  placeNavigation();
  if (typeof ResizeObserver !== 'undefined') {
    const sizeNavigation = () => {
      if (!reading()) return;
      const height = Math.ceil(tools.getBoundingClientRect().height);
      const tall = height > Math.min(200, window.innerHeight / 3);
      root.classList.toggle('layout-tall-navigation', tall);
      root.style.setProperty('--layout-toolbar-offset', tall ? '12px' : Math.max(160, height + 12) + 'px');
    };
    new ResizeObserver(sizeNavigation).observe(tools);
    window.addEventListener('resize', sizeNavigation);
  }

  // Capture before the runtime changes layout; act while bubbling after its
  // target handler, so its focus frame is queued before our restoration frame.
  const clicks = new WeakMap();
  root.addEventListener('click', event => {
    const control = event.target.closest('button, a');
    if (reading() && control?.id === 'atlas-reader-show-map') revealTown();
    clicks.set(event, {active: reading(), position: {left: window.scrollX, top: window.scrollY, viewport: readViewport()},
      returning: browseReturn, control});
  }, true);
  root.addEventListener('click', event => {
    const before = clicks.get(event);
    if (!before) return;
    const {control} = before;
    if (!before.active) { if (reading()) browseReturn = before.position; return; }
    if (control?.id === 'atlas-reading-toggle') {
      const position = before.returning;
      requestAnimationFrame(() => {
        if (!reading() && position) {
          restoreViewport(position.viewport);
          toggle.focus({preventScroll: true});
          window.scrollTo({left: position.left, top: position.top, behavior: 'instant'});
        }
      });
    } else if (control &&
               ['atlas-prev-town', 'atlas-next-town', 'atlas-open-map-story'].includes(control.id)) {
      requestAnimationFrame(() => { if (reading()) story.scrollIntoView({behavior: 'instant', block: 'start'}); });
    }
  });
  const escapes = new WeakMap();
  root.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || !reading() || event.defaultPrevented ||
        event.target.matches('input, select, textarea') || root.querySelector('dialog[open]')) return;
    escapes.set(event, browseReturn);
  }, true);
  window.addEventListener('keydown', event => {
    const position = escapes.get(event);
    if (!position) return;
    requestAnimationFrame(() => {
      if (!reading() && position) {
        restoreViewport(position.viewport);
        toggle.focus({preventScroll: true});
        window.scrollTo({left: position.left, top: position.top, behavior: 'instant'});
      }
    });
  });
})
