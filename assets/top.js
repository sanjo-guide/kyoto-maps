/* トップページ（マップ一覧）: 言語の切り替えと、「いつでも行ける／季節限定」のタブ */
/* 言語の切り替え。選んだ言語は各マップにも引き継ぐ（同じサイト内なので保存先を共有できる） */
(function () {
  var KEYS = ['kyoto-maps-lang', 'kanazawa-lang'];
  function load() {
    var q = (location.search.match(/[?&]lang=(ja|en)\b/) || [])[1];
    if (q) return q;
    try { var s = localStorage.getItem(KEYS[0]); if (s === 'ja' || s === 'en') return s; } catch (e) {}
    return /^ja\b/i.test((navigator.languages || [navigator.language || ''])[0] || '') ? 'ja' : 'en';
  }
  function apply(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-' + lang + ']').forEach(function (el) { el.innerHTML = el.getAttribute('data-' + lang); });
    document.querySelectorAll('.lang button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); });
  }
  document.querySelector('.lang').addEventListener('click', function (e) {
    var b = e.target.closest('button[data-lang]'); if (!b) return;
    KEYS.forEach(function (k) { try { localStorage.setItem(k, b.dataset.lang); } catch (err) {} });
    apply(b.dataset.lang);
  });
  apply(load());
})();

/* 「いつでも行ける」「季節限定」のタブ。開いていたタブは覚えておく（マップから戻ったときに同じタブを出す） */
(function () {
  var KEY = 'kyoto-maps-top-tab';
  var tabs = document.querySelectorAll('.tabs [role="tab"]');
  function show(name, save) {
    if (name !== 'season') name = 'year';
    tabs.forEach(function (b) { b.setAttribute('aria-selected', String(b.dataset.tab === name)); });
    document.getElementById('panel-year').hidden = name !== 'year';
    document.getElementById('panel-season').hidden = name !== 'season';
    var now = document.getElementById('now'); if (now.dataset.on) now.hidden = name !== 'year';
    if (save) { try { sessionStorage.setItem(KEY, name); } catch (e) {} history.replaceState(null, '', name === 'season' ? '#season' : location.pathname + location.search); }
  }
  document.querySelector('.tabs').addEventListener('click', function (e) {
    var b = e.target.closest('[role="tab"]'); if (b) show(b.dataset.tab, true);
  });
  // 今の季節のマップがあるときは、ひとこと案内を出す
  var m = new Date().getMonth() + 1, d = new Date().getDate();
  var cur = (m === 3 || (m === 4 && d <= 20)) ? ['h-spring', '今は桜の季節です。桜のマップを見る →', 'It’s cherry-blossom season. See the spring maps →']
          : (m >= 6 && m <= 10) ? ['h-summer', '夏は高原へ。白馬のマップを見る →', 'Summer is for the highlands. See the Hakuba map →']
          : (m === 11 || (m === 12 && d <= 10)) ? ['h-autumn', '今は紅葉の季節です。紅葉のマップを見る →', 'It’s maple season. See the autumn maps →'] : null;
  var now = document.getElementById('now'), link = now.querySelector('a');
  if (cur) {
    now.dataset.on = '1'; link.setAttribute('data-ja', cur[1]); link.setAttribute('data-en', cur[2]);
    link.textContent = cur[document.documentElement.lang === 'en' ? 2 : 1];
    link.addEventListener('click', function (e) {
      e.preventDefault(); show('season', true);
      var sec = document.getElementById(cur[0]).closest('.group'), panel = document.getElementById('panel-season');
      panel.insertBefore(sec, panel.querySelector('.group'));   // 今の季節の段をいちばん上へ
      document.querySelector('.tabs').scrollIntoView();
    });
    var sec0 = document.getElementById(cur[0]).closest('.group'), panel0 = document.getElementById('panel-season');
    panel0.insertBefore(sec0, panel0.querySelector('.group'));
  }
  var target = location.hash.length > 1 && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  var start = location.hash === '#season' || (target && target.closest('#panel-season')) ? 'season' : (target && target.closest('#panel-year') ? 'year' : null);
  if (!start) { try { start = sessionStorage.getItem(KEY); } catch (e) {} }
  show(start || 'year', false);
})();

/* 地域（季節）のボタン：押すと、その地域のマップだけを出す（上下に行き来しなくてよいように）。
   下へスクロールすると上に細いバー（いまの地域と「地域を変える」）が残り、その場で地域を変えられる */
