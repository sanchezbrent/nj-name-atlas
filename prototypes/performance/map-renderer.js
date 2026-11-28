/* Render immutable, checkpoint-bound geography without recreating its DOM.
   The original runtime still owns projections, selection, filters and guards.
   Titles are validated on node creation; a new document creates a new renderer.
   There is no mutable content/editor API in a loaded atlas document. */
function createAtlasRetainedMap({features, contextFeatures, countyFeatures, land,
  profiles, byTheme, colorFor, storyHookFor, svgEl, activate, preview, hidePreview}) {
  const towns = new Map(), contexts = [], counties = [];
  const featureIndex = new Map(features.map((f, i) => [f.properties.code, i]));
  let geometryKey = null, selectedBefore = '', currentMatches = new Set(), currentConnections = new Map();
  const set = (node, key, value) => {
    if (node.getAttribute(key) !== value) node.setAttribute(key, value);
  };
  return ({key, path, context, shapes, boundaries, mask, matches, selected, connections}) => {
    currentMatches = matches;
    currentConnections = new Map(connections.map(connection => [connection.other, connection]));
    const geometryChanged = key !== geometryKey;
    if (!towns.size) {
      for (const feature of contextFeatures) {
        const node = svgEl('path', {class: 'map-context'});
        contexts.push({feature, node}); context.append(node);
      }
      for (const feature of countyFeatures) {
        const node = svgEl('path', {class: 'county-boundary'});
        counties.push({feature, node}); boundaries.append(node);
      }
      for (const feature of features) {
        const code = feature.properties.code, profile = profiles[code];
        // One call retains the original guard while avoiding two canonical
        // serializations per town on every pan, zoom and filter operation.
        const hook = storyHookFor(code);
        const baseTitle = profile.name + ' · ' + profile.county + ' County · ' +
          byTheme[profile.current_origin].label + (hook ? ' · ' + hook : '');
        const node = svgEl('path', {'data-code': code, 'data-origin': profile.current_origin});
        const title = svgEl('title', {}, baseTitle);
        node.style.setProperty('--origin-color', colorFor(code)); node.append(title);
        node.addEventListener('click', () => {
          if (currentMatches.has(code) || currentConnections.has(code)) activate(code);
        });
        node.addEventListener('pointerenter', () => preview(code, currentMatches.has(code)));
        node.addEventListener('pointerleave', hidePreview);
        towns.set(code, {feature, node, title, baseTitle}); shapes.append(node);
      }
    }
    if (geometryChanged) {
      set(mask, 'd', path(land));
      for (const {feature, node} of [...contexts, ...counties, ...towns.values()]) set(node, 'd', path(feature));
      geometryKey = key;
    }
    for (const [code, {node, title, baseTitle}] of towns) {
      const active = matches.has(code), connection = currentConnections.get(code);
      set(node, 'class', 'municipality' + (active ? '' : ' is-dimmed') +
        (code === selected ? ' is-selected' : active && selected ? ' is-muted' : '') +
        (connection ? ' is-connected' : ''));
      const text = baseTitle + (connection ? ' · Connected name history: ' + connection.label : '');
      if (title.textContent !== text) title.textContent = text;
    }
    // Restore the former selection's original position, then raise the new one.
    // This preserves the original stable feature order with at most two moves.
    if (selected !== selectedBefore) {
      if (towns.has(selectedBefore)) {
        const next = features.slice(featureIndex.get(selectedBefore) + 1)
          .find(feature => feature.properties.code !== selected);
        shapes.insertBefore(towns.get(selectedBefore).node,
          next ? towns.get(next.properties.code).node : null);
      }
      if (towns.has(selected)) shapes.append(towns.get(selected).node);
      selectedBefore = selected;
    }
  };
}
