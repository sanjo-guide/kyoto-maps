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
  var start = location.hash === '#season' ? 'season' : null;
  if (!start) { try { start = sessionStorage.getItem(KEY); } catch (e) {} }
  show(start || 'year', false);
})();
