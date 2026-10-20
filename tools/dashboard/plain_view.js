// Preview-only Plain view. This code is injected into the dashboard's existing
// IIFE, so the map and Detailed view remain the dashboard's own implementation.
(function () {
  if (!D.plain || !Array.isArray(D.plain.questions) || !map) return;

  var plain = D.plain;
  var active = false;
  var currentQuestion = -1;
  var currentHotspot = 0;
  var plainSelectedCode = null;
  var answerBeforeMenu = false;
  var detailedSnapshot = null;
  var actionLayer = null;
  var actionPane = null;
  var councilLabelPane = null;
  var plainHighlightCodes = new Set();
  var originalUpdate = update;
  var originalDetail = detail;
  var originalSelect = select;
  var originalStyle = selectedStyle;
  var originalTooltip = showAreaTooltip;
  var originalLegendDetailsHidden = $('legend-details').hidden;
  var originalPatternKeyHidden = document.querySelector('.pattern-key').hidden;
  var mixedLine = plain.mixed_area_line || 'Living conditions vary a lot between the neighbourhoods inside this area, so its average may hide big differences.';
  var measureKeys = [
    'annual_equivalised_income_after_housing_costs_gbp',
    'households_deprived_2plus_pct',
    'overcrowded_households_pct',
    'unemployment_rate_active_pct',
    'no_qualifications_pct',
    'pm25_area_mean_ug_m3',
    'fuel_poor_households_pct'
  ];
  var measureRows = plain.metrics.filter(function (metric) { return measureKeys.indexOf(metric.key) >= 0; });
  var backLinkHome = null;

  metrics.adult_smoking_pct = {
    label: 'Smoking', short_label: 'Smoking', family: 'context', format: 'percentage',
    display_decimals: 1, unit: '%', period: '2022–24',
    definition: 'Adult smoking estimate reported for a council, not an individual neighbourhood.',
    poor_end: 'high', band_colors: seq,
    note: 'Smoking figures describe councils, not individual neighbourhoods; some councils have no figure.'
  };

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      var value = attrs[key];
      if (key === 'className') node.className = value;
      else if (key === 'hidden') node.hidden = !!value;
      else if (key === 'disabled') node.disabled = !!value;
      else if (value !== null && value !== undefined) node.setAttribute(key, String(value));
    });
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function makeInterface() {
    var mount = $('plain-view-mount');
    var box = el('section', {id: 'plain-question-box', 'aria-label': 'Ask a question'});
    var top = el('div', {className: 'plain-box-top'});
    top.append(el('p', {className: 'plain-kicker'}, 'Healthy Life Expectancy Explorer'));
    var title = el('h1');
    title.append(
      el('span', {}, 'Birmingham and its surrounding areas'),
      el('span', {}, 'Years in good health')
    );
    top.append(title);
    var ask = el('button', {id: 'plain-ask-button', type: 'button', 'aria-expanded': 'false', 'aria-controls': 'plain-question-list'});
    ask.append(el('span', {}, 'What would you like to know?'), el('span', {className: 'plain-chevron', 'aria-hidden': 'true'}, '▾'));
    ask.onclick = function () { setQuestionMenu($('plain-question-list').hidden); };
    top.append(ask);

    var list = el('ol', {id: 'plain-question-list', 'aria-label': 'Plain view questions'});
    list.hidden = true;
    plain.questions.forEach(function (entry, index) {
      var item = el('li');
      var button = el('button', {type: 'button', className: 'plain-question-pill', 'aria-current': 'false'});
      button.append(el('span', {className: 'plain-question-number', 'aria-hidden': 'true'}, String(index + 1)));
      button.append(el('span', {}, entry.question));
      button.onclick = function () { showQuestion(index); };
      item.append(button);
      list.append(item);
    });

    var answer = el('section', {id: 'plain-answer', 'aria-live': 'polite', 'aria-label': 'Answer'});
    answer.hidden = true;
    var answerHead = el('div', {className: 'plain-answer-head'});
    answerHead.append(el('h2', {id: 'plain-answer-title'}));
    var answerClose = el('button', {type: 'button', id: 'plain-answer-close', className: 'plain-close', 'aria-label': 'Close answer'}, '×');
    answerClose.onclick = closeAnswer;
    answerHead.append(answerClose);
    answer.append(answerHead, el('div', {id: 'plain-answer-body', className: 'plain-answer-body'}));

    var foot = el('div', {className: 'plain-box-foot'});
    var originalQuestionLink = document.querySelector('.bottom-actions .question-btn');
    var questionUrl = originalQuestionLink ? originalQuestionLink.href : 'https://github.com/TidyWeb/Birmingham-Healthy-Life-Second-Look/issues/new?template=question-this-work.yml';
    foot.append(document.createTextNode('Think something here is wrong? '));
    foot.append(el('a', {href: questionUrl, target: '_blank', rel: 'noopener noreferrer'}, 'Tell me.'));
    foot.append(document.createTextNode(' The form needs a free GitHub account.'));
    box.append(top, list, answer, foot);

    var topbar = el('nav', {id: 'plain-view-topbar', role: 'group', 'aria-label': 'Choose a view'});
    var plainButton = el('button', {type: 'button', id: 'plain-view-button', 'aria-pressed': 'true'}, 'Plain view');
    var detailButton = el('button', {type: 'button', id: 'detailed-view-button', 'aria-pressed': 'false'}, 'Detailed view');
    plainButton.onclick = function () { setView(true); };
    detailButton.onclick = function () { setView(false); };
    topbar.append(plainButton, detailButton);

    var tools = el('div', {id: 'plain-map-tools', 'aria-label': 'Map controls'});
    var zoom = el('div', {className: 'plain-zoom-controls', role: 'group', 'aria-label': 'Map zoom'});
    var zoomIn = el('button', {type: 'button', 'aria-label': 'Zoom in'}, '+');
    var zoomOut = el('button', {type: 'button', 'aria-label': 'Zoom out'}, '−');
    zoomIn.onclick = function () { map.zoomIn(); };
    zoomOut.onclick = function () { map.zoomOut(); };
    zoom.append(zoomIn, zoomOut);
    var legend = el('section', {id: 'plain-legend', 'aria-label': 'Map legend'});
    legend.append(el('p', {id: 'plain-legend-title'}), el('p', {id: 'plain-legend-note'}), el('div', {id: 'plain-bands', className: 'plain-bands'}));
    tools.append(zoom, legend);

    var popup = el('section', {id: 'plain-area-popup', role: 'dialog', 'aria-labelledby': 'plain-area-title'});
    popup.hidden = true;
    var popupHead = el('div', {id: 'plain-area-head', className: 'plain-area-head'});
    var areaTitle = el('h2', {id: 'plain-area-title'});
    areaTitle.append(el('span', {className: 'plain-drag-hint'}, 'Drag to move'), el('span', {id: 'plain-area-name'}));
    var areaClose = el('button', {type: 'button', className: 'plain-close', 'aria-label': 'Close area'}, '×');
    areaClose.onclick = closeArea;
    popupHead.append(areaTitle, areaClose);
    popup.append(popupHead, el('div', {id: 'plain-area-body'}));

    mount.replaceChildren(box, topbar, tools, popup);
    wireAreaDragging(popup, popupHead);
    document.addEventListener('DOMContentLoaded', moveBackLink, {once: true});
    if (document.readyState !== 'loading') moveBackLink();
  }

  function moveBackLink() {
    var link = $('back-to-story');
    var topbar = $('plain-view-topbar');
    if (!active || !link || !topbar || topbar.contains(link)) return;
    if (!backLinkHome) backLinkHome = {parent: link.parentNode, next: link.nextSibling, style: link.getAttribute('style')};
    topbar.insertBefore(link, topbar.firstChild);
  }

  function restoreBackLink() {
    var link = $('back-to-story');
    if (!link || !backLinkHome) return;
    var home = backLinkHome;
    if (home.next && home.next.parentNode === home.parent) home.parent.insertBefore(link, home.next);
    else home.parent.appendChild(link);
    if (home.style === null) link.removeAttribute('style');
    else link.setAttribute('style', home.style);
  }

  function captureDetailedState() {
    var stateKeys = ['metric', 'sex', 'coverage', 'pinned', 'detailOpen', 'pair', 'pairReturn', 'sort', 'direction', 'drawer', 'fill'];
    var savedState = {};
    stateKeys.forEach(function (key) { savedState[key] = state[key]; });
    savedState.authorities = Array.from(state.authorities || []);
    savedState.histogramBins = Array.from(state.histogramBins || []);
    savedState.legendBands = Array.from(state.legendBands || []);
    var checks = {};
    ['student-layer', 'visitor-layer', 'imputed-layer', 'gaps-layer', 'boundaries', 'map-labels'].forEach(function (id) {
      checks[id] = $(id).checked;
    });
    var centre = map.getCenter();
    return {
      state: savedState,
      checks: checks,
      controlsOpen: !$('controls').classList.contains('collapsed'),
      detailOpenClass: !$('detail').classList.contains('collapsed'),
      drawerOpenClass: !$('drawer').classList.contains('collapsed'),
      detailScrollTop: $('detail').scrollTop,
      drawerScrollTop: $('drawer').scrollTop,
      areaPicker: $('area-picker').value,
      legendExpanded: legendExpanded,
      mapCenter: [centre.lat, centre.lng],
      mapZoom: map.getZoom(),
      mapClean: document.body.classList.contains('map-clean')
    };
  }

  function restoreDetailedState(snapshot) {
    if (!snapshot) return;
    var saved = snapshot.state;
    Object.keys(saved).forEach(function (key) {
      if (key === 'authorities') state.authorities = new Set(saved[key]);
      else if (key === 'histogramBins') state.histogramBins = new Set(saved[key]);
      else if (key === 'legendBands') state.legendBands = new Set(saved[key]);
      else state[key] = saved[key];
    });
    Object.keys(snapshot.checks).forEach(function (id) { $(id).checked = snapshot.checks[id]; });
    $('metric-select').value = state.metric;
    $('coverage').value = state.coverage;
    $('area-picker').value = snapshot.areaPicker;
    $('opacity').value = String(Math.round(state.fill * 100));
    $('opacity-label').textContent = Math.round(state.fill * 100) + '%';
    ['average', 'male', 'female'].forEach(function (name) {
      $('sex-' + name).setAttribute('aria-pressed', String((name === 'average' && state.sex === 'avg') || name === state.sex));
    });
    document.querySelectorAll('#authorities input').forEach(function (input) {
      input.checked = state.authorities.has(input.value);
    });
    $('controls').classList.toggle('collapsed', !snapshot.controlsOpen);
    $('controls-toggle').setAttribute('aria-expanded', String(snapshot.controlsOpen));
    $('detail').classList.toggle('collapsed', !snapshot.detailOpenClass);
    $('drawer').classList.toggle('collapsed', !snapshot.drawerOpenClass);
    $('charts-open').setAttribute('aria-expanded', String(!!state.drawer));
    $('detail').scrollTop = snapshot.detailScrollTop;
    $('drawer').scrollTop = snapshot.drawerScrollTop;
    legendExpanded = snapshot.legendExpanded;
    $('legend-details').open = legendExpanded;
    document.body.classList.toggle('map-clean', snapshot.mapClean);
    authorityCount();
  }

  function setView(plainMode) {
    if (plainMode === active) return;
    if (plainMode) {
      detailedSnapshot = captureDetailedState();
      active = true;
      document.body.classList.add('plain-view-active');
      $('plain-view-button').setAttribute('aria-pressed', 'true');
      $('detailed-view-button').setAttribute('aria-pressed', 'false');
      $('map').setAttribute('aria-label', 'Map of years in good health and living conditions across the areas covered');
      closeAreaTooltip();
      clearActionLayer();
      plainSelectedCode = null;
      currentQuestion = -1;
      answerBeforeMenu = false;
      $('plain-question-list').hidden = true;
      $('plain-ask-button').setAttribute('aria-expanded', 'false');
      $('plain-answer').hidden = true;
      $('plain-question-list').querySelectorAll('.plain-question-pill').forEach(function (button) {
        button.setAttribute('aria-current', 'false');
      });
      $('plain-area-popup').hidden = true;
      state.metric = 'hle_average';
      state.sex = 'avg';
      state.coverage = 'all';
      state.authorities = new Set(areas.map(auth));
      state.pinned = null;
      state.pair = null;
      state.pairReturn = null;
      state.detailOpen = false;
      state.drawer = '';
      state.fill = .72;
      state.histogramBins = new Set();
      state.legendBands = new Set();
      $('metric-select').value = 'hle_average';
      $('coverage').value = 'all';
      $('opacity').value = '72';
      $('opacity-label').textContent = '72%';
      ['average', 'male', 'female'].forEach(function (name) {
        $('sex-' + name).setAttribute('aria-pressed', String(name === 'average'));
      });
      document.querySelectorAll('#authorities input').forEach(function (input) { input.checked = true; });
      ['student-layer', 'visitor-layer', 'imputed-layer', 'gaps-layer', 'map-labels'].forEach(function (id) { $(id).checked = false; });
      $('controls').classList.add('collapsed');
      $('controls-toggle').setAttribute('aria-expanded', 'false');
      $('detail').classList.add('collapsed');
      $('drawer').classList.add('collapsed');
      $('charts-open').setAttribute('aria-expanded', 'false');
      $('legend-details').hidden = true;
      document.querySelector('.pattern-key').hidden = true;
      moveBackLink();
      map.invalidateSize({pan: false});
      update();
      renderPlainLegend();
      fitHome();
    } else {
      clearActionLayer();
      plainSelectedCode = null;
      $('plain-area-popup').hidden = true;
      active = false;
      document.body.classList.remove('plain-view-active');
      $('plain-view-button').setAttribute('aria-pressed', 'false');
      $('detailed-view-button').setAttribute('aria-pressed', 'true');
      $('map').setAttribute('aria-label', 'Map of healthy life expectancy and area measures');
      $('legend-details').hidden = originalLegendDetailsHidden;
      document.querySelector('.pattern-key').hidden = originalPatternKeyHidden;
      restoreDetailedState(detailedSnapshot);
      restoreBackLink();
      map.invalidateSize({pan: false});
      update();
      if (detailedSnapshot) map.setView(detailedSnapshot.mapCenter, detailedSnapshot.mapZoom, {animate: false});
      detailedSnapshot = null;
    }
  }

  function fitPadding() {
    var box = $('plain-question-box').getBoundingClientRect();
    return {paddingTopLeft: [Math.ceil(box.right + 26), 64], paddingBottomRight: [28, 28], animate: false};
  }

  function fitHome() {
    if (!map || !baseBounds) return;
    map.fitBounds(baseBounds.pad(BOUNDS_PADDING), fitPadding());
  }

  function setQuestionMenu(open, restoreAnswer) {
    var list = $('plain-question-list');
    var answer = $('plain-answer');
    if (open) {
      answerBeforeMenu = !answer.hidden;
      answer.hidden = true;
    } else if (restoreAnswer !== false && answerBeforeMenu) {
      answer.hidden = false;
    }
    list.hidden = !open;
    $('plain-ask-button').setAttribute('aria-expanded', String(open));
    if (open) {
      var selected = list.querySelector('[aria-current="true"]') || list.querySelector('.plain-question-pill');
      if (selected) selected.focus();
    }
    if (!open) answerBeforeMenu = false;
  }

  function appendQuestionText(parent, question) {
    var text = question.answer || '';
    var signal = plain.fair_use_signal_box || 'Before publishing, I checked this work with Signal Box, my 27-question ethics check.';
    var at = question.question.indexOf('judge a place') >= 0 ? text.indexOf(signal) : -1;
    if (at < 0) {
      parent.append(el('p', {}, text));
      return;
    }
    var paragraph = el('p');
    paragraph.append(document.createTextNode(text.slice(0, at)));
    paragraph.append(el('a', {href: plain.signal_box_method_href, target: '_blank', rel: 'noopener noreferrer'}, signal));
    paragraph.append(document.createTextNode(text.slice(at + signal.length)));
    parent.append(paragraph);
  }

  function showQuestion(index) {
    var question = plain.questions[index];
    if (!question) return;
    var previousQuestion = currentQuestion;
    currentQuestion = index;
    if (index !== 4 || previousQuestion !== index) {
      state.metric = 'hle_average';
      $('metric-select').value = 'hle_average';
    }
    setQuestionMenu(false, false);
    $('plain-question-list').querySelectorAll('.plain-question-pill').forEach(function (button, i) {
      button.setAttribute('aria-current', String(i === index));
    });
    $('plain-answer-title').textContent = (index + 1) + '. ' + question.question;
    var body = $('plain-answer-body');
    body.replaceChildren();
    appendQuestionText(body, question);
    $('plain-answer').hidden = false;
    var action = question.action || {type: 'answer'};
    if (index === 4) appendMeasureButtons(body);
    if (action.type === 'hotspots') appendHotspotControls(body);
    clearActionLayer();
    if (action.type === 'highlight') {
      plainHighlightCodes = new Set(action.codes || []);
      areasLayer.setStyle(selectedStyle);
      fitHome();
    } else if (action.type === 'hotspots') {
      currentHotspot = Number(action.index) || 0;
      showHotspot();
    } else if (action.type === 'outline-councils') {
      showCouncils();
    }
    update();
    renderPlainLegend();
    renderPlainArea();
    body.scrollTop = 0;
  }

  function closeAnswer() {
    $('plain-answer').hidden = true;
    currentQuestion = -1;
    plainHighlightCodes = new Set();
    clearActionLayer();
    state.metric = 'hle_average';
    $('metric-select').value = 'hle_average';
    update();
    renderPlainLegend();
    renderPlainArea();
    $('plain-ask-button').focus();
  }

  function appendMeasureButtons(body) {
    body.append(el('p', {}, 'See one of these on the map:'));
    var root = el('div', {className: 'plain-action-buttons', role: 'group', 'aria-label': 'Choose a measure to show on the map'});
    var all = [{key: 'hle_average', label: 'Years in good health'}].concat(measureRows);
    all.forEach(function (metric) {
      var button = el('button', {type: 'button', className: 'plain-action-button', 'data-metric': metric.key, 'aria-pressed': String(state.metric === metric.key)}, metric.label);
      button.onclick = function () { setPlainMetric(metric.key); };
      root.append(button);
    });
    body.append(root);
  }

  function setPlainMetric(key) {
    state.metric = key;
    state.sex = 'avg';
    $('metric-select').value = key;
    ['average', 'male', 'female'].forEach(function (name) {
      $('sex-' + name).setAttribute('aria-pressed', String(name === 'average'));
    });
    $('plain-answer-body').querySelectorAll('[data-metric]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.getAttribute('data-metric') === key));
    });
    update();
    renderPlainLegend();
    renderPlainArea();
  }

  function appendHotspotControls(body) {
    var root = el('div', {id: 'plain-hotspot-controls'});
    root.append(el('div', {id: 'plain-hotspot-note', className: 'plain-hotspot-note'}));
    var controls = el('div', {className: 'plain-step-controls'});
    var previous = el('button', {type: 'button', id: 'plain-hotspot-previous', className: 'plain-action-button'}, '← Previous place');
    var next = el('button', {type: 'button', id: 'plain-hotspot-next', className: 'plain-action-button'}, 'Next place →');
    previous.onclick = function () { moveHotspot(-1); };
    next.onclick = function () { moveHotspot(1); };
    controls.append(previous, next);
    root.append(controls);
    body.append(root);
  }

  function showHotspot() {
    var hot = plain.hotspots[currentHotspot];
    if (!hot) return;
    clearActionLayer();
    plainHighlightCodes = new Set(hot.codes || []);
    areasLayer.setStyle(selectedStyle);
    actionLayer = L.layerGroup().addTo(map);
    var selectedFeatures = D.geometry.features.filter(function (feature) {
      return plainHighlightCodes.has(feature.properties.area_code);
    });
    if (selectedFeatures.length) {
      L.geoJSON({type: 'FeatureCollection', features: selectedFeatures}, {
        pane: 'plainActionPane', interactive: false,
        style: {color: '#fff', weight: 2.2, opacity: 1, fillColor: '#d7e75b', fillOpacity: .24}
      }).addTo(actionLayer);
    }
    (hot.pairs || []).forEach(function (pair) {
      var a = byCode.get(pair[0]), b = byCode.get(pair[1]);
      var first = center(a), second = center(b);
      if (first && second) L.polyline([first, second], {
        pane: 'plainActionPane', color: '#172329', weight: 3, dashArray: '6 6', opacity: .95, interactive: false
      }).addTo(actionLayer);
    });
    var note = $('plain-hotspot-note');
    note.replaceChildren(el('b', {}, (currentHotspot + 1) + ' of ' + plain.hotspots.length + ': ' + hot.name + '. '), document.createTextNode(hot.sentence));
    $('plain-hotspot-previous').disabled = currentHotspot === 0;
    $('plain-hotspot-next').disabled = currentHotspot === plain.hotspots.length - 1;
    var bounds = hot.bounds;
    map.fitBounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]], Object.assign(fitPadding(), {maxZoom: 13}));
  }

  function moveHotspot(direction) {
    currentHotspot = Math.max(0, Math.min(plain.hotspots.length - 1, currentHotspot + direction));
    showHotspot();
  }

  function showCouncils() {
    clearActionLayer();
    plainHighlightCodes = new Set();
    areasLayer.setStyle(selectedStyle);
    actionLayer = L.layerGroup().addTo(map);
    L.geoJSON(plain.council_outline_geojson, {
      pane: 'plainActionPane', interactive: false,
      style: {color: '#172329', weight: 3.2, opacity: 1, fill: false, fillOpacity: 0}
    }).addTo(actionLayer);
    (plain.council_labels || []).forEach(function (council) {
      var label = council.name + ': about ' + council.average + ' years';
      L.marker([council.lat, council.lon], {
        pane: 'plainCouncilLabelPane', interactive: false,
        icon: L.divIcon({className: 'plain-council-icon', iconSize: null, html: '<span class="plain-council-label">' + esc(label) + '</span>'})
      }).addTo(actionLayer);
    });
    var bounds = L.geoJSON(plain.council_outline_geojson);
    map.fitBounds(bounds.getBounds(), Object.assign(fitPadding(), {maxZoom: 10}));
  }

  function clearActionLayer() {
    if (actionLayer && map.hasLayer(actionLayer)) map.removeLayer(actionLayer);
    actionLayer = null;
    plainHighlightCodes = new Set();
    if (areasLayer) areasLayer.setStyle(selectedStyle);
  }

  function renderPlainLegend() {
    if (!active) return;
    var metric = plain.metrics.find(function (row) { return row.key === state.metric; }) || plain.metrics[0];
    var palette = mapPalette();
    $('plain-legend-title').textContent = metric.key === 'hle_average'
      ? metric.label + ', compared with the average across all the areas covered'
      : metric.label + ', compared across the areas covered';
    $('plain-legend-note').textContent = metric.key === 'hle_average'
      ? 'Lower values mean fewer years in good health.'
      : (metric.worse === 'lower' ? 'Lower values generally mean worse conditions.' : 'Higher values generally mean worse conditions.');
    var labels = ['Much lower', 'Lower', 'Around average', 'Higher', 'Much higher'];
    var bands = $('plain-bands');
    bands.replaceChildren();
    labels.forEach(function (label, index) {
      var item = el('div', {className: 'plain-band'});
      item.append(el('i', {style: 'background:' + palette[index]}), document.createTextNode(label));
      bands.append(item);
    });
  }

  function plainHleColour(value) {
    var v = Number(value);
    return v < 55 ? colors[0] : v < 60 ? colors[1] : v < 65 ? colors[2] : v < 70 ? colors[3] : colors[4];
  }

  function metricPosition(value) {
    if (value === null || value === undefined || !Number.isFinite(Number(value))) return 'No figure is available for this measure.';
    if (state.metric === 'hle_average') return '';
    var index = quantiles.findIndex(function (cut) { return Number(value) <= cut; });
    if (index < 0) index = 4;
    return ['among the lowest fifth of areas', 'lower than most areas', 'in the middle', 'higher than most areas', 'among the highest fifth of areas'][index] + '.';
  }

  function renderPlainArea() {
    if (!active || !plainSelectedCode) return;
    var area = byCode.get(plainSelectedCode);
    var data = plain.areas[plainSelectedCode];
    if (!area || !data) return;
    var popup = $('plain-area-popup');
    var wasHidden = popup.hidden;
    $('plain-area-name').textContent = nm(area);
    var body = $('plain-area-body');
    body.replaceChildren();
    body.append(el('p', {}, data.sentence));
    var where = el('p', {className: 'plain-where'});
    where.append(document.createTextNode('Where it sits: '), document.createTextNode(data.position + '.'));
    body.append(where);
    if (state.metric !== 'hle_average') {
      var measure = plain.metrics.find(function (row) { return row.key === state.metric; });
      var value = raw(area, state.metric);
      if (measure) body.append(el('p', {}, measure.label + ': ' + metricPosition(value)));
    }
    (data.notes || []).forEach(function (note) { body.append(el('p', {className: 'plain-note'}, note)); });
    if (data.mixed) body.append(el('p', {className: 'plain-note'}, mixedLine));
    body.append(el('p', {className: 'plain-bar-heading'}, 'Compared with the average across all the areas covered'));
    var value = Number(data.bar && data.bar.value !== undefined ? data.bar.value : data.hle);
    var average = Number(data.bar && data.bar.average !== undefined ? data.bar.average : data.average);
    appendAreaBar(body, 'This area', value, plainHleColour(value));
    appendAreaBar(body, 'Average', average, '#4a5652');
    var fullData = el('div', {className: 'plain-full-data'});
    var fullButton = el('button', {type: 'button', id: 'plain-see-full-data'}, 'See the full data');
    fullButton.onclick = function () {
      var code = plainSelectedCode;
      setView(false);
      select(code);
    };
    fullData.append(fullButton);
    body.append(fullData);
    popup.hidden = false;
    if (wasHidden && popup.dataset.moved !== '1') {
      popup.style.left = 'auto';
      popup.style.right = '1rem';
      popup.style.top = '4.65rem';
    }
  }

  function appendAreaBar(parent, label, value, colorValue) {
    var row = el('div', {className: 'plain-area-bar'});
    row.append(el('span', {}, label));
    var track = el('span', {className: 'plain-area-bar-track'});
    var fill = Math.max(4, Math.min(100, (value - 45) / 35 * 100));
    track.append(el('i', {className: 'plain-area-bar-fill', style: 'width:' + fill + '%;background:' + colorValue}));
    row.append(track, el('strong', {}, Math.round(value) + ' years'));
    parent.append(row);
  }

  function closeArea() {
    var popup = $('plain-area-popup');
    popup.hidden = true;
    popup.removeAttribute('data-moved');
    popup.style.left = 'auto';
    popup.style.right = '1rem';
    popup.style.top = '4.65rem';
    plainSelectedCode = null;
    state.pinned = null;
    state.pair = null;
    state.pairReturn = null;
    state.detailOpen = false;
    $('area-picker').value = '';
    update();
  }

  function wireAreaDragging(popup, head) {
    var pointerId = null;
    var moveHandler = null;
    var upHandler = null;
    head.addEventListener('pointerdown', function (event) {
      if (event.target.closest('.plain-close')) return;
      var rect = popup.getBoundingClientRect();
      var dx = event.clientX - rect.left;
      var dy = event.clientY - rect.top;
      pointerId = event.pointerId;
      head.setPointerCapture(pointerId);
      moveHandler = function (move) {
        if (move.pointerId !== pointerId) return;
        popup.dataset.moved = '1';
        popup.style.right = 'auto';
        popup.style.left = Math.max(-rect.width + 120, Math.min(innerWidth - 120, move.clientX - dx)) + 'px';
        popup.style.top = Math.max(0, Math.min(innerHeight - 60, move.clientY - dy)) + 'px';
      };
      upHandler = function (up) {
        if (up.pointerId !== pointerId) return;
        head.removeEventListener('pointermove', moveHandler);
        head.removeEventListener('pointerup', upHandler);
        head.removeEventListener('pointercancel', upHandler);
        pointerId = null;
      };
      head.addEventListener('pointermove', moveHandler);
      head.addEventListener('pointerup', upHandler);
      head.addEventListener('pointercancel', upHandler);
    });
  }

  function handlePlainEscape(event) {
    if (!active || event.key !== 'Escape') return;
    if (!$('plain-question-list').hidden) {
      event.preventDefault();
      event.stopImmediatePropagation();
      setQuestionMenu(false, true);
      $('plain-ask-button').focus();
    } else if (!$('plain-area-popup').hidden) {
      event.preventDefault();
      event.stopImmediatePropagation();
      closeArea();
    } else if (!$('plain-answer').hidden) {
      event.preventDefault();
      event.stopImmediatePropagation();
      closeAnswer();
    }
  }

  function handlePlainAreaClick(code) {
    plainSelectedCode = code;
    originalSelect(code);
    renderPlainArea();
  }

  selectedStyle = function (feature) {
    var style = originalStyle(feature);
    if (!active || !plainHighlightCodes.size) return style;
    var code = feature.properties.area_code;
    if (plainHighlightCodes.has(code)) {
      style.fillOpacity = .92;
      style.color = '#fff';
      style.weight = 2;
    } else {
      style.fillOpacity = .28;
      style.weight = .45;
    }
    return style;
  };
  update = function () {
    originalUpdate();
    if (active) {
      renderPlainLegend();
      renderPlainArea();
    }
  };
  detail = function () {
    originalDetail();
    if (active) renderPlainArea();
  };
  select = function (code) {
    if (active) handlePlainAreaClick(code);
    else originalSelect(code);
  };
  showAreaTooltip = function (area, latlng, persist) {
    if (!active) originalTooltip(area, latlng, persist);
  };

  makeInterface();
  actionPane = map.createPane('plainActionPane');
  actionPane.style.zIndex = '445';
  actionPane.style.pointerEvents = 'none';
  councilLabelPane = map.createPane('plainCouncilLabelPane');
  councilLabelPane.style.zIndex = '455';
  councilLabelPane.style.pointerEvents = 'none';
  $('plain-view-button').setAttribute('aria-pressed', 'false');
  $('detailed-view-button').setAttribute('aria-pressed', 'true');
  setView(true);
  document.addEventListener('keydown', handlePlainEscape, true);
})();
