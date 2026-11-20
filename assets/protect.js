/* 写真の保存よけ（全ページ共通）。
   右クリック・長押しの「画像を保存」と、ドラッグでの持ち出しを止めて、短いお知らせを出す。
   ブラウザの仕組み上、完全には防げない（画面の撮影や開発者ツールなど）。気軽な保存を止めるためのもの。
   読み込み: 各ページの <head> に <script src="../assets/protect.js?v=1" defer></script>（トップは assets/…） */
(function () {
  "use strict";
  var css = "img{-webkit-touch-callout:none;-webkit-user-drag:none;user-drag:none;-webkit-user-select:none;user-select:none}";
  var st = document.createElement("style");
  st.textContent = css;
  (document.head || document.documentElement).appendChild(st);

  function isJa() {
    var l = "";
    try { l = localStorage.getItem("kyoto-maps-lang") || localStorage.getItem("kanazawa-lang") || ""; } catch (e) {}
    if (l === "ja") return true;
    if (l === "en") return false;
    return (navigator.language || "").toLowerCase().indexOf("ja") === 0;
  }

  var toast = null, timer = 0;
  function notice() {
    if (!document.body) return;
    if (!toast) {
      toast = document.createElement("div");
      toast.setAttribute("role", "status");
      toast.style.cssText = "position:fixed;left:50%;bottom:calc(84px + env(safe-area-inset-bottom));transform:translateX(-50%);z-index:100000;" +
        "max-width:calc(100% - 32px);padding:10px 16px;border-radius:999px;background:rgba(20,22,24,.88);color:#fff;" +
        "font:500 13.5px/1.4 system-ui,-apple-system,'Hiragino Sans',sans-serif;text-align:center;pointer-events:none;transition:opacity .25s;opacity:0";
      document.body.appendChild(toast);
    }
    toast.textContent = isJa() ? "写真の保存・転載はご遠慮ください（© Toshi）" : "Please don’t save or reuse the photos (© Toshi)";
    toast.style.opacity = "1";
    clearTimeout(timer);
    timer = setTimeout(function () { toast.style.opacity = "0"; }, 2200);
  }

  function onImg(e) {
    var t = e.target;
    return t && t.tagName === "IMG";
  }
  document.addEventListener("contextmenu", function (e) { if (onImg(e)) { e.preventDefault(); notice(); } }, true);
  document.addEventListener("dragstart", function (e) { if (onImg(e)) e.preventDefault(); }, true);
})();
