/* Prototype navigation only. The original runtime owns towns, filters and maps.
   No narrative parsing, storage, network, history or duplicated selection state. */
((viewportApi) => {
  'use strict';
  const {readViewport, restoreViewport, revealTown, resultContext, selectedTown, openResult} = viewportApi;
  const root = document.getElementById('nj-name-atlas');
  const stepper = document.getElementById('atlas-map-stepper');
  const tools = root?.querySelector('.story-tools');
  const story = document.getElementById('atlas-story');
  const toggle = document.getElementById('atlas-reading-toggle');
  const status = document.getElementById('atlas-browse-status');
  const showMap = document.getElementById('atlas-reader-show-map');
  if (!root || !stepper || !tools || !story || !toggle || !status || !showMap) return;
  const mapNavigation = root.querySelector('.layout-map-navigation');
  const stateView = document.getElementById('atlas-state-view');
  const countyView = document.getElementById('atlas-county-view');
  if (mapNavigation && stateView && countyView) {
    for (const control of [stateView, countyView]) control.title = 'Reset the map area and zoom; keep search and origin filters.';
    let countyLabel = '';
    const copy = (control, text) => {
      if (control.textContent !== text) control.textContent = text;
      if (control.getAttribute('aria-label') !== text) control.setAttribute('aria-label', text);
    };
    const scopeLabels = () => {
      // The runtime supplies this label after every render. Retain only the
      // county's display label when our own copy triggers a second observation.
      const label = countyView.getAttribute('aria-label') || '';
      if (label.startsWith('Browse ')) countyLabel = label.slice(7);
      const countyActive = countyView.getAttribute('aria-pressed') === 'true';
      copy(stateView, countyActive ? 'Show all New Jersey' : 'Reset statewide map');
      copy(countyView, countyLabel ? (countyActive ? 'Reset ' : 'Zoom to ') + countyLabel : 'Choose a county');
    };
    const observer = new MutationObserver(scopeLabels);
    observer.observe(countyView, {childList: true, attributes: true, attributeFilter: ['aria-label', 'aria-pressed']});
    scopeLabels();
  }

  // Decorate the original result links after each runtime render. Observe only
  // direct list replacements, so adding cues below cannot trigger itself.
  const decorateResults = list => {
    for (const link of list.querySelectorAll('a[data-index-town]')) {
      if (link.querySelector('.layout-result-cue')) continue;
      const row = link.closest('li'), code = link.dataset.indexTown;
      if (!row) continue;
      row.classList.add('layout-result');
      const contextText = resultContext(code);
      link.setAttribute('aria-label', link.textContent + ' · ' + contextText + '. Read story.');
      if (list.id === 'atlas-search-match-list') {
        const context = document.createElement('p');
        context.className = 'layout-result-context';
        context.textContent = contextText;
        link.after(context);
      }
      const selected = selectedTown() === code;
      row.dataset.selected = String(selected);
      if (selected) {
        link.setAttribute('aria-current', 'true');
        const marker = document.createElement('span');
        marker.className = 'layout-result-selected'; marker.textContent = 'Selected';
        link.append(marker);
      }
      const cue = document.createElement('span');
      cue.className = 'layout-result-cue'; cue.textContent = 'Read story';
      link.append(cue);
    }
  };
  for (const id of ['atlas-search-match-list', 'atlas-town-index-list']) {
    const list = document.getElementById(id);
    if (!list) continue;
    new MutationObserver(() => decorateResults(list)).observe(list, {childList: true});
    decorateResults(list);
  }

  const home = document.createComment('Original town navigation position');
  stepper.before(home);
  const mapHome = document.createComment('Original locator action position');
  showMap.before(mapHome);
  const reading = () => root.classList.contains('is-reading');
  let wasReading = reading();
  let browseReturn = null;
  const restorePosition = position => {
    restoreViewport(position.viewport);
    const current = readViewport();
    if (current.view === 'index' && position.viewport.view === 'index' && current.county === position.viewport.county) {
      document.getElementById('atlas-town-index-list').scrollTop = position.indexTop;
    }
    const links = document.getElementById(position.resultList)?.querySelectorAll('a[data-index-town]') || [];
    const origin = Array.from(links).find(link => link.dataset.indexTown === position.resultCode);
    (origin || document.getElementById(position.mapControl) || toggle).focus({preventScroll: true});
    window.scrollTo({left: position.left, top: position.top, behavior: 'instant'});
  };
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
      if (!reading()) {
        if (mapNavigation) {
          const height = Math.ceil(mapNavigation.getBoundingClientRect().height);
          const tall = height > Math.min(220, window.innerHeight / 3);
          root.classList.toggle('layout-tall-map-navigation', tall);
          root.style.setProperty('--layout-map-toolbar-offset', tall ? '12px' : height + 24 + 'px');
        }
        return;
      }
      const height = Math.ceil(tools.getBoundingClientRect().height);
      const tall = height > Math.min(200, window.innerHeight / 3);
      root.classList.toggle('layout-tall-navigation', tall);
      root.style.setProperty('--layout-toolbar-offset', tall ? '12px' : Math.max(160, height + 12) + 'px');
    };
    const observer = new ResizeObserver(sizeNavigation);
    observer.observe(tools);
    if (mapNavigation) observer.observe(mapNavigation);
    window.addEventListener('resize', sizeNavigation);
    sizeNavigation();
  }

  // Capture before the runtime changes layout; act while bubbling after its
  // target handler, so its focus frame is queued before our restoration frame.
  const clicks = new WeakMap();
  root.addEventListener('click', event => {
    const control = event.target.closest('button, a');
    const result = control?.matches('.search-town-link, .index-town-link');
    if (reading() && control?.id === 'atlas-reader-show-map') revealTown();
    clicks.set(event, {active: reading(), position: {left: window.scrollX, top: window.scrollY,
      resultCode: result ? control.dataset.indexTown : null,
      mapControl: control?.id === 'atlas-open-map-story' ? control.id : null,
      resultList: result ? control.closest('#atlas-search-match-list, #atlas-town-index-list')?.id : null,
      indexTop: document.getElementById('atlas-town-index-list')?.scrollTop || 0, viewport: readViewport()},
      returning: browseReturn, control});
  }, true);
  root.addEventListener('click', event => {
    const before = clicks.get(event);
    if (!before) return;
    const {control} = before;
    if (!before.active) {
      // The original anchor handler has already selected the town and updated
      // its route. Only its handled plain activation enters reading here.
      if (control?.matches('.search-town-link, .index-town-link') && event.defaultPrevented &&
          event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) openResult();
      if (reading()) browseReturn = before.position;
      return;
    }
    if (control?.id === 'atlas-reading-toggle') {
      const position = before.returning;
      requestAnimationFrame(() => {
        if (!reading() && position) {
          restorePosition(position);
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
        restorePosition(position);
      }
    });
  });
})