(function () {
  var KEY = 'kyoto-maps-top-region';
  var saved = {}; try { saved = JSON.parse(sessionStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  var bar = document.getElementById('regbar'), lbl = document.getElementById('reglbl'), chg = document.getElementById('regchg');
  var sheet = document.getElementById('sheet'), list = document.getElementById('sheet-list'), sh = document.getElementById('sheet-h');
  function en() { return document.documentElement.lang === 'en'; }
  function setText(el, ja, e) { el.setAttribute('data-ja', ja); el.setAttribute('data-en', e); el.innerHTML = en() ? e : ja; }
  function curNav() { return document.getElementById(document.getElementById('panel-season').hidden ? 'jump-year' : 'jump-season'); }
  function secOf(a) { var el = document.getElementById(a.getAttribute('href').slice(1)); return el && el.closest('.group'); }
  function choose(nav, r, save) {
    var panel = nav.closest('.panel'), cur = null;
    nav.querySelectorAll('a').forEach(function (a) { var on = (a.dataset.r || a.getAttribute('href').slice(1)) === r; a.setAttribute('aria-current', String(on)); if (on) cur = a; });
    if (!cur) { r = 'all'; cur = nav.querySelector('[data-r="all"]'); cur.setAttribute('aria-current', 'true'); }
    var target = r === 'all' ? null : secOf(cur);
    panel.querySelectorAll('.group').forEach(function (g) { g.hidden = !!target && g !== target; });
    nav.dataset.cur = r;
    if (save) { saved[nav.id] = r; try { sessionStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {} }
    update();
  }
  document.querySelectorAll('.jump').forEach(function (nav) {
    var total = 0;
    nav.querySelectorAll('a:not([data-r])').forEach(function (a) { var sec = secOf(a); if (sec) { var n = sec.querySelectorAll('.cards > li').length; a.setAttribute('data-n', n); total += n; } });
    nav.querySelector('[data-r="all"]').setAttribute('data-n', total);
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      e.preventDefault(); choose(nav, a.dataset.r || a.getAttribute('href').slice(1), true);
    });
    var h = location.hash.slice(1), fromHash = h && nav.querySelector('a[href="#' + h + '"]');
    choose(nav, fromHash ? h : (saved[nav.id] || 'all'), false);
  });
  // 上に残る細いバー
  function update() {
    var nav = curNav(), r = nav.getBoundingClientRect();
    bar.hidden = r.bottom > document.querySelector('.bar').getBoundingClientRect().bottom + 4;
    var a = nav.querySelector('[aria-current="true"]');
    if (a) setText(lbl, (nav.id === 'jump-year' ? '地域：' : '季節：') + a.getAttribute('data-ja'), (nav.id === 'jump-year' ? 'Region: ' : 'Season: ') + a.getAttribute('data-en'));
    setText(chg, nav.id === 'jump-year' ? '地域を変える ▾' : '季節を変える ▾', nav.id === 'jump-year' ? 'Change ▾' : 'Change ▾');
  }
  window.addEventListener('scroll', update, { passive: true });
  document.querySelector('.tabs').addEventListener('click', function () { setTimeout(update, 0); });
  // 選ぶ画面
  function close() { sheet.hidden = true; list.innerHTML = ''; document.getElementById('regopen').focus(); }
  document.getElementById('regopen').addEventListener('click', function () {
    var nav = curNav(), c = nav.cloneNode(true);
    c.removeAttribute('id'); list.innerHTML = ''; list.appendChild(c);
    setText(sh, nav.id === 'jump-year' ? '地域を選ぶ' : '季節を選ぶ', nav.id === 'jump-year' ? 'Choose a region' : 'Choose a season');
    c.addEventListener('click', function (e) {
      var a = e.target.closest('a'); if (!a) return;
      e.preventDefault(); choose(nav, a.dataset.r || a.getAttribute('href').slice(1), true); close();
      // 地域のボタンがちょうど上に隠れる位置へ（選んだ地域の見出しが、上のバーのすぐ下に来る）
      var y = nav.getBoundingClientRect().bottom + window.pageYOffset - document.querySelector('.bar').offsetHeight + 2;
      window.scrollTo({ top: y, behavior: 'instant' });
      update();
    });
    sheet.hidden = false; (c.querySelector('[aria-current="true"]') || c.querySelector('a')).focus();
  });
  document.getElementById('sheet-close').addEventListener('click', close);
  sheet.addEventListener('click', function (e) { if (e.target === sheet) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sheet.hidden) close(); });
  update();
})();
