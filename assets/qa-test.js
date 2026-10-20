(function () {
  'use strict';

  var FLAG_KEY = 'tidyweb-bhl-qa-test';
  var STATE_KEY = 'tidyweb-bhl-qa-test-state';
  var EMAIL = 'philipmccool@gmail.com';
  var SUBJECT = 'QA test report: The Ethics of a Birmingham Healthy Life';
  var TASKS = [
    {
      do: '**At the top right, click Detailed view.**\nFind the Active measure box in the top left corner.\n**Select HLE average.**\nYou can zoom and drag the map until you see an area you know.',
      ask: 'Find an area you know on the map and click it. Is it clear how many years of good health people there can expect?'
    },
    {
      do: 'Stay on that area’s card on the right. Under the years figure, find the green line that starts “Average HLE: Rank”.',
      ask: 'Is it clear that the rank isn’t exact, and what range of places it could fall in?'
    },
    {
      do: 'Zoom out a little.\nOn the left, click the arrow on the Active measure list.\n**Choose “Chance of being in the lowest tenth (HLE)”.**\nIf you look to the left, you’ll see the map key.',
      ask: 'Is it clear what the map colours now show?'
    },
    {
      do: 'Open the Active measure list. The ethnicity measures are six broad groups, such as Asian or Black. Choose any one.\nIn the map key at the bottom left, find the blue note that starts “Ethnicity is shown as six broad groups”.',
      ask: 'Is it clear why the site uses six broad ethnicity groups instead of more detailed ones?'
    },
    {
      do: 'Find the “Question this work” button and click it. (It opens GitHub; you don’t need to sign in or send anything.)',
      ask: 'Is it clear how you could challenge or correct something you think is wrong?'
    },
    {
      do: 'Find the Back button and use it to return to the home page.\n**Click \u2018The story\u2019.**\nIn the list of chapters on the left, find “How certain are the rankings?” (S11) and click it.\nRead only the “In short” box at the top. You don’t need to read the rest.',
      ask: 'From that summary, is it clear that some areas are definitely among the lowest, while others can’t be placed for certain?'
    }
  ];
  var TASK_COUNT = TASKS.length;
  var LIGHTS = [
    ['Green', 'Easy', '#3b7a2a'],
    ['Amber', 'Some trouble', '#c27c0e'],
    ['Red', 'Hard', '#b3261e']
  ];

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (error) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (error) {}
  }
  function safeRemove(key) {
    try { localStorage.removeItem(key); } catch (error) {}
  }

  var queryEnabled = false;
  try { queryEnabled = new URLSearchParams(window.location.search).has('qa-test'); } catch (error) {}
  if (queryEnabled) safeSet(FLAG_KEY, '1');
  if (!queryEnabled && safeGet(FLAG_KEY) !== '1') return;

  var script = document.currentScript;
  var scriptUrl = script && script.src ? script.src : window.location.href;
  var siteRoot = new URL('../', scriptUrl);
  var css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = new URL('qa-test.css', scriptUrl).href;
  css.setAttribute('data-qa-test-style', '');
  document.head.appendChild(css);

  function freshState() {
    return {
      step: 0,
      collapsed: false,
      pos: null,
      tester: '',
      tasks: TASKS.map(function () { return { light: '', why: '' }; }),
      extra: ''
    };
  }

  function loadState() {
    var value;
    try { value = JSON.parse(safeGet(STATE_KEY) || 'null'); } catch (error) { value = null; }
    if (!value || !Array.isArray(value.tasks) || value.tasks.length !== TASK_COUNT) return freshState();
    var state = freshState();
    state.step = Math.max(0, Math.min(TASK_COUNT + 1, Number(value.step) || 0));
    state.collapsed = value.collapsed === true;
    state.tester = value.tester === 'Technical' || value.tester === 'Non-technical' ? value.tester : '';
    state.extra = typeof value.extra === 'string' ? value.extra : '';
    if (Array.isArray(value.pos) && value.pos.length === 2 &&
        Number.isFinite(Number(value.pos[0])) && Number.isFinite(Number(value.pos[1]))) {
      state.pos = [Number(value.pos[0]), Number(value.pos[1])];
    }
    state.tasks = TASKS.map(function (task, index) {
      var item = value.tasks[index] || {};
      return {
        light: ['Green', 'Amber', 'Red'].indexOf(item.light) >= 0 ? item.light : '',
        why: typeof item.why === 'string' ? item.why : ''
      };
    });
    return state;
  }

  var state = loadState();
  var confirmEnd = false;
  var path = window.location.pathname;
  var isDashboard = path.endsWith('/dashboard/') || path.endsWith('/dashboard/index.html');
  var isHome = path === siteRoot.pathname || path === siteRoot.pathname + 'index.html';
  if (isDashboard && state.step === 0) {
    state.step = 1;
    state.collapsed = false;
    save();
  }

  var root = document.createElement('div');
  root.className = 'qa-root';
  root.id = 'qa-test-root';
  document.body.appendChild(root);

  function save() {
    safeSet(FLAG_KEY, '1');
    safeSet(STATE_KEY, JSON.stringify(state));
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>\"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[character];
    });
  }

  function report() {
    var output = ['Tester: ' + (state.tester || '-'), ''];
    state.tasks.forEach(function (item, index) {
      output.push('Task ' + (index + 1) + ': ' + TASKS[index].ask);
      output.push('Light: ' + (item.light || '-'));
      if (item.light === 'Amber' || item.light === 'Red') {
        output.push('What got in the way: ' + (item.why || '-'));
      }
      output.push('');
    });
    output.push('Additional comments: ' + (state.extra || '-'));
    return output.join('\n');
  }

  function reportLinks(body) {
    return [
      'https://mail.google.com/mail/?view=cm&fs=1&to=' + EMAIL +
        '&su=' + encodeURIComponent(SUBJECT) + '&body=' + encodeURIComponent(body),
      'mailto:' + EMAIL + '?subject=' + encodeURIComponent(SUBJECT) +
        '&body=' + encodeURIComponent(body)
    ];
  }

  function head() {
    if (confirmEnd) {
      return '<div class="qa-head" id="qa-drag"><span><strong>Clear all answers?</strong>  ' +
        '<button class="qa-link" data-act="confirm-end">Yes, end test</button> · ' +
        '<button class="qa-link" data-act="cancel-end">Cancel</button></span>' +
        '<span><button class="qa-link" data-act="collapse">Hide</button></span></div>';
    }
    return '<div class="qa-head" id="qa-drag"><span><strong>QA test' +
      (state.step >= 1 && state.step <= TASK_COUNT ? ' · Task ' + state.step + ' of ' + TASK_COUNT : '') +
      '</strong><span class="qa-grip">drag to move</span></span><span>' +
      '<button class="qa-link" data-act="end">End test</button> ' +
      '<button class="qa-link" data-act="collapse">Hide</button></span></div>';
  }

  function lightButtons(name, choices, selected) {
    return '<div class="qa-lights" role="radiogroup">' + choices.map(function (choice) {
      return '<label class="qa-light"><input type="radio" name="' + name + '" value="' + choice[0] + '"' +
        (selected === choice[0] ? ' checked' : '') + '><span>' +
        (choice[2] ? '<i class="qa-dot" style="background:' + choice[2] + '"></i>' +
          choice[0] + ': ' + choice[1] : choice[0]) + '</span></label>';
    }).join('') + '</div>';
  }

  function introScreen() {
    return '<h2>Welcome to the QA test</h2>' +
      '<p>I’m testing the site, not you. It takes about 10 minutes. Don’t include your address or any health details.</p>' +
      '<p class="qa-ask">Are you technical or non-technical?</p>' +
      lightButtons('tester', [['Technical'], ['Non-technical']], state.tester) +
      '<div class="qa-do" style="margin-top:18px"><b>Do this</b>On the left is the project’s home card.\nClick Open the dashboard.</div>' +
      '<p class="qa-waiting">Task 1 will appear as soon as the dashboard opens.</p>';
  }

  function taskScreen(index) {
    var item = state.tasks[index];
    var task = TASKS[index];
    var showWhy = item.light === 'Amber' || item.light === 'Red';
    var instruction = escapeHtml(task.do).replace(/\*\*(.+?)\*\*/g, '<strong class="qa-highlight">$1</strong>');
    return '<div class="qa-do"><b>Do this</b>' + instruction + '</div>' +
      '<p class="qa-ask">' + escapeHtml(task.ask) + '</p>' +
      '<label class="qa-field">How easy was it?</label>' + lightButtons('light', LIGHTS, item.light) +
      '<p class="qa-error" id="err-light" hidden>Pick a light first</p>' +
      '<div id="why-box"' + (showWhy ? '' : ' hidden') + '>' +
      '<label class="qa-field" for="why">What got in the way?</label>' +
      '<textarea id="why">' + escapeHtml(item.why) + '</textarea>' +
      '<p class="qa-error" id="err-why" hidden>Tell me what got in the way</p></div>' +
      '<div class="qa-nav"><button data-act="back">Back</button>' +
      '<button class="qa-primary" data-act="next">' +
      (index === TASK_COUNT - 1 ? 'Finish' : 'Next') + '</button></div>';
  }

  function finalScreen() {
    var body = report();
    var links = reportLinks(body);
    return '<p class="qa-ask">Send your report</p>' +
      (state.tester ? '' : '<p class="qa-ask" style="font-size:15px">Are you technical or non-technical?</p>' +
        lightButtons('tester', [['Technical'], ['Non-technical']], state.tester)) +
      '<label class="qa-field" for="extra">Do you have any additional comments? (optional)</label>' +
      '<textarea id="extra">' + escapeHtml(state.extra) + '</textarea>' +
      '<label class="qa-field">Your report</label><div class="qa-summary" id="summary">' +
      escapeHtml(body) + '</div><div class="qa-send">' +
      '<a class="qa-button qa-primary" href="' + links[0] + '" target="_blank" rel="noopener">Send with Gmail</a>' +
      '<a class="qa-button" href="' + links[1] + '">Send with Outlook or Apple Mail</a>' +
      '<button data-act="copy">Copy report</button>' +
      '<p>After copying, paste it into an email to ' + EMAIL + ', or paste it into WhatsApp and send it to Phil.</p>' +
      '</div><div class="qa-nav"><button data-act="back">Back</button><span></span></div>';
  }

  function placeAt(left, top) {
    var panel = root.querySelector('.qa-panel');
    if (!panel) return;
    panel.style.transform = 'none';
    panel.style.right = 'auto';
    panel.style.bottom = 'auto';
    panel.style.left = Math.round(left) + 'px';
    panel.style.top = Math.round(top) + 'px';
  }

  function alignHome(panel, intro) {
    var card = document.querySelector('.hero-card');
    if (!card) return;
    var rectangle = card.getBoundingClientRect();
    panel.style.transform = 'none';
    panel.style.right = 'auto';
    panel.style.bottom = 'auto';
    panel.style.left = Math.round(rectangle.right + 28) + 'px';
    panel.style.top = Math.round(rectangle.top) + 'px';
    panel.style.width = Math.round(rectangle.width) + 'px';
    panel.style.minHeight = intro ? Math.round(rectangle.height) + 'px' : '';
    panel.style.boxSizing = 'border-box';
  }

  function alignDashboard(panel) {
    var legend = document.querySelector('section.legend');
    // In the Plain view the Detailed legend is hidden and measures as zero, so dock below the view buttons instead.
    if (!legend || !legend.getClientRects().length) {
      panel.style.transform = 'none';
      panel.style.left = 'auto';
      panel.style.right = '44px';
      panel.style.top = '84px';
      panel.style.bottom = 'auto';
      return;
    }
    var rectangle = legend.getBoundingClientRect();
    panel.style.transform = 'none';
    panel.style.right = 'auto';
    panel.style.left = Math.round(rectangle.right + 18) + 'px';
    panel.style.top = 'auto';
    panel.style.bottom = Math.round(window.innerHeight - rectangle.bottom) + 'px';
  }

  function alignDefault() {
    if (state.collapsed || state.pos) return;
    var panel = root.querySelector('.qa-panel');
    if (!panel) return;
    if (isHome) {
      alignHome(panel, state.step === 0);
    } else if (isDashboard && state.step > 0) {
      alignDashboard(panel);
    } else {
      panel.style.left = 'auto';
      panel.style.right = '44px';
      panel.style.top = isDashboard ? '84px' : '20px';
      panel.style.bottom = 'auto';
    }
  }

  function scheduleAlignment() {
    window.requestAnimationFrame(alignDefault);
    window.setTimeout(alignDefault, 500);
    window.setTimeout(alignDefault, 1200);
  }

  function drag(panel) {
    var header = document.getElementById('qa-drag');
    var dragging = false;
    var offsetX = 0;
    var offsetY = 0;
    header.addEventListener('pointerdown', function (event) {
      if (event.button !== 0 || event.target.closest('button')) return;
      var rectangle = panel.getBoundingClientRect();
      offsetX = event.clientX - rectangle.left;
      offsetY = event.clientY - rectangle.top;
      dragging = true;
      panel.classList.add('qa-moved');
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
      panel.style.left = rectangle.left + 'px';
      panel.style.top = rectangle.top + 'px';
      header.setPointerCapture(event.pointerId);
      event.preventDefault();
    });
    header.addEventListener('pointermove', function (event) {
      if (!dragging) return;
      var maxLeft = Math.max(0, window.innerWidth - panel.offsetWidth);
      var x = Math.max(0, Math.min(maxLeft, event.clientX - offsetX));
      var y = Math.max(0, Math.min(window.innerHeight - 40, event.clientY - offsetY));
      panel.style.left = x + 'px';
      panel.style.top = y + 'px';
      state.pos = [x, y];
      save();
    });
    function stopDragging() {
      if (!dragging) return;
      dragging = false;
      save();
    }
    header.addEventListener('pointerup', stopDragging);
    header.addEventListener('pointercancel', stopDragging);
  }

  function show(id, visible) {
    var element = document.getElementById(id);
    if (element) element.hidden = !visible;
  }

  function wire() {
    root.querySelectorAll('[data-act]').forEach(function (button) {
      button.addEventListener('click', act);
    });
    root.querySelectorAll('input[name="tester"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        state.tester = radio.value;
        save();
        if (state.step > TASK_COUNT) render();
      });
    });
    var taskIndex = state.step - 1;
    root.querySelectorAll('input[name="light"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        var item = state.tasks[taskIndex];
        item.light = radio.value;
        show('err-light', false);
        var needsWhy = radio.value !== 'Green';
        show('why-box', needsWhy);
        if (!needsWhy) {
          item.why = '';
          var whyField = document.getElementById('why');
          if (whyField) whyField.value = '';
          show('err-why', false);
        }
        save();
      });
    });
    var why = document.getElementById('why');
    if (why) why.addEventListener('input', function () {
      state.tasks[taskIndex].why = why.value;
      save();
      show('err-why', false);
    });
    var extra = document.getElementById('extra');
    if (extra) extra.addEventListener('input', function () {
      state.extra = extra.value;
      save();
      updateReport();
    });
  }

  function updateReport() {
    var summary = document.getElementById('summary');
    if (!summary) return;
    var body = report();
    var links = reportLinks(body);
    summary.textContent = body;
    var anchors = root.querySelectorAll('.qa-send a');
    if (anchors[0]) anchors[0].href = links[0];
    if (anchors[1]) anchors[1].href = links[1];
  }

  function valid() {
    var item = state.tasks[state.step - 1];
    var okay = true;
    if (!item.light) {
      show('err-light', true);
      okay = false;
    }
    if ((item.light === 'Amber' || item.light === 'Red') && !item.why.trim()) {
      show('err-why', true);
      okay = false;
    }
    return okay;
  }

  function act(event) {
    var action = event.currentTarget.getAttribute('data-act');
    if (action === 'next') {
      if (!valid()) return;
      state.step += 1;
    } else if (action === 'back') {
      state.step = Math.max(1, state.step - 1);
    } else if (action === 'collapse') {
      state.collapsed = true;
    } else if (action === 'expand') {
      state.collapsed = false;
    } else if (action === 'end') {
      confirmEnd = true;
    } else if (action === 'cancel-end') {
      confirmEnd = false;
    } else if (action === 'confirm-end') {
      safeRemove(STATE_KEY);
      safeRemove(FLAG_KEY);
      root.remove();
      css.remove();
      window.location.assign(siteRoot.href);
      return;
    } else if (action === 'copy') {
      var button = event.currentTarget;
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        button.textContent = 'Copy failed: select the report text instead';
        return;
      }
      navigator.clipboard.writeText(report()).then(function () {
        button.textContent = 'Copied';
      }, function () {
        button.textContent = 'Copy failed: select the report text instead';
      });
      return;
    }
    save();
    render();
  }

  function render() {
    if (state.collapsed) {
      root.innerHTML = '<button class="qa-tab" data-act="expand">QA test</button>';
      wire();
      return;
    }
    var intro = state.step === 0;
    var content = intro ? introScreen() :
      state.step <= TASK_COUNT ? taskScreen(state.step - 1) : finalScreen();
    root.innerHTML = '<section class="qa-panel' + (intro ? ' qa-intro' : ' qa-dock') +
      '" role="region" aria-label="QA test">' + head() +
      '<div class="qa-body">' + content + '</div></section>';
    var panel = root.querySelector('.qa-panel');
    if (state.pos) {
      panel.classList.add('qa-moved');
      panel.style.left = state.pos[0] + 'px';
      panel.style.top = state.pos[1] + 'px';
      panel.style.right = 'auto';
      panel.style.bottom = 'auto';
    } else {
      alignDefault();
      scheduleAlignment();
    }
    drag(panel);
    wire();
  }

  window.addEventListener('load', scheduleAlignment);
  window.addEventListener('resize', scheduleAlignment);
  window.addEventListener('scroll', function () {
    if (isHome && !state.pos) scheduleAlignment();
  }, { passive: true });
  render();
})();
