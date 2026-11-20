/* 京都 嵐山・嵯峨野 — map, list, spot detail, intro and language switch.
   Data: ../data/routes/arashiyama.json（写真は ../images/arashiyama/）. Texts: js/i18n.js
   eizan-line/js/app.js の複製。違いは scripts/sync_arashiyama.py の説明を参照
   （テンプレートを更新したら python3 scripts/sync_arashiyama.py で写し直す） */
(function () {
  'use strict';

  // Base map: OpenFreeMap vector tiles (OpenStreetMap data), drawn by MapLibre inside Leaflet,
  // so place names can follow the EN / 日本語 switch. Change only this block to switch provider.
  var BASEMAP = {
    style: 'https://tiles.openfreemap.org/styles/liberty',
    worker: '../vendor/maplibre/maplibre-gl-csp-worker.js',
    attribution: '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> ' +
      '<a href="https://www.openmaptiles.org/" target="_blank" rel="noopener">&copy; OpenMapTiles</a> ' +
      'Data from <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>',
    maxZoom: 19,
    // shops, cafes and other points of interest: the map is about the spots in this guide
    hide: ['poi_r20', 'poi_r7', 'poi_r1']
  };
  var gl = null, glReady = false;
  var PHOTO_ZOOM = 16;          // show photo cards at this zoom and closer（嵐山はスポットが近いので16から）
  var WIDE = window.matchMedia('(min-width: 900px)');
  var I18N = window.ARASHIYAMA_I18N;
  // 2026-11-20 に番号を振り直した（出町柳スタート）ので、「行った」印は新しいキーで保存し直す
  var KEY_LANG = 'kyoto-maps-lang', KEY_SEEN = 'kyoto-maps-arashiyama-intro-seen', KEY_VISITED = 'kyoto-maps-arashiyama-visited-v2';

  var $ = function (id) { return document.getElementById(id); };
  var panel = $('panel'), viewList = $('view-list'), viewDetail = $('view-detail'), intro = $('intro');
  var data, spots = [], byNo = {}, map, markers = {}, photoMode = null, activeNo = null, lang = 'en';
  var visited = {}, resetArmed = false, locLayer = null, toastTimer = null;
  // 「選んで回る」: mode は 'all'（全部回る）か 'pick'（選んで回る）。picks は選んだ場所の番号
  var KEY_MODE = 'kyoto-maps-arashiyama-mode', KEY_PICKS = 'kyoto-maps-arashiyama-picks';
  var mode = 'all', picks = {}, routeLine = null;

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  // a photo is a file name, or {file, credit: {author, license, page}} for a photo taken from the web
  function photoFile(p) { return typeof p === 'string' ? p : p.file; }
  function photoUrl(p) { return data.photoBase + photoFile(p); }
  function creditHtml(p) {
    var c = p && p.credit;
    if (!c) return '';
    return '<a href="' + esc(c.page) + '" target="_blank" rel="noopener noreferrer">' + esc(T().photoBy) + esc(c.author) + ' / ' + esc(c.license) + '</a>';
  }
  function showCredit(el, p) {
    if (!el) return;
    var h = creditHtml(p);
    el.innerHTML = h;
    el.hidden = !h;
  }
  function T() { return I18N[lang]; }
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  function todayJST() { return new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10); }
  function inRange(from, to) { var d = todayJST(); return (!from || d >= from) && (!to || d <= to); }
  function fill(str, map) { return str.replace(/\{(\w+)\}/g, function (m, k) { return map[k]; }); }
  function loadVisited() {
    try { (JSON.parse(load(KEY_VISITED) || '[]') || []).forEach(function (n) { visited[n] = true; }); } catch (e) {}
  }
  function saveVisited() { store(KEY_VISITED, JSON.stringify(Object.keys(visited).map(Number))); }

  /* ---------- 選んで回る ---------- */
  // 自分で選ぶ場所（picks）と、選んだ場所に合わせて自動で入る駅・バス停（auto）は data.plan に書いてある
  function loadPlan() {
    mode = load(KEY_MODE) === 'pick' && data.plan ? 'pick' : 'all';
    try { (JSON.parse(load(KEY_PICKS) || '[]') || []).forEach(function (n) { if (isPick(n)) picks[n] = true; }); } catch (e) {}
  }
  function savePlan() { store(KEY_MODE, mode); store(KEY_PICKS, JSON.stringify(Object.keys(picks).map(Number))); }
  function isPick(no) { return !!(data.plan && data.plan.picks.indexOf(no) >= 0); }
  function anyPicked(list) { return (list || []).some(function (n) { return picks[n]; }); }
  function ruleOk(r) {
    if (!r || r.always) return true;
    if (!anyPicked(r.any)) return false;
    if (r.andAny && !anyPicked(r.andAny)) return false;
    if (r.none && anyPicked(r.none)) return false;
    return true;
  }
  function included(no) {
    if (mode !== 'pick' || !data.plan) return true;
    if (isPick(no)) return !!picks[no];
    return ruleOk(data.plan.auto[no]);
  }
  // 選んだ組み合わせによって行き方が変わるところの一言（例：古今 藤やを選んだらバスに乗らず歩く）
  function hintsFor(no) {
    if (mode !== 'pick' || !data.plan || !data.plan.hints) return [];
    return data.plan.hints.filter(function (h) { return h.spot === no && ruleOk(h.rule); });
  }
  function routeSpots() { return spots.filter(function (s) { return included(s.no); }); }
  function neighbor(no, dir) {       // 前後の「ルートに入っている」スポット
    for (var n = no + dir; byNo[n]; n += dir) if (included(n)) return byNo[n];
    return null;
  }
  function pickCount() { return Object.keys(picks).length; }

  /* ---------- 写真提供の表示（例：鞍馬温泉の写真に「写真提供：くらま温泉」） ---------- */
  // data のスポットに photoCredit: {files: [...], text: {ja, en}} があれば、その写真を表示している間だけ出す
  function pcText(s, i) {
    var c = s && s.photoCredit, f = s && s.photos[i];
    if (!c || f == null) return '';
    var file = typeof f === 'string' ? f : f.file;
    return c.files.indexOf(file) >= 0 ? c.text[lang] : '';
  }
  function setPc(el, s, i) {
    if (!el) return;
    var t = pcText(s, i);
    el.textContent = t;
    el.hidden = !t;
  }
  function slideIndex(el) { return Math.round(el.scrollLeft / Math.max(1, el.clientWidth)); }
  function toast(msg) {
    var el = $('toast');
    el.textContent = msg; el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.hidden = true; }, 4000);
  }
  // Number badge: a square with inward-curved sides, as on the momiji site
  var MARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M2,2 Q20,7.5 38,2 Q32.5,20 38,38 Q20,32.5 2,38 Q7.5,20 2,2 Z"/></svg>';
  function badge(no, extra) {
    return '<span class="badge' + (no === 1 ? ' start' : '') + (extra ? ' ' + extra : '') + '">' + MARK + '<span>' + no + '</span></span>';
  }
  function nameHtml(s, tag) {
    var other = lang === 'ja' ? 'en' : 'ja';
    var alt = s.name[other] !== s.name[lang] ? '<i lang="' + other + '">' + esc(s.name[other]) + '</i>' : '';
    return '<' + tag + ' class="nm"><b>' + esc(s.name[lang]) + '</b>' + alt + '</' + tag + '>';
  }
  function sectionOf(no) {
    return (data.sections || []).filter(function (x) { return no >= x.first && no <= x.last; })[0];
  }
  function areaOf(sec, l) {
    if (!sec) return '';
    return sec.day != null ? I18N[l].intro.day[sec.day].area : sec.area[l];
  }

  var ICON = {
    official: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
    timetable: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    info: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5h.01"/></svg>',
    ext: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    route: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/></svg>',
    warn: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l9.5 17h-19z"/><path d="M12 10v4.5M12 17.5h.01"/></svg>',
    cash: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/></svg>'
  };

  function pickLang() {
    var q = (location.search.match(/[?&]lang=(ja|en)\b/) || [])[1];
    if (q) return q;
    var saved = load(KEY_LANG);
    if (saved === 'ja' || saved === 'en') return saved;
    var langs = navigator.languages || [navigator.language || ''];
    return /^ja\b/i.test(langs[0] || '') ? 'ja' : 'en';
  }

  var TIME_RE = /^(おすすめ(?:訪問|出発|移動|到着|乗船)時間|営業時間|Recommended [A-Za-z ]*(?:time|arrival|departure|boat)|Opening hours)\s*[：:]/;
  function recTime(s) {
    var re = lang === 'ja' ? /^おすすめ(?:訪問|出発|移動|到着|乗船)時間\s*[：:]\s*(.+)$/ : /^Recommended [A-Za-z ]*(?:time|arrival|departure|boat)\s*:\s*(.+)$/;
    var lines = s.text[lang].split('\n');
    for (var i = 0; i < lines.length; i++) {
      var m = lines[i].match(re);
      if (m) return m[1].trim();
    }
    return '';
  }

  function textToHtml(text) {
    var out = [], para = [];
    function flush() { if (para.length) { out.push('<p>' + para.join('<br>') + '</p>'); para = []; } }
    text.split('\n').forEach(function (raw) {
      var line = raw.trim();
      if (!line) { flush(); return; }
      if (TIME_RE.test(line)) { flush(); out.push('<p class="time">' + esc(line) + '</p>'); return; }
      para.push(esc(line));
    });
    flush();
    return out.join('');
  }

  /* ---------- static texts ---------- */
  function applyTexts() {
    var t = T();
    document.documentElement.lang = t.htmlLang;
    document.title = t.docTitle;
    $('t-main').textContent = t.titleMain;
    $('t-alt').textContent = t.titleSub;
    $('t-alt').lang = lang === 'ja' ? 'en' : 'ja';
    [].forEach.call(document.querySelectorAll('[data-t]'), function (el) { el.textContent = t[el.dataset.t]; });
    [].forEach.call(document.querySelectorAll('[data-t-html]'), function (el) { el.innerHTML = t[el.dataset.tHtml]; });
    [].forEach.call(document.querySelectorAll('[data-t-aria]'), function (el) { el.setAttribute('aria-label', t[el.dataset.tAria]); });
    [].forEach.call(document.querySelectorAll('.langsw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });
    renderProgress();
  }

  function renderProgress() {
    var r = routeSpots();
    var n = r.filter(function (s) { return visited[s.no]; }).length, t = r.length || spots.length;
    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
    // 「選んで回る」の設定（data.plan）がないマップでは、切り替えボタンごと出さない
    document.querySelector('.modesw').hidden = !(data && data.plan);
    $('pick-box').hidden = mode !== 'pick';
    $('pick-count').textContent = pickCount() ? fill(T().pickCount, { n: pickCount(), t: r.length }) : T().pickEmpty;
    $('progress-label').textContent = fill(T().progress, { n: n, t: t });
    $('progress-fill').style.width = (t ? Math.round(n / t * 100) : 0) + '%';
    $('btn-reset').hidden = n === 0;
    $('btn-reset').textContent = resetArmed ? T().resetAsk : T().reset;
  }

  function toggleVisited(no) {
    if (visited[no]) delete visited[no]; else visited[no] = true;
    saveVisited();
    resetArmed = false;
    if (markers[no]) markers[no].setIcon(iconFor(byNo[no], photoMode, no === activeNo));
    updateListItem(no);
    renderProgress();
    if (activeNo === no && !viewDetail.hidden) renderVisitBtn(byNo[no]);
  }

  function setLang(l) {
    if (l === lang) return;
    lang = l;
    store(KEY_LANG, l);
    applyTexts();
    applyMapLang();
    renderList();
    refreshIcons(true);
    if (!intro.hidden) renderIntro();
    if (!viewDetail.hidden && activeNo) renderDetail(byNo[activeNo]);
  }

  /* ---------- base map ---------- */
  // English: the English name from OpenStreetMap, else its romaji; places with neither get no label
  // (no automatic transliteration, which gives Chinese readings for Japanese names).
  // Japanese: the Japanese name.
  function labelExpr(l) {
    return l === 'ja'
      ? ['coalesce', ['get', 'name:ja'], ['get', 'name']]
      : ['coalesce', ['get', 'name:en'], ['get', 'name:ja-Latn'], ''];
  }

  function applyMapLang() {
    if (!gl || !glReady) return;
    window.KM_BASEMAP.setLang(gl, lang);   // 地図の文字を EN / 日本語 に合わせる
  }

  // 地図の見た目は全マップ共通の assets/basemap.js（Googleマップに近いスタイル）
  function addBaseMap() {
    if (!window.KM_BASEMAP) return;
    var layer = window.KM_BASEMAP.addTo(map, { lang: lang, worker: BASEMAP.worker, maxZoom: BASEMAP.maxZoom });
    if (!layer) return;
    gl = layer.getMaplibreMap();
    gl.on('style.load', function () { glReady = true; applyMapLang(); });
  }

  /* ---------- markers ---------- */
  function iconFor(s, withPhoto, active) {
    var start = s.no === 1 ? ' start' : '';
    var num = badge(s.no);
    var cls = 'mk' + (active ? ' is-active' : '') + (visited[s.no] ? ' visited' : '') + (included(s.no) ? '' : ' is-off');
    var dx = s._dup * 34;     // spots that share one location are drawn side by side
    if (!withPhoto) {
      return L.divIcon({ className: cls, html: num, iconSize: [32, 32], iconAnchor: [16 - dx, 16] });
    }
    var html = '<div class="m-card">' + num +
      '<img src="' + photoUrl(s.photos[0]) + '" alt="" loading="lazy" decoding="async">' +
      '<span class="m-label"><b>' + esc(s.name[lang]) + '</b><small>' + esc(s.kind[lang]) + '</small></span></div>';
    return L.divIcon({ className: cls, html: html, iconSize: [158, 52], iconAnchor: [28, 58 + s._dup * 64] });
  }

  function refreshIcons(force) {
    var want = map.getZoom() >= PHOTO_ZOOM;
    if (!force && want === photoMode) return;
    photoMode = want;
    spots.forEach(function (s) { markers[s.no].setIcon(iconFor(s, want, s.no === activeNo)); });
  }

  function setActive(no) {
    var prev = activeNo;
    activeNo = no;
    [prev, no].forEach(function (n) {
      if (n && markers[n]) {
        markers[n].setIcon(iconFor(byNo[n], photoMode, n === activeNo));
        markers[n].setZIndexOffset(n === activeNo ? 1000 : 0);
      }
    });
    var items = document.querySelectorAll('#list button.l-main');
    for (var i = 0; i < items.length; i++) {
      items[i].setAttribute('aria-current', String(Number(items[i].dataset.no) === no));
    }
  }

  /* ---------- panel / routing ---------- */
  function setHash(h) {
    if (h) { location.hash = h; }
    else { history.pushState(null, '', location.pathname + location.search); route(); }
  }

  function openPanel(mode) {
    panel.classList.remove('mode-list', 'mode-detail');
    panel.classList.add('mode-' + mode, 'open');
    document.body.classList.add('sheet-open');
    $('btn-list').setAttribute('aria-expanded', 'true');
  }
  function closePanel() {
    panel.classList.remove('open');
    document.body.classList.remove('sheet-open');
    $('btn-list').setAttribute('aria-expanded', 'false');
  }

  function route() {
    showRoute();
    updateTabs();
  }

  // Phones: highlight the tab for what is on screen (the spot details count as part of the list)
  function updateTabs() {
    var cur = !intro.hidden ? 'about' : (panel.classList.contains('open') && !WIDE.matches ? 'list' : 'map');
    [].forEach.call(document.querySelectorAll('#tabbar button'), function (b) {
      if (b.dataset.tab === cur) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
    });
  }

  function showRoute() {
    if (location.hash === '#about') { showIntro(); return; }
    hideIntro();
    // #spot-16 の形。番号だけの #16 でも同じスポットを開く
    var m = location.hash.match(/^#spot-(\d+)$/) || location.hash.match(/^#(\d+)$/);
    var no = m ? Number(m[1]) : 0;
    if (no && byNo[no]) {
      showDetail(no);
      return;
    }
    viewDetail.hidden = true;
    viewList.hidden = false;
    setActive(null);
    if (location.hash === '#list') openPanel('list');
    else if (WIDE.matches) openPanel('list');
    else closePanel();
  }

  /* ---------- intro ---------- */
  function introPhoto(p) { return photoUrl(byNo[p[0]].photos[p[1]]); }
  // Toshi 個人のマップなので、ロゴは文字だけ
  function logo(cls) {
    return '<span class="' + cls + ' in-brand">TOSHI’S MAPS</span>';
  }
  var CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';

  function renderIntro() {
    var t = T(), x = t.intro;
    var lsw = '<div class="langsw" role="group" aria-label="Language / 言語">' +
      '<button type="button" data-lang="en" lang="en" aria-pressed="' + (lang === 'en') + '">EN</button>' +
      '<button type="button" data-lang="ja" lang="ja" aria-pressed="' + (lang === 'ja') + '">日本語</button></div>';
    $('intro-card').innerHTML =
      '<div class="in-top">' + logo('in-logo') +
        '<div class="in-top-r"><a class="in-home" href="../">' + esc(t.allMaps) + '</a>' + lsw +
        '<button type="button" class="iconbtn in-x" data-act="close" aria-label="' + esc(t.close) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div></div>' +
      '<div class="in-scroll">' +
        // how to use the map comes first
        '<section class="in-sec"><h2 class="in-h2">' + esc(x.howHead) + '</h2><ol class="in-how">' +
          x.how.map(function (h, i) {
            return '<li><span class="in-num">' + (i + 1) + '</span><div><b>' + esc(h.title) + '</b><p>' + esc(h.text) + '</p></div></li>';
          }).join('') +
        '</ol></section>' +
        '<section class="in-hero">' +
          '<div class="in-hero-txt">' +
            '<p class="in-kicker">' + esc(x.kicker) + '</p>' +
            '<h1 class="in-h1" id="intro-h">' + esc(x.h1) + '</h1>' +
            '<p class="in-lead">' + esc(x.lead) + '</p>' +
          '</div>' +
          '<figure class="in-fav">' +
            '<img src="' + introPhoto(x.favPhoto) + '" alt="' + esc(x.favName) + '" decoding="async">' +
            '<figcaption><span class="in-fav-label">' + esc(x.favLabel) + '</span>' +
            '<span class="in-fav-name">' + esc(x.favName) + '</span>' +
            '<span class="in-fav-text">' + esc(x.favText) + '</span></figcaption>' +
          '</figure>' +
        '</section>' +
        '<section class="in-sec"><h2 class="in-h2">' + esc(x.whoHead) + '</h2><ul class="in-who">' +
          x.who.map(function (w) { return '<li><span class="in-ck">' + CHECK + '</span><span>' + esc(w) + '</span></li>'; }).join('') +
        '</ul></section>' +
        '<section class="in-sec"><h2 class="in-h2">' + esc(x.dayHead) + '</h2><ol class="in-day">' +
          x.day.map(function (d) {
            return '<li><div class="in-time">' + (x.from ? '<span class="in-from">' + esc(x.from) + '</span>' : '') +
              '<span class="in-clock">' + esc(d.time + x.timeSuffix) + '</span>' +
              (d.note ? '<span class="in-note">' + esc(d.note) + '</span>' : '') + '</div>' +
              '<span class="in-dot" aria-hidden="true"></span>' +
              '<img src="' + introPhoto(d.photo) + '" alt="" loading="lazy" decoding="async">' +
              '<div class="in-stop"><span class="in-area">' + esc(d.area) + '</span>' +
              '<span class="in-title">' + esc(d.title) + '</span>' +
              (d.badge ? '<span class="in-badge">' + CHECK + esc(d.badge) + '</span>' : '') +
              '<span class="in-text">' + esc(d.text) + '</span></div></li>';
          }).join('') +
        '</ol></section>' +
        '<section class="in-sec"><h2 class="in-h2">' + esc(x.dealsHead) + '</h2><p class="in-deals-lead">' + esc(x.dealsLead) + '</p><div class="in-deals">' +
          x.deals.map(function (d) {
            return '<div class="in-deal' + (d.best ? ' best' : '') + '">' + (d.best ? '<span class="in-best">' + esc(d.best) + '</span>' : '') +
              '<p class="in-deal-name"><b>' + esc(d.name) + '</b><span>' + esc(d.price) + '</span></p><p>' + esc(d.text) + '</p>' +
              '<a href="' + esc(d.url) + '" target="_blank" rel="noopener noreferrer">' + esc(x.dealsMore) + '</a></div>';
          }).join('') +
        '</div><p class="in-deals-note">' + esc(x.dealsNote) + '</p></section>' +
        '<footer class="in-foot">' + logo('in-logo') +
          '<p>' + esc(x.footer1) + '</p></footer>' +
      '</div>' +
      '<div class="in-cta"><button type="button" class="in-go" data-act="close">' + esc(x.cta) +
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></div>';
  }

  function showIntro() {
    if (intro.hidden) {
      renderIntro();
      intro.hidden = false;
      document.body.classList.add('intro-open');
      var sc = intro.querySelector('.in-scroll'); if (sc) sc.scrollTop = 0;
      $('intro-h').setAttribute('tabindex', '-1');
      $('intro-h').focus({ preventScroll: true });
    }
  }
  function hideIntro() {
    if (!intro.hidden) {
      intro.hidden = true;
      document.body.classList.remove('intro-open');
      store(KEY_SEEN, '1');
    }
  }

  /* ---------- list ---------- */
  function sectionHtml(sec) {
    var x = T().intro, d = sec.day != null ? x.day[sec.day] : null;
    var title = d ? d.title : sec.title[lang];
    return '<li class="sec" role="presentation"><span class="sec-area">' + esc(areaOf(sec, 'en')) +
      '<span lang="ja">' + esc(areaOf(sec, 'ja')) + '</span></span><b>' + esc(title) + '</b></li>';
  }

  function renderList() {
    var lastSec = null;
    $('list').innerHTML = spots.map(function (s) {
      var inc = included(s.no), pickable = mode === 'pick' && isPick(s.no), auto = mode === 'pick' && !isPick(s.no);
      if (auto && !inc) return '';          // 選んだ場所に関係ない駅・バス停は出さない
      var sec = sectionOf(s.no), head = '';
      if (sec && sec !== lastSec) { head = sectionHtml(sec); lastSec = sec; }
      var v = !!visited[s.no];
      var n = s.photos.length;
      return head + '<li class="spot' + (v ? ' is-visited' : '') + (inc ? '' : ' is-off') + '">' +
        // large photos you can swipe through, so the place is easy to picture from the list alone
        '<div class="l-ph"><div class="l-slides" data-open="' + s.no + '">' +
        s.photos.map(function (f, i) {
          return '<img src="' + photoUrl(f) + '" alt=""' + ' loading="lazy" decoding="async">';
        }).join('') + '</div>' + badge(s.no) +
        '<span class="l-cr"' + (creditHtml(s.photos[0]) ? '' : ' hidden') + '>' + creditHtml(s.photos[0]) + '</span>' +
        (n > 1 ? '<span class="l-count">1 / ' + n + '</span>' +
          '<button type="button" class="l-arrow prev" data-step="-1" aria-label="' + esc(T().prevPhoto) + '" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>' +
          '<button type="button" class="l-arrow next" data-step="1" aria-label="' + esc(T().nextPhoto) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>' : '') +
        '<button type="button" class="l-check" data-check="' + s.no + '" aria-pressed="' + v + '" aria-label="' + esc(pad(s.no) + ' ' + s.name[lang] + ': ' + (v ? T().visitOn : T().visitOff)) + '">' +
        '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.8 2.8L16.5 9.5"/></svg></button>' +
        (s.photoCredit ? '<span class="l-pc"' + (pcText(s, 0) ? '' : ' hidden') + '>' + esc(pcText(s, 0)) + '</span>' : '') + '</div>' +
        '<button type="button" class="l-main" data-no="' + s.no + '" aria-current="' + (s.no === activeNo) + '">' +
        '<span class="l-txt">' + nameHtml(s, 'span') +
        '<span class="l-tags"><span class="kind">' + esc(s.kind[lang]) + '</span>' +
        (auto ? '<span class="kind auto">' + esc(T().autoTag) + '</span>' : '') + '</span>' +
        (s.caution ? '<span class="l-caution">' + ICON.warn + esc(s.caution[lang]) + '</span>' : '') +
        '<span class="l-blurb">' + esc(s.blurb[lang]) + '</span>' +
        '<span class="l-more">' + esc(T().seeDetails) + '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></span></span></button>' +
        (pickable ? '<div class="l-pickrow"><button type="button" class="l-pick" data-pick="' + s.no + '" aria-pressed="' + inc + '">' +
          (inc ? '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>' : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>') +
          '<span>' + esc(inc ? T().pickOn : T().pickOff) + '</span></button></div>' : '') +
        '</li>';
    }).join('');
  }

  // 選んだ場所が変わったら、地図の点線・番号・一覧・進み具合をまとめて更新する
  function updateRoute() {
    if (routeLine) routeLine.setLatLngs(routeSpots().map(function (s) { return [s.lat, s.lng]; }));
    refreshIcons(true);
    renderList();
    renderProgress();
    if (activeNo && !viewDetail.hidden) renderDetail(byNo[activeNo]);
  }
  function keepInView(no, fn) {      // 一覧を描き直しても、押したカードが画面の同じ位置にあるようにする
    var el = document.querySelector('#list [data-pick="' + no + '"]');
    var y0 = el ? el.getBoundingClientRect().top : null;
    fn();
    var el2 = document.querySelector('#list [data-pick="' + no + '"]');
    if (y0 !== null && el2) viewList.scrollTop += el2.getBoundingClientRect().top - y0;
  }
  function togglePick(no) {
    if (picks[no]) delete picks[no]; else picks[no] = true;
    savePlan();
    keepInView(no, updateRoute);
  }
  function setMode(m) {
    if (m === mode) return;
    mode = m;
    savePlan();
    updateRoute();
  }

  // Update one spot in the list in place, so its photos and the scroll position stay where they are
  function updateListItem(no) {
    var c = document.querySelector('#list button[data-check="' + no + '"]');
    if (!c) { renderList(); return; }
    var v = !!visited[no], s = byNo[no];
    c.setAttribute('aria-pressed', String(v));
    c.setAttribute('aria-label', pad(no) + ' ' + s.name[lang] + ': ' + (v ? T().visitOn : T().visitOff));
    c.closest('li').classList.toggle('is-visited', v);
  }

  /* ---------- detail ---------- */
  function updateCounter() {
    var el = $('slides'), n = el.children.length;
    var i = Math.round(el.scrollLeft / Math.max(1, el.clientWidth));
    $('counter').textContent = (i + 1) + ' / ' + n;
    $('slide-prev').disabled = i <= 0;
    $('slide-next').disabled = i >= n - 1;
    if (activeNo && byNo[activeNo]) showCredit($('ph-credit'), byNo[activeNo].photos[i]);
  }

  function renderDetail(s) {
    var t = T(), other = lang === 'ja' ? 'en' : 'ja';
    $('ph-no').innerHTML = badge(s.no, 'on-photo');
    setPc($('ph-pc'), s, slideIndex($('slides')));
    var sec = sectionOf(s.no);
    $('ph-area').innerHTML = esc(areaOf(sec, 'en')) + '<span lang="ja">' + esc(areaOf(sec, 'ja')) + '</span>';
    $('d-name').textContent = s.name[lang];
    $('d-alt').textContent = s.name[other] !== s.name[lang] ? s.name[other] : '';
    $('d-alt').lang = other;
    $('d-kind').textContent = s.kind[lang];
    $('d-blurb').textContent = '';

    $('btn-howto-3').hidden = s.no !== 1;
    renderVisitBtn(s);
    renderPickBtn(s);

    var notices = (s.notices || []).filter(function (n) { return inRange(n.from, n.to); });
    $('d-notices').innerHTML = notices.map(function (n) {
      return '<div class="notice">' + ICON.warn + '<div><b>' + esc(n.head ? n.head[lang] : t.noticeHead) + '</b><p>' + esc(n.text[lang]) + '</p>' +
        (n.url ? '<a href="' + esc(n.url) + '" target="_blank" rel="noopener noreferrer">' + esc(t.more) + '</a>' : '') + '</div></div>';
    }).join('') + hintsFor(s.no).map(function (h) {
      return '<div class="notice hint">' + ICON.route + '<div><b>' + esc(t.hintHead) + '</b><p>' + esc(h.text[lang]) + '</p></div></div>';
    }).join('');

    $('d-actions').innerHTML = s.gmaps.map(function (g) {
      var label = s.gmaps.length > 1 ? t.gmapsMany + g.label[lang] : t.gmapsOne;
      return '<a class="btn" href="' + esc(g.url) + '" target="_blank" rel="noopener noreferrer">' +
        '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>' +
        '<span>' + esc(label) + '</span></a>';
    }).join('') + nextRouteHtml(s);

    $('d-text').innerHTML = textToHtml(s.text[lang]);
    $('d-text').lang = lang;
    $('d-links').innerHTML = s.links.map(function (l) {
      return '<a href="' + esc(l.url[lang]) + '" target="_blank" rel="noopener noreferrer" class="lk lk-' + l.kind + '">' + ICON[l.kind] +
        '<span><small>' + esc(t.linkKinds[l.kind]) + '</small>' + esc(l.label[lang]) + '</span>' + ICON.ext + '</a>';
    }).join('');
    $('d-info').innerHTML = infoHtml(s);
    $('share-label').textContent = t.copy;

    var prev = neighbor(s.no, -1), next = neighbor(s.no, 1);   // 選んで回るときは、ルートに入っている前後へ
    $('btn-prev').disabled = !prev;
    $('btn-next').disabled = !next;
    $('prev-label').textContent = prev ? pad(prev.no) + ' ' + prev.name[lang] : '';
    $('next-label').textContent = next ? pad(next.no) + ' ' + next.name[lang] : '';
    [].forEach.call($('slides').querySelectorAll('img'), function (img, i) {
      img.alt = s.name[lang] + ' (' + (i + 1) + '/' + s.photos.length + ')';
    });
    if (activeNo === s.no) updateCounter();   // photo credit in the current language
  }

  function renderPickBtn(s) {
    var show = mode === 'pick' && isPick(s.no), on = !!picks[s.no];
    $('btn-pick').hidden = !show;
    if (!show) return;
    $('btn-pick').setAttribute('aria-pressed', String(on));
    $('btn-pick').querySelector('svg').innerHTML = on ? '<path d="M5 12.5l4.5 4.5L19 7.5"/>' : '<path d="M12 5v14M5 12h14"/>';
    $('pick-label').textContent = on ? T().pickOn : T().pickOff;
  }

  function renderVisitBtn(s) {
    var v = !!visited[s.no];
    $('btn-visit').setAttribute('aria-pressed', String(v));
    $('visit-label').textContent = v ? T().visitOn : T().visitOff;
  }

  function nextRouteHtml(s) {
    var n = neighbor(s.no, 1);
    if (!n) return '';
    var url = 'https://www.google.com/maps/dir/?api=1&origin=' + s.lat + ',' + s.lng + '&destination=' + n.lat + ',' + n.lng + '&travelmode=transit';
    return '<a class="btn ghost next" href="' + esc(url) + '" target="_blank" rel="noopener noreferrer">' + ICON.route +
      '<span>' + esc(T().nextRoute) + '<small>' + pad(n.no) + ' ' + esc(n.name[lang]) + '</small></span></a>';
  }

  function infoHtml(s) {
    var t = T(), inf = s.info || { rows: [] };
    var tm = recTime(s);
    var rows = inf.rows.filter(function (r) { return inRange(r.from, r.until); });
    var html = '';
    if (tm || rows.length) {
      html += '<dl class="facts">' +
        (tm ? '<dt>' + esc(t.suggestedLabel) + '</dt><dd class="soft">' + esc(tm) + '</dd>' : '') +
        rows.map(function (r) { return '<dt>' + esc(t[r.kind]) + '</dt><dd>' + esc(r.text[lang]) + '</dd>'; }).join('') +
        '</dl>';
    }
    if (inf.cash) html += '<p class="cash">' + ICON.cash + esc(t.cash) + '</p>';
    if (rows.length) html += '<p class="checked">' + esc(fill(inf.verified === false ? t.unchecked : t.checked, { d: t.checkedDate })) + '</p>';
    if (inf.tip) html += '<p class="tip">' + esc(inf.tip[lang]) + '</p>';
    return html;
  }

  function showDetail(no) {
    var s = byNo[no];
    viewList.hidden = true;
    viewDetail.hidden = false;
    openPanel('detail');
    $('slides').innerHTML = s.photos.map(function (f, i) {
      return '<img src="' + photoUrl(f) + '" alt=""' + (i === 0 ? '' : ' loading="lazy"') + ' decoding="async">';
    }).join('');
    $('slides').scrollLeft = 0;
    updateCounter();
    renderDetail(s);
    $('detail-scroll').scrollTop = 0;
    setActive(no);
    showCredit($('ph-credit'), s.photos[0]);
    focusMarker(s);
  }

  function focusMarker(s) {
    var z = Math.max(map.getZoom(), 15);
    var target = L.latLng(s.lat, s.lng);
    if (!WIDE.matches) {
      // keep the spot in the strip of map that the bottom sheet leaves visible
      var size = map.getSize();
      var sheet = panel.getBoundingClientRect().height;
      var visibleCenterY = Math.max(60, (size.y - sheet) / 2);
      var p = map.project(target, z).add([0, size.y / 2 - visibleCenterY]);
      target = map.unproject(p, z);
    }
    map.setView(target, z, { animate: true });
  }

  /* ---------- my location (stays on this device; nothing is sent anywhere) ---------- */
  function locate() {
    if (!navigator.geolocation) { toast(T().locateErr); return; }
    toast(T().locating);
    map.locate({ setView: true, maxZoom: 16, enableHighAccuracy: true, timeout: 15000 });
  }
  function onLocated(e) {
    $('toast').hidden = true;
    if (locLayer) map.removeLayer(locLayer);
    locLayer = L.layerGroup([
      L.circle(e.latlng, { radius: e.accuracy, color: '#2E6FD8', weight: 1, fillOpacity: 0.12, interactive: false }),
      L.circleMarker(e.latlng, { radius: 8, color: '#fff', weight: 3, fillColor: '#2E6FD8', fillOpacity: 1, interactive: false })
    ]).addTo(map);
  }

  /* ---------- share ---------- */
  function share() {
    var url = location.href;
    var label = $('share-label');
    if (navigator.share && !WIDE.matches) {
      navigator.share({ title: document.title, url: url }).catch(function () {});
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { label.textContent = T().copied; },
        function () { label.textContent = url; });
    } else {
      label.textContent = url;
    }
  }

  /* ---------- init ---------- */
  // 地図を開いたときは歩くエリア（data.focus）だけを映す。「全体を表示」ボタン（e がある）では全部
  function fitAll(e) {
    var r = routeSpots(), f = !e && data.focus;
    if (f) r = r.filter(function (x) { return x.no >= f.first && x.no <= f.last; });
    var b = L.latLngBounds((r.length >= 2 ? r : spots).map(function (s) { return [s.lat, s.lng]; }));
    map.fitBounds(b, WIDE.matches ? { padding: [40, 40] } : { paddingTopLeft: [20, 150], paddingBottomRight: [20, 80] });
  }

  function init(d) {
    data = d;
    spots = d.spots.slice().sort(function (a, b) { return a.no - b.no; });
    var seen = {};
    spots.forEach(function (s) {
      byNo[s.no] = s;
      var k = s.lat.toFixed(5) + ',' + s.lng.toFixed(5);
      s._dup = seen[k] || 0;
      seen[k] = s._dup + 1;
    });

    lang = pickLang();
    loadVisited();
    loadPlan();
    applyTexts();

    map = L.map('map', { zoomControl: false, attributionControl: false, maxZoom: 19 });
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.control.attribution({ position: WIDE.matches ? 'bottomright' : 'topright' }).addTo(map);

    routeLine = L.polyline(routeSpots().map(function (s) { return [s.lat, s.lng]; }), {
      color: '#AE3A22', weight: 2.5, opacity: 0.75, dashArray: '2 8', lineCap: 'round', interactive: false
    }).addTo(map);

    fitAll();
    addBaseMap();     // after the map has a view: the layer is only created then
    photoMode = map.getZoom() >= PHOTO_ZOOM;
    spots.forEach(function (s) {
      var m = L.marker([s.lat, s.lng], { icon: iconFor(s, photoMode, false), riseOnHover: true, keyboard: true });
      m.on('click', function () { setHash('spot-' + s.no); });
      m.addTo(map);
      markers[s.no] = m;
    });
    map.on('zoomend', function () { refreshIcons(false); });

    renderList();

    document.addEventListener('click', function (e) {
      var lb = e.target.closest('.langsw button[data-lang]');
      if (lb) { setLang(lb.dataset.lang); return; }
      var act = e.target.closest('[data-act="close"]');
      if (act && intro.contains(act)) { setHash(''); }
    });
    intro.addEventListener('click', function (e) { if (e.target === intro) setHash(''); });
    $('list').addEventListener('click', function (e) {
      var c = e.target.closest('button[data-check]');
      if (c) { toggleVisited(Number(c.dataset.check)); return; }
      var pk = e.target.closest('button[data-pick]');
      if (pk) { togglePick(Number(pk.dataset.pick)); return; }
      var st = e.target.closest('button[data-step]');
      if (st) {
        var sl = st.parentNode.querySelector('.l-slides');
        sl.scrollBy({ left: Number(st.dataset.step) * sl.clientWidth, behavior: 'smooth' });
        return;
      }
      var ph = e.target.closest('[data-open]');
      if (ph) { setHash('spot-' + ph.dataset.open); return; }
      var b = e.target.closest('button.l-main');
      if (b) setHash('spot-' + b.dataset.no);
    });
    // photo counter and arrows for each spot in the list ("scroll" does not bubble, so listen while capturing)
    $('list').addEventListener('scroll', function (e) {
      var sl = e.target;
      if (!sl.classList || !sl.classList.contains('l-slides')) return;
      window.requestAnimationFrame(function () {
        var n = sl.children.length, i = Math.round(sl.scrollLeft / Math.max(1, sl.clientWidth));
        var box = sl.parentNode, c = box.querySelector('.l-count');
        if (c) c.textContent = (i + 1) + ' / ' + n;
        var sp = byNo[Number(sl.dataset.open)];
        if (sp) showCredit(box.querySelector('.l-cr'), sp.photos[i]);
        var pv = box.querySelector('.l-arrow.prev'), nx = box.querySelector('.l-arrow.next');
        if (pv) pv.disabled = i <= 0;
        if (nx) nx.disabled = i >= n - 1;
      });
    }, true);
    $('btn-visit').addEventListener('click', function () { if (activeNo) toggleVisited(activeNo); });
    // 写真提供の表示を、めくった写真に合わせる（一覧と詳細）
    $('list').addEventListener('scroll', function (e) {
      var sl = e.target;
      if (!sl.classList || !sl.classList.contains('l-slides')) return;
      var sp = byNo[Number(sl.dataset.open)];
      if (sp && sp.photoCredit) setPc(sl.parentNode.querySelector('.l-pc'), sp, slideIndex(sl));
    }, true);
    $('slides').addEventListener('scroll', function () {
      if (activeNo && byNo[activeNo]) setPc($('ph-pc'), byNo[activeNo], slideIndex($('slides')));
    }, { passive: true });
    $('btn-pick').addEventListener('click', function () {
      if (!activeNo) return;
      if (picks[activeNo]) delete picks[activeNo]; else picks[activeNo] = true;
      savePlan(); updateRoute();
    });
    [].forEach.call(document.querySelectorAll('.modesw button'), function (b) {
      b.addEventListener('click', function () { setMode(b.dataset.mode); });
    });
    $('btn-pick-all').addEventListener('click', function () {
      data.plan.picks.forEach(function (n) { picks[n] = true; }); savePlan(); updateRoute();
    });
    $('btn-pick-none').addEventListener('click', function () { picks = {}; savePlan(); updateRoute(); });
    $('btn-reset').addEventListener('click', function () {
      if (!resetArmed) { resetArmed = true; renderProgress(); return; }
      visited = {}; saveVisited(); resetArmed = false;
      refreshIcons(true); renderList(); renderProgress();
      if (activeNo && !viewDetail.hidden) renderVisitBtn(byNo[activeNo]);
    });
    $('btn-locate').addEventListener('click', locate);
    map.on('locationfound', onLocated);
    map.on('locationerror', function () { toast(T().locateErr); });
    ['btn-howto', 'btn-howto-2', 'btn-howto-3'].forEach(function (id) {
      $(id).addEventListener('click', function () { setHash('about'); });
    });
    $('tabbar').addEventListener('click', function (e) {
      var b = e.target.closest('button[data-tab]');
      if (!b) return;
      var tab = b.dataset.tab;
      if (tab === 'map') setHash('');
      else if (tab === 'about') setHash('about');
      else if (location.hash === '#list') viewList.scrollTo({ top: 0, behavior: 'smooth' });  // already open: back to the top
      else setHash('list');
    });
    // Phones: tapping the map above the sheet, or pulling the sheet down by its top edge, goes back to the map
    map.on('click', function () {
      if (!WIDE.matches && panel.classList.contains('open')) setHash('');
    });
    var pullY = null;
    panel.addEventListener('touchstart', function (e) {
      pullY = null;
      if (WIDE.matches) return;
      var h = e.target.closest('.grab, .list-head, .detail-head');
      if (!h || (h.classList.contains('list-head') && viewList.scrollTop > 0)) return;
      pullY = e.touches[0].clientY;
    }, { passive: true });
    panel.addEventListener('touchend', function (e) {
      if (pullY === null) return;
      var dy = e.changedTouches[0].clientY - pullY;
      pullY = null;
      if (dy > 60) setHash('');
    }, { passive: true });
    $('btn-list').addEventListener('click', function () {
      if (panel.classList.contains('open') && !WIDE.matches) setHash('');
      else setHash('list');
    });
    $('btn-fit').addEventListener('click', fitAll);
    $('btn-list-close').addEventListener('click', function () { setHash(''); });
    $('btn-back').addEventListener('click', function () { setHash('list'); });
    $('btn-detail-close').addEventListener('click', function () { setHash(''); });
    $('btn-prev').addEventListener('click', function () { var p = neighbor(activeNo, -1); if (p) setHash('spot-' + p.no); });
    $('btn-next').addEventListener('click', function () { var n = neighbor(activeNo, 1); if (n) setHash('spot-' + n.no); });
    $('btn-share').addEventListener('click', share);
    $('slides').addEventListener('scroll', function () { window.requestAnimationFrame(updateCounter); }, { passive: true });
    $('slide-prev').addEventListener('click', function () { $('slides').scrollBy({ left: -$('slides').clientWidth, behavior: 'smooth' }); });
    $('slide-next').addEventListener('click', function () { $('slides').scrollBy({ left: $('slides').clientWidth, behavior: 'smooth' }); });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      if (!intro.hidden) setHash('');
      else if (panel.classList.contains('open') && !WIDE.matches) setHash('');
    });
    window.addEventListener('hashchange', route);
    if (WIDE.addEventListener) WIDE.addEventListener('change', function () { map.invalidateSize(); route(); });

    // Opening the map with no spot in the address: always show how to use it first
    if (!location.hash) history.replaceState(null, '', location.pathname + location.search + '#about');
    route();
  }

  fetch('../data/routes/arashiyama.json?v=5')
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(init)
    .catch(function () {
      var l = pickLang();
      document.body.insertAdjacentHTML('beforeend', '<p class="noscript">' + esc(I18N[l].loadError) + '</p>');
    });
})();
