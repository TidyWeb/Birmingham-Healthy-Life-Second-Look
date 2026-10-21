/* Signal Box, read-only boards for the Unit 3 site. Data: signal-box-data.js (window.SBX_DATA). */
(function(){
  // SBX_DATA: the guide's 27 questions with Phil's Unit 3 answers attached.
  var D = window.SBX_DATA, root = document.getElementById('sbx');
  if (!root) return;
  var active = D.groups[0].id, sel = null;
  var WORD = {o:'Yes: concern settled by executive decision', y:'Yes: investigated and recorded', g:'No: no concern raised'};
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function lamp(q, tag){
    var label = 'Question ' + q.n + ': ' + WORD[q.lamp];
    return tag === 'button'
      ? '<button type="button" class="sbx-lamp ' + q.lamp + (sel === q.n ? ' sel' : '') + '" data-q="' + q.n + '" data-g="' + q.g + '" aria-label="' + esc(label) + ', show what I recorded" title="Q' + q.n + ': ' + esc(q.q) + '">' + q.n + '</button>'
      : '<span class="sbx-lamp ' + q.lamp + '" aria-hidden="true">' + q.n + '</span>';
  }
  function open(g){ return g.qs.filter(function(q){ return q.lamp === 'o'; }).length; }
  function render(){
    var tot = {o:0, y:0, g:0};
    D.groups.forEach(function(g){ g.qs.forEach(function(q){ tot[q.lamp]++; }); });
    var held = tot.o;
    var html = '<p class="sbx-title">Signal Box: my answers for this project</p>' +
      '<div class="sbx-sum" role="group" aria-label="Lamp totals"><span><i class="sbx-sw o"></i>Orange, settled by executive decision <strong>' + tot.o + '</strong></span>' +
      '<span><i class="sbx-sw y"></i>Yellow, investigated and recorded <strong>' + tot.y + '</strong></span>' +
      '<span><i class="sbx-sw g"></i>Grey, no concern raised <strong>' + tot.g + '</strong></span></div>' +
      '<p class="sbx-start">Start: the published project</p><div class="sbx-track">' +
      D.groups.map(function(g){
        var h = open(g);
        return '<div class="sbx-col' + (h ? ' held' : '') + '"><div class="sbx-box" role="button" tabindex="0" data-g="' + g.id + '" aria-pressed="' + (active === g.id) + '" aria-label="Checkpoint ' + g.id + ', ' + esc(g.name) + ', show its questions">' +
          '<h4><small>Checkpoint ' + g.id + '</small>' + esc(g.name) + '</h4><div class="sbx-lamps">' + g.qs.map(function(q){ return lamp(q, 'button'); }).join('') + '</div></div>' +
          '<div class="sbx-link"></div><div class="sbx-dia"><span>Any<br>orange?</span></div><div class="sbx-out">' + (h ? 'Yes: held' : 'No: continue') + '</div>' +
          (h ? '<div class="sbx-held">Held: ' + h + ' open</div>' : '') + '</div>';
      }).join('') + '</div>' +
      '<div class="sbx-end' + (held ? ' held' : '') + '"><b>End: I decide, as the project owner: proceed, narrow, redesign or stop.</b><span>' +
      (D.decision ? '<strong>My decision: proceed.</strong> ' + held + ' lamp' + (held > 1 ? 's' : '') + ' stay orange on purpose.' : held + ' orange lamps not yet settled') + '</span></div>' +
      (D.decision ? '<div class="sbx-why"><h4>Why three lamps stay orange</h4><p>' + esc(D.decision.intro) + '</p><ul>' +
        D.decision.items.map(function(it){ return '<li><button type="button" class="sbx-lamp o" data-q="' + it.n + '" data-g="' + it.g + '" aria-label="Question ' + it.n + ', show what I recorded">' + it.n + '</button><div><b>' + esc(it.title) + '</b> ' + esc(it.text) + '</div></li>'; }).join('') +
        '</ul></div>' : '') +
      '<div class="sbx-panel"><div class="sbx-tabs" role="tablist" aria-label="Checkpoints">' +
      D.groups.map(function(g){ return '<button type="button" role="tab" id="sbx-tab-' + g.id + '" aria-controls="sbx-qs" aria-selected="' + (active === g.id) + '" tabindex="' + (active === g.id ? 0 : -1) + '" data-tab="' + g.id + '">' + g.id + ' · ' + esc(g.name) + '<i>' + (open(g) || '') + '</i></button>'; }).join('') +
      '</div><ol class="sbx-qs" id="sbx-qs" role="tabpanel" aria-labelledby="sbx-tab-' + active + '">' +
      group(active).qs.map(function(q){
        return '<li class="sbx-q" id="sbx-q' + q.n + '">' + lamp(q, 'span') + '<div><div class="sbx-qt">Q' + q.n + '. ' + esc(q.q) + (q.legal ? '<span class="sbx-legal">legal trigger</span>' : '') + '</div>' +
          '<span class="sbx-ans ' + q.lamp + '">' + WORD[q.lamp] + '</span>' +
          '<details' + (sel === q.n ? ' open' : '') + '><summary>What I recorded</summary><div class="sbx-rec">' +
          '<h5>What I found</h5>' + q.evidence.map(function(p){ return '<p>' + esc(p) + '</p>'; }).join('') +
          (q.action ? '<h5>What I did about it</h5><p>' + esc(q.action) + '</p>' : '') +
          (q.where ? '<h5>Where it is dealt with</h5><p><a href="' + esc(q.where.href) + '"' + (q.where.ext ? ' target="_blank" rel="noopener noreferrer"' : '') + '>' + esc(q.where.label) + '</a></p>' : '') +
          '</div></details></div></li>';
      }).join('') + '</ol></div>';
    root.innerHTML = html;
  }
  function group(id){ return D.groups.filter(function(g){ return g.id === id; })[0]; }
  root.addEventListener('click', function(e){
    var l = e.target.closest('[data-q]');
    if (l){ sel = +l.dataset.q; active = l.dataset.g; render();
      var row = document.getElementById('sbx-q' + sel); if (row){ row.scrollIntoView({block:'nearest', behavior:'smooth'}); row.querySelector('summary').focus({preventScroll:true}); }
      return; }
    var t = e.target.closest('[data-tab],[data-g]');
    if (t){ active = t.dataset.tab || t.dataset.g; sel = null; render();
      var f = root.querySelector(t.dataset.tab ? '#sbx-tab-' + active : '.sbx-box[data-g="' + active + '"]'); if (f) f.focus(); }
  });
  root.addEventListener('keydown', function(e){
    var t = e.target;
    if (t.classList.contains('sbx-box') && (e.key === 'Enter' || e.key === ' ')){ e.preventDefault(); t.click(); return; }
    if (t.getAttribute('role') === 'tab' && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')){
      var ids = D.groups.map(function(g){ return g.id; }), i = ids.indexOf(active);
      i = (i + (e.key === 'ArrowRight' ? 1 : ids.length - 1)) % ids.length;
      active = ids[i]; sel = null; render(); root.querySelector('#sbx-tab-' + active).focus(); e.preventDefault();
    }
  });
  render();
})();

(function () {
  "use strict";

  var D = window.SBX_DATA;
  if (!D || !Array.isArray(D.groups) || !Array.isArray(D.stages)) {
    throw new Error("Compact Signal Box data is missing or incomplete.");
  }

  var QS = [];
  D.groups.forEach(function (group) {
    group.qs.forEach(function (question) { QS.push(question); });
  });

  var WORD = { o: "concern", y: "investigated and recorded", g: "no concern raised" };
  var AFTER = { o: "concern settled by executive decision", y: "investigated and recorded", g: "no concern raised" };

  function esc(value) {
    return String(value).replace(/[&<>"']/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
    });
  }

  function lamp(state, number, legal) {
    return '<span class="sbx-lamp ' + state + '" aria-hidden="true">' + number + "</span>" +
      (legal ? '<span class="sbm-legal" aria-hidden="true">⚖</span>' : "");
  }

  function methodLink() {
    return '<p class="sbm-more"><a href="' + esc(D.methodHref) + '">See every answer in Signal Box on The method</a></p>';
  }

  function board(state) {
    var after = state === "after";
    return '<div class="sbm-board" role="group" aria-label="' + (after ? "After the Unit 3 re-test" : "Unit 2 screen") + '">' +
      D.groups.map(function (group) {
        return '<div class="sbm-cp"><h5><small>Checkpoint ' + esc(group.id) + '</small>' + esc(group.name) + '</h5><div class="sbm-lamps">' +
          group.qs.map(function (question) {
            return '<span class="sbm-l">' + lamp(after ? question.lamp : question.before, question.n, question.legal) + '</span>';
          }).join("") +
          '</div></div>';
      }).join("") +
      '</div><p class="sbm-sr">' + D.groups.map(function (group) {
        return "Checkpoint " + group.id + ", " + group.name + ": " + group.qs.map(function (question) {
          var status = after ? AFTER[question.lamp] : WORD[question.before];
          return "Q" + question.n + " " + status + (question.legal ? ", legal trigger" : "");
        }).join("; ") + ".";
      }).join(" ") + "</p>";
  }

  function key(kind) {
    var items = [];
    if (kind === "pair" || kind === "both") {
      items.push("<span>Left: the Unit 2 screen. Right: after the Unit 3 re-test.</span>");
      items.push('<span><i class="sbx-sw o"></i>Orange: concern in Unit 2; settled by executive decision after the re-test</span>');
      items.push('<span><i class="sbx-sw y"></i>Yellow: investigated and recorded</span>');
      items.push('<span><i class="sbx-sw g"></i>Grey: no concern raised</span>');
    } else {
      items.push('<span><i class="sbx-sw o"></i>Orange: concern</span>');
      items.push('<span><i class="sbx-sw g"></i>Grey: no concern raised</span>');
      items.push("<span>⚖ legal-trigger question</span>");
    }
    return '<p class="sbm-key">' + items.join("") + "</p>";
  }

  function totals(field) {
    var result = { o: 0, y: 0, g: 0 };
    QS.forEach(function (question) { result[question[field]] += 1; });
    return result;
  }

  function stageList(element) {
    var stage = element.dataset.stage;
    var questions = QS.filter(function (question) { return question.stages.indexOf(stage) !== -1; });
    element.innerHTML = '<ul class="sbm-list">' + questions.map(function (question) {
      return '<li><span class="sbm-pair">' + lamp(question.before, question.n) +
        '<span class="sbm-arrow" aria-hidden="true">→</span>' + lamp(question.lamp, question.n) +
        '</span><span><b>Q' + question.n + '.</b> ' + esc(question.q) +
        '<span class="sbm-sr"> Unit 2: ' + WORD[question.before] + '. After the Unit 3 re-test: ' + AFTER[question.lamp] +
        (question.legal ? ". Legal trigger." : ".") + '</span></span></li>';
    }).join("") + '</ul>' + key("pair") + methodLink();
  }

  function checkpoints(element) {
    element.innerHTML = board("before") + key("before") + methodLink();
  }

  function beforeAfter(element) {
    var before = totals("before");
    var after = totals("lamp");
    element.innerHTML = '<div class="sbm-ba"><section><h4>Unit 2 screen</h4>' +
      '<p class="sbm-tot">' + before.o + ' concerns · ' + before.g + ' with no concern raised</p>' + board("before") +
      '</section><section><h4>After the Unit 3 re-test</h4><p class="sbm-tot">' +
      after.y + ' investigated and recorded · ' + after.o + ' settled by executive decision · ' + after.g +
      ' with no concern raised</p>' + board("after") + '</section></div>' + key("both") + methodLink();
  }

  function stages(element) {
    element.innerHTML = '<div class="sbm-table-wrap"><table class="sbm-table"><thead><tr>' +
      '<th scope="col">Stage</th><th scope="col">Unit 2 concerns assigned to this stage</th><th scope="col">Count</th></tr></thead><tbody>' +
      D.stages.map(function (stage) {
        var questions = QS.filter(function (question) {
          return question.before === "o" && question.stages.indexOf(stage.id) !== -1;
        });
        return '<tr><th scope="row"><a href="' + esc(stage.href) + '">' + esc(stage.title) + '</a></th><td><span class="sbm-lamps">' +
          questions.map(function (question) {
            return '<span class="sbm-l" title="Q' + question.n + ': ' + esc(question.q) + '">' + lamp("o", question.n) + '</span>';
          }).join("") +
          '</span><span class="sbm-sr">' + questions.map(function (question) {
            return "Q" + question.n + ". " + question.q;
          }).join("; ") + '</span></td><td>' + questions.length + '</td></tr>';
      }).join("") + '</tbody></table></div>' + methodLink();
  }

  var modes = {
    stage: stageList,
    checkpoints: checkpoints,
    "before-after": beforeAfter,
    stages: stages
  };

  document.querySelectorAll(".sbm").forEach(function (element) {
    var render = modes[element.dataset.mode];
    if (!render) throw new Error("Unknown compact Signal Box board mode: " + element.dataset.mode);
    render(element);
  });
})();
